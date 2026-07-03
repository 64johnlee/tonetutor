import concurrent.futures
import json
import re
import vertexai
from vertexai.generative_models import GenerativeModel
from models.schemas import (
    Grade, TOPIC_DESCRIPTIONS, HSK_DESCRIPTIONS, Topic, HskLevel
)

vertexai.init(project="disco-module-487411-m0", location="us-central1")

_model_cache = {}

# User-facing calls (chat, summary, assessment, drills) use Flash-Lite — thinking is
# OFF by default so latency stays interactive (full Flash took ~8s+ per summary).
# Full Flash remains for non-blocking / low-frequency paths (copilot, shadow scoring).
FAST_MODEL = "gemini-2.5-flash-lite"
QUALITY_MODEL = "gemini-2.5-flash"

def _get_model(name=QUALITY_MODEL):
    if name not in _model_cache:
        _model_cache[name] = GenerativeModel(name)
    return _model_cache[name]


_gen_pool = concurrent.futures.ThreadPoolExecutor(max_workers=8)
GEN_DEADLINE_S = 30


def _generate(model, prompt: str, config: dict):
    """generate_content with JSON mode, a hard per-attempt deadline, one retry.

    Vertex occasionally stalls far past Cloud Run's 60s request timeout, which
    surfaced to users as an opaque 504 ("upstream request timeout"). Every call
    also sets max_output_tokens via `config` so a repetition loop can't run
    unbounded. Non-timeout errors (e.g. quota) propagate untouched so the
    routers' ResourceExhausted handling keeps working.
    """
    config = {**config, "response_mime_type": "application/json"}
    for attempt in (1, 2):
        future = _gen_pool.submit(model.generate_content, prompt, generation_config=config)
        try:
            return future.result(timeout=GEN_DEADLINE_S)
        except concurrent.futures.TimeoutError:
            future.cancel()
            if attempt == 2:
                raise TimeoutError(f"Gemini did not answer within {GEN_DEADLINE_S}s (2 attempts)")


def _parse_json(text: str) -> dict:
    text = re.sub(r"```(?:json)?\s*", "", text).strip().rstrip("`")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            return json.loads(m.group())
        raise RuntimeError(f"Gemini returned non-JSON response: {text[:200]}")


def _safe_str(data: dict, key: str, fallback: str = "") -> str:
    val = data.get(key)
    return str(val) if val is not None else fallback


SYSTEM_CHAT = (
    "You are Lin Wei, a friendly native Mandarin speaker helping an English speaker practice. "
    "Always return valid JSON only — no markdown, no extra text."
)

CHAT_PROMPT = """Scenario: {scenario}
Learner level: {level}

Conversation so far:
{history}

Learner's latest message: "{user_message}"

Note: the learner's message may come from speech recognition and can contain mis-hearings (near-homophones or nonsensical substitutions). If an apparent error looks like a likely speech-recognition mistake rather than a genuine learner error, do NOT count it as a tone or grammar mistake.

Grade the learner's message and continue the conversation naturally.

Return ONLY this JSON (no markdown):
{{
  "reply_zh": "your reply in simplified Chinese",
  "reply_pinyin": "pinyin with tone numbers (e.g. ni3 hao3)",
  "reply_en": "English translation of your reply",
  "grade": {{
    "score": <1-10>,
    "correct": "what they got right (brief, in English)",
    "tone_errors": ["list each tone error as 'said X should be Y'"],
    "suggestion": "a more natural phrasing if applicable, else null"
  }}
}}"""

SUMMARY_PROMPT = """Review this Mandarin practice session and return ONLY this JSON (no markdown):
{{
  "overall_score": <1-10>,
  "strengths": ["up to 3 things done well"],
  "top_mistakes": ["up to 3 most important mistakes"],
  "vocab_to_review": ["word: meaning", "...up to 5 items"],
  "next_focus": "one sentence on what to practise next"
}}

Session:
{history}"""

OPENING_PROMPT = """You are Lin Wei, a friendly native Mandarin speaker.
Scenario: {scenario}
Learner level: {level}

Open the conversation with a natural first line IN Mandarin (as Lin Wei in this scenario).
Return ONLY this JSON (no markdown):
{{
  "reply_zh": "opening line in simplified Chinese",
  "reply_pinyin": "pinyin with tone numbers",
  "reply_en": "English translation"
}}"""


def get_opening(topic: Topic, level: HskLevel) -> dict:
    model = _get_model(FAST_MODEL)
    scenario = TOPIC_DESCRIPTIONS[topic]
    lvl_desc = HSK_DESCRIPTIONS[level]
    prompt = OPENING_PROMPT.format(scenario=scenario, level=lvl_desc)
    response = _generate(model, prompt, {"temperature": 0.7, "max_output_tokens": 512})
    data = _parse_json(response.text)
    return {
        "reply_zh": _safe_str(data, "reply_zh", "你好！"),
        "reply_pinyin": _safe_str(data, "reply_pinyin", "ni3 hao3!"),
        "reply_en": _safe_str(data, "reply_en", "Hello!"),
    }


