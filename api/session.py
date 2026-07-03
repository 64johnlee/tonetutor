import os
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from google.api_core.exceptions import ResourceExhausted
from models.schemas import (
    StartSessionRequest, SessionStartResponse, SessionSummary, LevelAssessment
)
from services.gemini import get_opening, get_summary, get_level_assessment
from .store import sessions

router = APIRouter(prefix="/api/session", tags=["session"])

# Paywall is off until Lemon Squeezy is configured, so the app stays free until then.
BILLING_ON = bool(os.getenv("LEMON_API_KEY"))


@router.post("/start", response_model=SessionStartResponse)
async def start_session(req: StartSessionRequest):
    if BILLING_ON and req.uid:
        from services.db import can_start_and_consume
        access = can_start_and_consume(req.uid)
        if not access["allowed"]:
            raise HTTPException(status_code=402, detail="free_exhausted")
    try:
        opening = get_opening(req.topic, req.level)
    except ResourceExhausted:
        raise HTTPException(status_code=503, detail="Gemini API quota reached — please wait a minute and try again.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="The tutor is taking too long — please try again.")
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "topic": req.topic,
        "level": req.level,
        "history": [],
        "opening": opening["reply_zh"],
        "created_at": datetime.utcnow().isoformat(),
        "free_turns_used": 0,
        "focus": req.focus or "",
    }
    return SessionStartResponse(
        session_id=session_id,
        opening_zh=opening["reply_zh"],
        opening_pinyin=opening["reply_pinyin"],
        opening_en=opening["reply_en"],
        topic=req.topic.value,
        level=req.level.value,
    )


@router.get("/{session_id}/summary", response_model=SessionSummary)
async def get_session_summary(session_id: str):
    sess = sessions.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    if not sess["history"]:
        raise HTTPException(status_code=400, detail="No conversation to summarise yet")
    try:
        data = get_summary(sess["history"])
    except ResourceExhausted:
        raise HTTPException(status_code=503, detail="Gemini API quota reached — please wait a minute and try again.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="The tutor is taking too long — please try again.")
    return SessionSummary(
        session_id=session_id,
        overall_score=data.get("overall_score", 5),
        strengths=data.get("strengths", []),
        top_mistakes=data.get("top_mistakes", []),
        vocab_to_review=data.get("vocab_to_review", []),
        next_focus=data.get("next_focus", ""),
        turns=len(sess["history"]),
    )


@router.get("/{session_id}/assessment", response_model=LevelAssessment)
async def get_level_test(session_id: str):
    sess = sessions.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    if not sess["history"]:
        raise HTTPException(status_code=400, detail="No conversation to assess yet")
    try:
        data = get_level_assessment(sess["history"])
    except ResourceExhausted:
        raise HTTPException(status_code=503, detail="Gemini API quota reached — please wait a minute and try again.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="The tutor is taking too long — please try again.")
    return LevelAssessment(
        session_id=session_id,
        estimated_level=data["estimated_level"],
        score=data["score"],
        headline=data["headline"],
        strengths=data["strengths"],
        weaknesses=data["weaknesses"],
        share_blurb=data["share_blurb"],
        turns=len(sess["history"]),
    )
