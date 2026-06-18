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

    prompt = SYSTEM_CHAT + "\n\n" + CHAT_PROMPT.format(
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