def chat_turn(
    topic: Topic,
    level: HskLevel,
    history: list[dict],
    user_message: str,
    opening_zh: str = "",
    focus: str = "",
) -> dict:
    model = _get_model(FAST_MODEL)
    scenario = TOPIC_DESCRIPTIONS[topic]
    lvl_desc = HSK_DESCRIPTIONS[level]

    history_lines = []
    if opening_zh:
        history_lines.append(f"Lin Wei: {opening_zh}")
    for t in history:
        history_lines.append(f"Learner: {t['learner']}")
        history_lines.append(f"Lin Wei: {t['lin_wei']}")
    history_text = "\n".join(history_lines) if history_lines else "(start of conversation)"

    focus_note = (
        f"\nThe learner is specifically working on these weak points: {focus}. "
        "Naturally create chances for them to practise these, and pay extra attention to them when grading.\n"
        if focus else ""
    )
    prompt = SYSTEM_CHAT + focus_note + "\n\n" + CHAT_PROMPT.format(
        scenario=scenario,
        level=lvl_desc,
        history=history_text,
        user_message=user_message,
    )
    response = _generate(model, prompt, {"temperature": 0.7, "max_output_tokens": 1024})
    data = _parse_json(response.text)

    grade_raw = data.get("grade") or {}
    grade = None
    if grade_raw.get("score") is not None:
        raw_errors = grade_raw.get("tone_errors")
        grade = Grade(
            score=int(grade_raw.get("score", 5)),
            correct=_safe_str(grade_raw, "correct", ""),
            tone_errors=raw_errors if isinstance(raw_errors, list) else [],
            suggestion=grade_raw.get("suggestion"),
        )
    return {
        "reply_zh": _safe_str(data, "reply_zh", "请继续。"),
        "reply_pinyin": _safe_str(data, "reply_pinyin", "qing3 ji4xu4."),
        "reply_en": _safe_str(data, "reply_en", "Please continue."),
        "grade": grade,
    }


def get_summary(history: list[dict]) -> dict:
    model = _get_model(FAST_MODEL)
    history_text = "\n".join(
        f"Learner: {t['learner']}\nLin Wei: {t['lin_wei']}"
        for t in history
    )
    prompt = SUMMARY_PROMPT.format(history=history_text)
    response = _generate(model, prompt, {"temperature": 0.3, "max_output_tokens": 1024})
    data = _parse_json(response.text)
    return {
        "overall_score": int(data.get("overall_score", 5)),
        "strengths": data.get("strengths") or [],
        "top_mistakes": data.get("top_mistakes") or [],
        "vocab_to_review": data.get("vocab_to_review") or [],
        "next_focus": _safe_str(data, "next_focus", "Keep practising!"),
    }


ASSESS_PROMPT = """You are an experienced HSK examiner. Based ONLY on the LEARNER's Mandarin in this short practice conversation, estimate their spoken HSK level. Judge what the learner actually produced — grammar control, vocabulary range, sentence complexity, and accuracy. Lin Wei's lines are context only; do NOT grade them.

Conversation:
{history}

Important: the learner's lines may come from automatic speech recognition and can contain transcription errors (near-homophones or nonsensical fragments). Do NOT penalise the learner for words that are clearly speech-recognition mis-hearings rather than their own mistakes, and do NOT quote nonsensical mis-transcribed fragments as evidence of weaknesses. Judge their level from the overall meaning and structure they were clearly trying to produce.

Be encouraging but honest, and estimate conservatively from the evidence. If the learner barely produced any Mandarin, lean to a lower level and say the result is rough.

Return ONLY this JSON (no markdown):
{{
  "estimated_level": "exactly one of: HSK 1, HSK 2, HSK 3, HSK 4, HSK 5, HSK 6",
  "score": <integer 0-100, overall spoken-proficiency score>,
  "headline": "one punchy sentence the learner can share, e.g. 'Your spoken Mandarin is a solid HSK 3 — strong grammar, watch your tones.'",
  "strengths": ["up to 3 concrete strengths"],
  "weaknesses": ["up to 3 concrete things to improve"],
  "share_blurb": "a short first-person social caption, e.g. 'I just tested my Mandarin on ToneTutor and I speak at HSK 3 level! Test yours:'"
}}"""

_VALID_LEVELS = {"HSK 1", "HSK 2", "HSK 3", "HSK 4", "HSK 5", "HSK 6"}


