"""Lemon Squeezy billing: access check, subscription checkout, and webhook.

Lemon Squeezy is a Merchant of Record — no company or local entity needed, it
handles tax and pays out (e.g. via PayPal). The paywall is OFF until
LEMON_API_KEY is set, so the app runs fully free until billing is configured.
"""
import os
import json
import hmac
import hashlib
import httpx
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from services.db import get_status, mark_paid, FREE_LIMIT

router = APIRouter(prefix="/api", tags=["billing"])

LEMON_API_KEY = os.getenv("LEMON_API_KEY", "")
VIP_TOKEN = os.getenv("VIP_TOKEN", "")
LEMON_STORE_ID = os.getenv("LEMON_STORE_ID", "")
LEMON_VARIANT_ID = os.getenv("LEMON_VARIANT_ID", "")
LEMON_WEBHOOK_SECRET = os.getenv("LEMON_WEBHOOK_SECRET", "")
BASE_URL = os.getenv(
    "PUBLIC_BASE_URL", "https://tonetitor-346314536777.asia-southeast1.run.app"
).rstrip("/")

CHECKOUT_API = "https://api.lemonsqueezy.com/v1/checkouts"

# Webhook events that grant access (subscription purchase confirmed)
UNLOCK_EVENTS = {"subscription_created", "order_created"}


def _billing_on() -> bool:
    return bool(LEMON_API_KEY)


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


class VipRequest(BaseModel):
    uid: str
    token: str


@router.post("/access/vip")
async def vip_unlock(req: VipRequest):
    """Owner/testing bypass: visiting /?vip=<VIP_TOKEN> marks that device's uid
    paid (provider_ref 'vip'), skipping the free-session limit. Disabled unless
    the VIP_TOKEN env var is set."""
    if not VIP_TOKEN or not req.token or not hmac.compare_digest(req.token, VIP_TOKEN):
        raise HTTPException(status_code=403, detail="Invalid token")
    if not req.uid:
        raise HTTPException(status_code=400, detail="Missing uid")
    mark_paid(req.uid, "vip")
    return {"ok": True, "paid": True}


@router.post("/checkout")
async def create_checkout(req: CheckoutRequest):
    """Create a Lemon Squeezy hosted checkout for the $5/mo subscription."""
    if not _billing_on() or not LEMON_STORE_ID or not LEMON_VARIANT_ID:
        raise HTTPException(status_code=503, detail="Billing not configured")
    if not req.uid:
        raise HTTPException(status_code=400, detail="Missing uid")
    body = {
        "data": {
            "type": "checkouts",
            "attributes": {
                "checkout_data": {"custom": {"uid": req.uid}},
                "product_options": {"redirect_url": f"{BASE_URL}/?paid=success"},
            },
            "relationships": {
                "store": {"data": {"type": "stores", "id": str(LEMON_STORE_ID)}},
                "variant": {"data": {"type": "variants", "id": str(LEMON_VARIANT_ID)}},
            },
        }
    }
    headers = {
        "Authorization": f"Bearer {LEMON_API_KEY}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
    }
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(CHECKOUT_API, headers=headers, json=body)
        if r.status_code >= 300:
            raise HTTPException(status_code=502, detail=f"Lemon Squeezy error: {r.text}")
        url = r.json()["data"]["attributes"]["url"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Checkout error: {e}")
    return {"url": url}


@router.post("/billing/webhook")
async def webhook(request: Request):
    """Lemon Squeezy webhook — marks a uid paid on confirmed purchase.

    Signature: HMAC-SHA256 hex of the raw body, keyed by the signing secret,
    sent in the X-Signature header.
    """
    if not LEMON_WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Webhook not configured")
    payload = await request.body()
    sig = request.headers.get("x-signature", "")
    expected = hmac.new(LEMON_WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        raise HTTPException(status_code=400, detail="Invalid signature")

    try:
        event = json.loads(payload)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload")

    meta = event.get("meta", {})
    if meta.get("event_name") in UNLOCK_EVENTS:
        uid = (meta.get("custom_data") or {}).get("uid")
        if uid:
            mark_paid(uid, event.get("data", {}).get("id"))

    return {"received": True}
