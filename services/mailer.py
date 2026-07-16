"""Outbound email via the Gmail API (owner's account, gmail.send scope only).

Card-free: uses the project's existing OAuth desktop client with a refresh
token minted once locally. Mail is strictly best-effort — every failure is
swallowed after logging, because notifications must never break the API.

Config (Cloud Run env): GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET,
GMAIL_REFRESH_TOKEN, OWNER_EMAIL. Sending is OFF unless all are set.
"""
import base64
import os
from email.mime.text import MIMEText

import httpx

GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID", "")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET", "")
GMAIL_REFRESH_TOKEN = os.getenv("GMAIL_REFRESH_TOKEN", "")
OWNER_EMAIL = os.getenv("OWNER_EMAIL", "")
FROM_NAME = "John @ ToneTutor"

TOKEN_URL = "https://oauth2.googleapis.com/token"
SEND_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"


def mail_on() -> bool:
    return bool(GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET and GMAIL_REFRESH_TOKEN)


async def _access_token(client: httpx.AsyncClient) -> str:
    r = await client.post(TOKEN_URL, data={
        "client_id": GMAIL_CLIENT_ID,
        "client_secret": GMAIL_CLIENT_SECRET,
        "refresh_token": GMAIL_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    })
    r.raise_for_status()
    return r.json()["access_token"]


async def send_email(to: str, subject: str, body: str, reply_to: str = "") -> bool:
    """Send a plain-text email. Returns False (never raises) on any failure."""
    if not mail_on() or not to:
        return False
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["To"] = to
        msg["From"] = FROM_NAME
        msg["Subject"] = subject
        if reply_to:
            msg["Reply-To"] = reply_to
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        async with httpx.AsyncClient(timeout=15) as client:
            token = await _access_token(client)
            r = await client.post(
                SEND_URL,
                headers={"Authorization": f"Bearer {token}"},
                json={"raw": raw},
            )
        if r.status_code >= 300:
            print(f"[mailer] send failed {r.status_code}: {r.text[:200]}")
            return False
        return True
    except Exception as e:
        print(f"[mailer] send error: {e}")
        return False


async def notify_owner(subject: str, body: str, reply_to: str = "") -> bool:
    return await send_email(OWNER_EMAIL, subject, body, reply_to=reply_to)
