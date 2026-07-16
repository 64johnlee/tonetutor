"""In-app support tickets ("Help & feedback" button).

Users submit a message (+ optional contact email) from the frontend modal;
tickets land in the Firestore "feedback" collection. The owner reads them via
the token-guarded /api/feedback/list endpoint (same EV_STATS_TOKEN guard and
hidden-404 behaviour as /api/ev/stats).
"""
import os
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.cloud import firestore

from services.mailer import send_email, notify_owner

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

MAX_MESSAGE_LEN = 2000
MIN_MESSAGE_LEN = 5
MAX_CONTACT_LEN = 200
DAILY_LIMIT_PER_UID = 5

_db = None


def _client():
    global _db
    if _db is None:
        _db = firestore.Client()
    return _db


class FeedbackIn(BaseModel):
    uid: str
    message: str
    contact: str = ""
    website: str = ""  # honeypot — real users never fill this


CONFIRMATION_SUBJECT = "Got your message — ToneTutor"
CONFIRMATION_BODY = (
    "你好!\n\n"
    "Thanks for writing in — your message reached me (a real person, not a bot).\n"
    "I read every message and will reply within 24-48 hours.\n\n"
    "Your message:\n{message}\n\n"
    "— John, founder of ToneTutor\n"
    "https://tonetutor.tefusiang.com\n"
)


@router.post("")
async def submit_feedback(body: FeedbackIn):
    uid = body.uid.strip()
    message = body.message.strip()
    contact = body.contact.strip()[:MAX_CONTACT_LEN]

    if not uid:
        raise HTTPException(status_code=400, detail="Missing uid")
    if body.website:
        # Honeypot tripped: pretend success, store nothing.
        return {"ok": True}
    if len(message) < MIN_MESSAGE_LEN:
        raise HTTPException(status_code=400, detail="Message too short")
    if len(message) > MAX_MESSAGE_LEN:
        raise HTTPException(status_code=400, detail="Message too long")

    now = datetime.now(timezone.utc)
    since = now - timedelta(days=1)
    # uid-only filter stays on Firestore's auto-index (uid+ts range would need a
    # composite index); recency is counted client-side over a tiny result set.
    recent = _client().collection("feedback").where("uid", "==", uid).limit(50).stream()
    recent_count = sum(1 for snap in recent if (snap.to_dict() or {}).get("ts") and snap.to_dict()["ts"] >= since)
    if recent_count >= DAILY_LIMIT_PER_UID:
        raise HTTPException(status_code=429, detail="Too many messages today — please try again tomorrow")

    _client().collection("feedback").add({
        "uid": uid,
        "message": message,
        "contact": contact,
        "status": "open",
        "ts": now,
        "day": now.strftime("%Y-%m-%d"),
    })

    # Send inline (not BackgroundTasks): Cloud Run throttles CPU after the
    # response, which silently freezes post-response coroutines. A feedback
    # POST can afford the extra second; both sends are still best-effort.
    if contact:
        await send_email(contact, CONFIRMATION_SUBJECT,
                         CONFIRMATION_BODY.format(message=message))
    await notify_owner(
        f"🎫 New ToneTutor ticket — {contact or uid[:12]}",
        f"Message:\n{message}\n\nContact: {contact or '(none left)'}\nuid: {uid}\nTime: {now.isoformat()}",
        contact,  # reply_to: hit Reply to answer the user directly
    )
    return {"ok": True}


@router.get("/list")
async def list_feedback(token: str = "", limit: int = 50):
    """Owner-only ticket readout; 404 (not 401) on bad token to stay hidden."""
    expected = os.getenv("EV_STATS_TOKEN")
    if not expected or token != expected:
        raise HTTPException(status_code=404, detail="Not found")

    limit = max(1, min(limit, 200))
    q = (
        _client().collection("feedback")
        .order_by("ts", direction=firestore.Query.DESCENDING)
        .limit(limit)
    )
    tickets = []
    for snap in q.stream():
        d = snap.to_dict() or {}
        tickets.append({
            "id": snap.id,
            "uid": d.get("uid"),
            "message": d.get("message"),
            "contact": d.get("contact"),
            "status": d.get("status"),
            "ts": d.get("ts").isoformat() if d.get("ts") else None,
        })
    return {"count": len(tickets), "tickets": tickets}
