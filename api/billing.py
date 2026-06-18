"""Stripe billing: access check, subscription checkout, and webhook.

The paywall is OFF until STRIPE_SECRET_KEY is set, so the app runs fully free
until billing is configured.
"""
import os
import stripe
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from services.db import get_status, mark_paid, FREE_LIMIT

router = APIRouter(prefix="/api", tags=["billing"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
PRICE_ID = os.getenv("STRIPE_PRICE_ID", "")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
BASE_URL = os.getenv(
    "PUBLIC_BASE_URL", "https://tonetitor-346314536777.asia-southeast1.run.app"
).rstrip("/")


def _billing_on() -> bool:
    return bool(stripe.api_key)


class CheckoutRequest(BaseModel):
    uid: str


@router.get("/access")
async def access(uid: str = ""):
    """Access status for a uid. When billing is off, everyone is unlimited."""
    if not _billing_on():
        return {"billing_enabled": False, "paid": True, "free_used": 0, "free_limit": FREE_LIMIT}
    if not uid:
        raise HTTPException(status_code=400, detail="Missing uid")
    status = get_status(uid)
    status["billing_enabled"] = True
    return status


@router.post("/checkout")
async def create_checkout(req: CheckoutRequest):
    """Create a Stripe Checkout session for the $5/mo subscription."""
    if not _billing_on() or not PRICE_ID:
        raise HTTPException(status_code=503, detail="Billing not configured")
    if not req.uid:
        raise HTTPException(status_code=400, detail="Missing uid")
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": PRICE_ID, "quantity": 1}],
            client_reference_id=req.uid,
            success_url=f"{BASE_URL}/?paid=success",
            cancel_url=f"{BASE_URL}/?paid=cancel",
            allow_promotion_codes=True,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Stripe error: {e}")
    return {"url": session.url}


@router.post("/billing/webhook")
async def webhook(request: Request):
    """Stripe webhook — marks a uid paid on completed checkout."""
    if not WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Webhook not configured")
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig, WEBHOOK_SECRET)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        obj = event["data"]["object"]
        uid = obj.get("client_reference_id")
        if uid:
            mark_paid(uid, obj.get("customer"))

    return {"received": True}
