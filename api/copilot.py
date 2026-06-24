from fastapi import APIRouter, HTTPException
from google.api_core.exceptions import ResourceExhausted
from models.schemas import CopilotRequest, CopilotResponse
from services.gemini import copilot_turn
from .store import sessions

router = APIRouter(prefix="/api", tags=["copilot"])


@router.post("/copilot", response_model=CopilotResponse)
async def copilot(req: CopilotRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    sess = sessions.get(req.session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        result = copilot_turn(
            level=sess["level"],
            history=sess["history"],
            weak_points=sess.get("weak_points", ""),
            question=req.question,
        )
    except ResourceExhausted:
        raise HTTPException(status_code=503, detail="Gemini API quota reached — please wait a minute and try again.")

    return CopilotResponse(**result)