def get_level_assessment(history: list[dict]) -> dict:
    model = _get_model(FAST_MODEL)
    history_text = "\n".join(
        f"Learner: {t['learner']}\nLin Wei: {t['lin_wei']}"
        for t in history
    )
    prompt = ASSESS_PROMPT.format(history=history_text)
    response = _generate(model, prompt, {"temperature": 0.3, "max_output_tokens": 1024})
    data = _parse_json(response.text)

    level = _safe_str(data, "estimated_level", "HSK 1").strip()
    if level not in _VALID_LEVELS:
        # Normalise loose forms like "HSK3" / "hsk 3" → "HSK 3", else fall back.
        digits = re.findall(r"[1-6]", level)
        level = f"HSK {digits[0]}" if digits else "HSK 1"

    try:
        score = int(data.get("score", 50))
    except (ValueError, TypeError):
        score = 50
    score = max(0, min(100, score))

    return {
        "estimated_level": level,
        "score": score,
        "headline": _safe_str(data, "headline", ""),
        "strengths": data.get("strengths") or [],
        "weaknesses": data.get("weaknesses") or [],
        "share_blurb": _safe_str(data, "share_blurb", ""),
    }


COPILOT_PROMPT = """You are Lin Wei, stepping OUT of the roleplay to act as the learner's
patient Mandarin teacher. Answer their question in clear, encouraging English, grounded in
THIS practice session. Be concrete and show Mandarin examples with pinyin tone numbers.

Learner level: {level}
Weak points flagged so far this session: {weak_points}

Recent conversation (Lin Wei = you in roleplay, Learner = the student):
{history}

The learner's question to you (their teacher): "{question}"

Return ONLY this JSON (no markdown):
{{
  "answer_en": "the explanation, in English",
  "examples": [{{"zh": "simplified Chinese", "pinyin": "pinyin with tone numbers e.g. ni3 hao3", "en": "English"}}],
  "drill_focus": "if practice would help, a SHORT weak-point string to target a focused session (e.g. '3rd tone, 是/不是'), else null"
}}"""


def copilot_turn(
    level: HskLevel,
    history: list[dict],
    weak_points: str,
    question: str,
) -> dict:
    model = _get_model()
    lvl_desc = HSK_DESCRIPTIONS[level]
    history_lines = []
    for t in history:
        history_lines.append(f"Learner: {t['learner']}")
        history_lines.append(f"Lin Wei: {t['lin_wei']}")
    history_text = "\n".join(history_lines) if history_lines else "(no conversation yet)"
    prompt = COPILOT_PROMPT.format(
        level=lvl_desc,
        weak_points=weak_points or "nothing flagged yet",
        history=history_text,
        question=question,
    )
    response = _generate(model, prompt, {"temperature": 0.4, "max_output_tokens": 1024})
    data = _parse_json(response.text)

    examples = []
    for ex in (data.get("examples") or [])[:5]:
        if isinstance(ex, dict) and ex.get("zh"):
            examples.append({
                "zh": _safe_str(ex, "zh", ""),
                "pinyin": _safe_str(ex, "pinyin", ""),
                "en": _safe_str(ex, "en", ""),
            })

    drill = str(data.get("drill_focus") or "").strip()
    if drill.lower() in ("", "null", "none", "n/a"):
        drill = None
    return {
        "answer_en": _safe_str(data, "answer_en", "Let's go over that again."),
        "examples": examples,
        "drill_focus": drill,
    }


# ── Shadow Drill: generate target sentences + score shadow attempts ──
DRILL_GEN_PROMPT = """You are a Mandarin speaking coach building a SHADOWING drill to RE-TRAIN a learner on their weak spots (not teach new material).

Learner level: {level}
Their weak points from a speaking test: {weak_points}

Write exactly {n} short, natural spoken Mandarin sentences for them to shadow (hear, then repeat aloud). Rules:
- Keep each sentence at or slightly below their level — this is retraining, not stretching.
- Each sentence should deliberately exercise one of their weak points (tones, a grammar pattern, etc.).
- Everyday, speakable sentences (things a person actually says), 4-12 characters each.
- Spread the weak points across the set; vary the sentences.

Return ONLY this JSON (no markdown):
{{
  "sentences": [
    {{"zh": "simplified Chinese", "pinyin": "pinyin with tone numbers e.g. ni3 hao3", "en": "English", "focus": "the weak point this trains, in a few words"}}
  ]
}}"""


