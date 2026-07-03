from fastapi import APIRouter, HTTPException
from google.api_core.exceptions import ResourceExhausted
from models.schemas import (
    DrillGenerateRequest, DrillGenerateResponse, DrillSentence,
    DrillScoreRequest, DrillScoreResponse,
    WordDrillItem, WordDrillResponse,
)
from services.gemini import get_drill_sentences, score_shadow, get_word_drill

router = APIRouter(prefix="/api/drill", tags=["drill"])


@router.post("/generate", response_model=DrillGenerateResponse)
async def generate_drill(req: DrillGenerateRequest):
    try:
        rows = get_drill_sentences(req.level, req.weak_points, n=10)
    except ResourceExhausted:
        raise HTTPException(status_code=503, detail="Gemini API quota reached — please wait a minute and try again.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="The tutor is taking too long — please try again.")
    if not rows:
        raise HTTPException(status_code=502, detail="Could not generate drill sentences — please try again.")
    return DrillGenerateResponse(sentences=[DrillSentence(**r) for r in rows])


@router.post("/score", response_model=DrillScoreResponse)
async def score_drill(req: DrillScoreRequest):
    if not req.target_zh.strip():
        raise HTTPException(status_code=400, detail="Missing target sentence")
    try:
        result = score_shadow(req.target_zh, req.attempt)
    except ResourceExhausted:
        raise HTTPException(status_code=503, detail="Gemini API quota reached — please wait a minute and try again.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="The tutor is taking too long — please try again.")
    return DrillScoreResponse(**result)


@router.post("/words", response_model=WordDrillResponse)
async def generate_word_drill(req: DrillGenerateRequest):
    try:
        rows = get_word_drill(req.level, req.weak_points, n=8)
    except ResourceExhausted:
        raise HTTPException(status_code=503, detail="Gemini API quota reached — please wait a minute and try again.")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="The tutor is taking too long — please try again.")
    if not rows:
        raise HTTPException(status_code=502, detail="Could not generate word drill — please try again.")
    return WordDrillResponse(items=[WordDrillItem(**r) for r in rows])
