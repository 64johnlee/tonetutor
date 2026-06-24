from fastapi import APIRouter, HTTPException
from google.api_core.exceptions import ResourceExhausted
from models.schemas import ChatRequest, ChatResponse
from services.gemini import chat_turn
from .store import sessions

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.user_message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    sess = sessions.get(req.session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        result = chat_turn(
            topic=sess["topic"],
            level=sess["level"],
            history=sess["history"],
            user_message=req.user_message,
            opening_zh=sess.get("opening", ""),
            focus=sess.get("focus", ""),
        )
    except ResourceExhausted:
        raise HTTPException(status_code=503, detail="Gemini API quota reached — please wait a minute and try again.")

    grade = result["grade"]
    sess["history"].append({
        "lin_wei": result["reply_zh"],
        "learner": req.user_message,
        "grade": grade.model_dump() if grade else None,
    })
    sess["free_turns_used"] += 1

    # Accumulate tone mistakes across the session so the copilot can target them.
    if grade and grade.tone_errors:
        weak_list = sess.setdefault("weak_points_list", [])
        weak_list.extend(grade.tone_errors)
        sess["weak_points"] = " · ".join(weak_list[-8:])

    return ChatResponse(
        session_id=req.session_id,
        reply_zh=result["reply_zh"],
        reply_pinyin=result["reply_pinyin"],
        reply_en=result["reply_en"],
        grade=result["grade"],
        turn=len(sess["history"]),
    )