def get_drill_sentences(level: HskLevel, weak_points: str, n: int = 10) -> list[dict]:
    model = _get_model(FAST_MODEL)
    lvl_desc = HSK_DESCRIPTIONS[level]
    prompt = DRILL_GEN_PROMPT.format(
        level=lvl_desc,
        weak_points=weak_points.strip() or "general tones and sentence rhythm",
        n=n,
    )
    response = _generate(model, prompt, {"temperature": 0.7, "max_output_tokens": 2048})
    data = _parse_json(response.text)
    out = []
    for s in (data.get("sentences") or [])[:n]:
        if isinstance(s, dict) and s.get("zh"):
            out.append({
                "zh": _safe_str(s, "zh", ""),
                "pinyin": _safe_str(s, "pinyin", ""),
                "en": _safe_str(s, "en", ""),
                "focus": _safe_str(s, "focus", ""),
            })
    return out


DRILL_SCORE_PROMPT = """A learner is shadowing (repeating) a target Mandarin sentence. You are scoring how well their spoken attempt matched the target.

Target sentence: "{target}"
What speech recognition heard them say: "{attempt}"

Score how closely the attempt matches the target in words and structure. Note: this is a speech-recognition transcript, so judge meaning and word match, NOT raw tone pitch (you cannot hear pitch). Minor homophone mis-hearings should be treated leniently. If the attempt is empty or unrelated, score low.

Return ONLY this JSON (no markdown):
{{
  "score": <integer 0-100, how well it matched>,
  "feedback": "one short, encouraging line of feedback (English)",
  "missed": ["any words/parts that were dropped or wrong, each as a short string; empty list if none"]
}}"""

DRILL_PASS_THRESHOLD = 75


def score_shadow(target_zh: str, attempt: str) -> dict:
    if not attempt.strip():
        return {"score": 0, "passed": False,
                "feedback": "I didn't catch that — tap the mic and say it again.", "missed": []}
    model = _get_model()
    prompt = DRILL_SCORE_PROMPT.format(target=target_zh, attempt=attempt)
    response = _generate(model, prompt, {"temperature": 0.2, "max_output_tokens": 512})
    data = _parse_json(response.text)
    try:
        score = int(data.get("score", 0))
    except (ValueError, TypeError):
        score = 0
    score = max(0, min(100, score))
    raw_missed = data.get("missed")
    missed = [str(m) for m in raw_missed][:5] if isinstance(raw_missed, list) else []
    return {
        "score": score,
        "passed": score >= DRILL_PASS_THRESHOLD,
        "feedback": _safe_str(data, "feedback", "Nice work — keep going!"),
        "missed": missed,
    }


# ── Word Drill: tap-the-missing-word vocab recognition items ──
WORD_DRILL_PROMPT = """You are building a "tap the missing word" Mandarin vocab drill to RE-TRAIN a learner on their weak spots.

Learner level: {level}
Their weak points from a speaking test: {weak_points}

Write exactly {n} short, natural spoken Mandarin sentences. For each, pick ONE meaningful word to be the missing answer, and give 4 answer choices (the correct word plus 3 plausible but wrong distractors of the same kind). Rules:
- Sentences at or slightly below the learner's level; everyday and speakable (4-12 characters).
- The answer word should exercise one of their weak points where possible.
- Distractors must be believable (same part of speech / category), not random.
- "sentence" must be the COMPLETE sentence with the answer already in it (used for audio).

Return ONLY this JSON (no markdown):
{{
  "items": [
    {{"sentence": "complete simplified Chinese sentence", "answer": "the missing word", "options": ["4 choices incl. the answer, shuffled"], "pinyin": "pinyin of the full sentence with tone numbers", "en": "English translation", "focus": "the weak point this trains, a few words"}}
  ]
}}"""


def get_word_drill(level: HskLevel, weak_points: str, n: int = 8) -> list[dict]:
    model = _get_model(FAST_MODEL)
    lvl_desc = HSK_DESCRIPTIONS[level]
    prompt = WORD_DRILL_PROMPT.format(
        level=lvl_desc,
        weak_points=weak_points.strip() or "common everyday vocabulary and measure words",
        n=n,
    )
    response = _generate(model, prompt, {"temperature": 0.7, "max_output_tokens": 2048})
    data = _parse_json(response.text)
    out = []
    for it in (data.get("items") or [])[:n]:
        if not isinstance(it, dict):
            continue
        sentence = _safe_str(it, "sentence", "")
        answer = _safe_str(it, "answer", "")
        raw_opts = it.get("options")
        options = [str(o) for o in raw_opts if str(o).strip()] if isinstance(raw_opts, list) else []
        if answer and answer not in options:      # make sure the answer is always selectable
            options.append(answer)
        options = list(dict.fromkeys(options))[:4]  # dedupe, cap at 4
        if sentence and answer and len(options) >= 2:
            out.append({
                "sentence": sentence,
                "answer": answer,
                "options": options,
                "pinyin": _safe_str(it, "pinyin", ""),
                "en": _safe_str(it, "en", ""),
                "focus": _safe_str(it, "focus", ""),
            })
    return out
