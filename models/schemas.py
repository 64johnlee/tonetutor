from pydantic import BaseModel
from typing import Optional
from enum import Enum


class HskLevel(str, Enum):
    hsk1 = "HSK1"
    hsk2 = "HSK2"
    hsk3 = "HSK3"
    hsk4 = "HSK4"
    hsk5 = "HSK5"
    hsk6 = "HSK6"


class Topic(str, Enum):
    restaurant = "restaurant"
    shopping = "shopping"
    travel = "travel"
    work = "work"
    friends = "friends"
    doctor = "doctor"


TOPIC_DESCRIPTIONS = {
    Topic.restaurant: "ordering food and drinks at a Chinese restaurant",
    Topic.shopping: "buying clothes or items at a market or shop",
    Topic.travel: "asking for directions, buying train/bus tickets, checking into a hotel",
    Topic.work: "a work meeting introduction or discussing a project with a colleague",
    Topic.friends: "meeting someone new and making small talk",
    Topic.doctor: "describing symptoms to a doctor at a clinic",
}

HSK_DESCRIPTIONS = {
    HskLevel.hsk1: "absolute beginner (150 words). Use very simple sentences only.",
    HskLevel.hsk2: "beginner (300 words). Simple sentences, common daily topics.",
    HskLevel.hsk3: "elementary (600 words). Can handle most daily situations.",
    HskLevel.hsk4: "intermediate (1200 words). Can discuss abstract topics.",
    HskLevel.hsk5: "upper-intermediate (2500 words). Can read newspapers and watch films.",
    HskLevel.hsk6: "advanced (5000+ words). Near-native fluency, nuanced expression.",
}


class StartSessionRequest(BaseModel):
    topic: Topic
    level: HskLevel = HskLevel.hsk2
    uid: Optional[str] = None


class ChatRequest(BaseModel):
    session_id: str
    user_message: str


class Grade(BaseModel):
    score: int
    correct: str
    tone_errors: list[str]
    suggestion: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    reply_zh: str
    reply_pinyin: str
    reply_en: str
    grade: Optional[Grade] = None
    turn: int


class SessionSummary(BaseModel):
    session_id: str
    overall_score: int
    strengths: list[str]
    top_mistakes: list[str]
    vocab_to_review: list[str]
    next_focus: str
    turns: int


class SessionStartResponse(BaseModel):
    session_id: str
    opening_zh: str
    opening_pinyin: str
    opening_en: str
    topic: str
    level: str
