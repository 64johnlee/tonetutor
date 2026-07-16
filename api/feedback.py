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
    recent = list(
        _client().collection("feedback")
        .where("uid", "==", uid)
        .where("ts", ">=", since)
        .limit(DAILY_LIMIT_PER_UID)
        .stream()
    )
    if len(recent) >= DAILY_LIMIT_PER_UID:
        raise HTTPException(status_code=429, detail="Too many messages today — please try again tomorrow")

    _client().collection("feedback").add({
        "uid": uid,
        "message": message,
        "contact": contact,
        "status": "open",
        "ts": now,
        "day": now.strftime("%Y-%m-%d"),
    })
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
