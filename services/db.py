"""Firestore-backed user access store (paid status + free-session counting).

Only used when billing is enabled (STRIPE_SECRET_KEY set). Each user is keyed
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


def get_status(uid: str) -> dict:
    """Read-only access status for a uid (no mutation)."""
    snap = _client().collection("users").document(uid).get()
    data = snap.to_dict() if snap.exists else {}
    return {
        "paid": bool(data.get("paid", False)),
        "free_used": int(data.get("free_used", 0)),
        "free_limit": FREE_LIMIT,
    }


def mark_paid(uid: str, customer_id: str | None = None) -> None:
    """Mark a uid as a paying subscriber (called from the Stripe webhook)."""
    _client().collection("users").document(uid).set(
        {
            "paid": True,
            "stripe_customer": customer_id,
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
        if paid:
            return {"allowed": True, "paid": True, "free_used": free_used, "free_limit": FREE_LIMIT}
        if free_used >= FREE_LIMIT:
            return {"allowed": False, "paid": False, "free_used": free_used, "free_limit": FREE_LIMIT}
        new_used = free_used + 1
        txn.set(ref, {"free_used": new_used, "updated_at": datetime.utcnow().isoformat()}, merge=True)
        return {"allowed": True, "paid": False, "free_used": new_used, "free_limit": FREE_LIMIT}

    return _txn(transaction)
