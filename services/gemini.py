import json
import re
import vertexai
from vertexai.generative_models import GenerativeModel
from models.schemas import (
    Grade, TOPIC_DESCRIPTIONS, HSK_DESCRIPTIONS, Topic, HskLevel
)

vertexai.init(project="disco-module-487411-m0", location="us-central1")

_model_cache = None

def _get_model():
    global _model_cache
    if _model_cache is None:
        _model_cache = GenerativeModel("gemini-2.5-flash")
    return _model_cache


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
    model = _get_model()
    scenario = TOPIC_DESCRIPTIONS[topic]
    lvl_desc = HSK_DESCRIPTIONS[level]
    prompt = OPENING_PROMPT.format(scenario=scenario, level=lvl_desc)
    response = model.generate_content(prompt, generation_config={"temperature": 0.7})
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
    model = _get_model()
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
    response = model.generate_content(prompt, generation_config={"temperature": 0.7})
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
    model = _get_model()
    history_text = "\n".join(
        f"Learner: {t['learner']}\nLin Wei: {t['lin_wei']}"
        for t in history
    )
    prompt = SUMMARY_PROMPT.format(history=history_text)
    response = model.generate_content(prompt, generation_config={"temperature": 0.3})
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
    model = _get_model()
    history_text = "\n".join(
        f"Learner: {t['learner']}\nLin Wei: {t['lin_wei']}"
        for t in history
    )
    prompt = ASSESS_PROMPT.format(history=history_text)
    response = model.generate_content(prompt, generation_config={"temperature": 0.3})
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
    response = model.generate_content(prompt, generation_config={"temperature": 0.4})
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
