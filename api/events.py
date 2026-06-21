"""First-party funnel analytics (GROWTH_HSK.md §10).

A single lightweight collector endpoint the front-end pings via navigator.sendBeacon,
plus an admin-only stats readout that computes the funnel ratios we actually act on
(completion rate, share rate, practice CTR). Events are stored in Firestore so the
data stays first-party (no GA/cookie banner — important for the EU/RU launch pools).
"""
import json
import os
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Request, Response, HTTPException
from google.cloud import firestore

router = APIRouter(prefix="/api/ev", tags=["events"])

# Allowlisted funnel events. Anything else is silently dropped (no spoofed events).
ALLOWED_EVENTS = {
    "test_started", "test_completed", "card_rendered",
    "card_shared", "card_saved", "caption_copied",
    "practice_from_card", "paywall_hit", "subscribe",
}

_db = None


def _client():
    global _db
    if _db is None:
        _db = firestore.Client()
    return _db


@router.post("")
async def record_event(request: Request):
    """Fire-and-forget event sink. Parses leniently (sendBeacon sends raw JSON),
    swallows every error, and always returns 204 — analytics must never break UX."""
    try:
        raw = await request.body()
        data = json.loads(raw or b"{}")
        event = str(data.get("event") or "")
        uid = str(data.get("uid") or "")
        if event in ALLOWED_EVENTS and uid:
            props = data.get("props")
            if not isinstance(props, dict):
                props = {}
            now = datetime.now(timezone.utc)
            _client().collection("events").add({
                "event": event,
                "uid": uid,
                "props": props,
                "ts": now,
                "day": now.strftime("%Y-%m-%d"),
            })
    except Exception:
        pass
    return Response(status_code=204)


@router.get("/stats")
async def stats(token: str = "", since: str = ""):
    """Admin-only funnel readout. Guarded by the EV_STATS_TOKEN env var; returns 404
    (not 401) when the token is missing/wrong so the endpoint's existence stays hidden."""
    expected = os.getenv("EV_STATS_TOKEN")
    if not expected or token != expected:
        raise HTTPException(status_code=404, detail="Not found")

    if not since:
        since = (datetime.now(timezone.utc) - timedelta(days=14)).strftime("%Y-%m-%d")

    # Single-field inequality on "day" is auto-indexed; cap reads so a hot collection
    # can't blow up a single stats call.
    q = _client().collection("events").where("day", ">=", since).limit(50000)

    counts = {}
    uids_by_event = {}
    scanned = 0
    for snap in q.stream():
        scanned += 1
        d = snap.to_dict() or {}
        ev = d.get("event")
        if ev not in ALLOWED_EVENTS:
            continue
        counts[ev] = counts.get(ev, 0) + 1
        uids_by_event.setdefault(ev, set()).add(d.get("uid"))

    def u(ev):
        return uids_by_event.get(ev, set())

    def rate(a, b):
        return round(len(a) / len(b), 3) if b else None

    started_u = u("test_started")
    completed_u = u("test_completed")
    rendered_u = u("card_rendered")
    shared_any_u = u("card_shared") | u("card_saved") | u("caption_copied")
    practice_u = u("practice_from_card")

    return {
        "since": since,
        "events_scanned": scanned,
        "counts": {e: counts.get(e, 0) for e in sorted(ALLOWED_EVENTS)},
        "unique_uids": {e: len(uids_by_event.get(e, set())) for e in sorted(ALLOWED_EVENTS)},
        "rates": {
            "completion_rate": rate(completed_u, started_u),  # §10 pass ≥0.60 / healthy ≥0.75
            "share_rate": rate(shared_any_u, rendered_u),      # §10 THE lever: pass ≥0.15 / healthy ≥0.30
            "practice_ctr": rate(practice_u, completed_u),     # §10 pass ≥0.40 / healthy ≥0.60
        },
        "note": (
            "share_rate = distinct uids who shared/saved/copied ÷ distinct uids who got a card. "
            "Viral coefficient K needs referral attribution (not tracked yet)."
        ),
    }
