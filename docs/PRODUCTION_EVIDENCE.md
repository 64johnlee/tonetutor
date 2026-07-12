# ToneTutor — Production Evidence (XPRIZE "Build with Gemini")

Last updated: 2026-07-13. Everything below is live and independently verifiable.

## 1. The product is live and serving users

- **App:** https://tonetutor.tefusiang.com (Cloud Run, `asia-southeast1`, scale-to-zero)
- **Live revision at time of writing:** `tonetitor-00069-z4x` (69 production revisions shipped since mid-June 2026 — near-daily AI-executed deploys)
- **Health:** `GET /health` returns 200 on the live service.

## 2. AI executes the product loop in production

Every session is AI end-to-end — there is no human tutor:

- **Vertex AI Gemini 2.5 Flash / Flash-Lite** — conversation, tone-error explanation, HSK-level assessment, drill generation (`services/gemini.py`; latency-based model routing in `_get_model`)
- **Cloud Speech-to-Text** — learner audio → transcript (`api/transcribe.py`, LINEAR16 PCM with an iOS Web-Audio capture path)
- **Cloud Text-to-Speech (Chirp3-HD)** — the tutor's voice (`/api/tts`)
- **Firestore** — users, subscriptions, first-party analytics events

## 3. First-party analytics funnel (read daily by the operating agent)

Live endpoint (admin-tokened): `GET /api/ev/stats`. Snapshot 2026-07-12 (14-day window):

```json
{"counts": {"test_started": 9, "test_completed": 5, "card_rendered": 5,
            "paywall_hit": 8, "subscribe": 0},
 "rates": {"completion_rate": 0.571}}
```

Growth decisions trace to these numbers (see §5).

## 4. Real billing, live since 2026-06-24

- Lemon Squeezy (merchant of record), US$5/month, 3 free sessions then paywall
- Verified end-to-end on the live store (not test mode): checkout → `POST /api/billing/webhook` (`subscription_created` + `order_created`, HMAC-verified, both 200) → Firestore `users/{uid}` → `GET /api/access` returns `{"paid": true}`
- Billing code: `api/billing.py`, gate in `api/session.py`

## 5. AI runs marketing in production (continuously)

The operating agent produces, schedules and answers all acquisition content:

- **Channel:** https://youtube.com/@tonetutor — 35 videos, 100% AI-produced (hooks written from a mined competitor-pain database of 2,734 App Store reviews; rendered with Python/ffmpeg; voiced with Cloud TTS Chirp3-HD)
- **Scheduled queue at time of writing (YouTube Data API `status.publishAt`):**
  - `fJ6VpenCk5s` → 2026-07-13T11:00Z
  - `A_aiSRJD47c` → 2026-07-14T01:00Z
  - `LlIhqV8Or9I` → 2026-07-14T11:00Z
  - `4KrTu_ilvwk` → 2026-07-15T01:00Z
- **A real strategy decision made from data:** grammar-lecture videos flopped (2–8 views: `l5AvSTmL3M8`, `ztQPBDhZxBM`) while embarrassment-stakes hooks won (304–415 views: `Mcr8vaPaMnk`, `zSvduGfY58E`, `liG9iy2n7rY`); the agent diagnosed this from view/funnel data and reset the content format. View counts are publicly verifiable on the channel.

## 6. Demo video

3-minute walkthrough of the AI operating in production: https://www.youtube.com/watch?v=G7IxLtNiKI0
