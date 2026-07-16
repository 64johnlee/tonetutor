"""Firestore-backed user access store (paid status + free-session counting).

Only used when billing is enabled (LEMON_API_KEY set). Each user is keyed
by an anonymous browser id (uid) stored in localStorage on the client.
"""
from datetime import datetime
from google.cloud import firestore

FREE_LIMIT = 3

_db = None


def _client():
    global _db
    if _db is None:
        _db = firestore.Client()
    return _db


def _effective_limit(data: dict) -> int:
    """Base free limit plus any earned bonus sessions (share/email rewards)."""
    return FREE_LIMIT + int(data.get("bonus_sessions", 0))


def get_status(uid: str) -> dict:
    """Read-only access status for a uid (no mutation)."""
    snap = _client().collection("users").document(uid).get()
    data = snap.to_dict() if snap.exists else {}
    return {
        "paid": bool(data.get("paid", False)),
        "free_used": int(data.get("free_used", 0)),
        "free_limit": _effective_limit(data),
    }


def mark_paid(uid: str, provider_ref: str | None = None) -> None:
    """Mark a uid as a paying subscriber (called from the billing webhook).

    provider_ref is the billing provider's id (e.g. Lemon Squeezy subscription id).
    """
    _client().collection("users").document(uid).set(
        {
            "paid": True,
            "provider_ref": provider_ref,
            "updated_at": datetime.utcnow().isoformat(),
        },
        merge=True,
    )


def can_start_and_consume(uid: str) -> dict:
    """Atomically decide whether a uid may start a session.

    Paid users: always allowed, nothing consumed.
    Free users: allowed while free_used < FREE_LIMIT, consuming one on success.
    Returns {allowed, paid, free_used, free_limit}.
    """
    ref = _client().collection("users").document(uid)
    transaction = _client().transaction()

    @firestore.transactional
    def _txn(txn):
        snap = ref.get(transaction=txn)
        data = snap.to_dict() if snap.exists else {}
        paid = bool(data.get("paid", False))
        free_used = int(data.get("free_used", 0))
        limit = _effective_limit(data)
        if paid:
            return {"allowed": True, "paid": True, "free_used": free_used, "free_limit": limit}
        if free_used >= limit:
            return {"allowed": False, "paid": False, "free_used": free_used, "free_limit": limit}
        new_used = free_used + 1
        txn.set(ref, {"free_used": new_used, "updated_at": datetime.utcnow().isoformat()}, merge=True)
        return {"allowed": True, "paid": False, "free_used": new_used, "free_limit": limit}

    return _txn(transaction)


# One-time bonus grants: kind -> (user-doc flag, sessions added)
BONUS_KINDS = {"share": ("share_rewarded", 1), "email": ("email_rewarded", 3)}


def grant_bonus(uid: str, kind: str) -> dict:
    """Grant a one-time bonus (share = +1 session, email = +3). Idempotent per
    uid+kind: repeat calls return granted=False with current status."""
    flag, amount = BONUS_KINDS[kind]
    ref = _client().collection("users").document(uid)
    transaction = _client().transaction()

    @firestore.transactional
    def _txn(txn):
        snap = ref.get(transaction=txn)
        data = snap.to_dict() if snap.exists else {}
        if data.get(flag):
            return {"granted": False, "paid": bool(data.get("paid", False)),
                    "free_used": int(data.get("free_used", 0)), "free_limit": _effective_limit(data)}
        bonus = int(data.get("bonus_sessions", 0)) + amount
        txn.set(ref, {flag: True, "bonus_sessions": bonus,
                      "updated_at": datetime.utcnow().isoformat()}, merge=True)
        data.update({flag: True, "bonus_sessions": bonus})
        return {"granted": True, "paid": bool(data.get("paid", False)),
                "free_used": int(data.get("free_used", 0)), "free_limit": _effective_limit(data)}

    return _txn(transaction)


def store_lead(uid: str, email: str) -> None:
    """Record a paywall email lead (owner follows up manually)."""
    from datetime import timezone
    now = datetime.now(timezone.utc)
    _client().collection("leads").add({
        "uid": uid,
        "email": email,
        "ts": now.isoformat(),
        "day": now.strftime("%Y-%m-%d"),
    })
