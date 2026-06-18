# ToneTutor — Project Guide for Claude Code

AI Mandarin conversation tutor. Users pick a scenario + HSK level (1–6) and chat
with "Lin Wei" (AI native speaker); each reply is graded for tones/grammar with
pinyin + voice, ending in a session summary.

**This is the XPRIZE "Build with Gemini" entry** — category *Education & Human
Potential*, submission deadline **Aug 17, 2026**. Judged on **real revenue +
real users + AI-native operations** (not a prototype) — so paying customers and
revenue evidence matter, not just features.

- **Live app:** https://tonetitor-346314536777.asia-southeast1.run.app
- **Custom domain:** https://tonetutor.tefusiang.com (CNAME → ghs.googlehosted.com; SSL via Cloud Run)
- **Public repo:** https://github.com/64johnlee/tonetutor

## Stack & layout
- **Backend:** FastAPI on Cloud Run. Entry `main.py` mounts routers from `api/`.
- **LLM:** Gemini 2.5 Flash via Vertex AI (ADC, no API key) — `services/gemini.py`
- **Speech:** Google Cloud STT (`cmn-Hans-CN`, **LINEAR16**) `api/transcribe.py`; TTS (`cmn-CN-Chirp3-HD-Aoede`) `api/tts.py`
- **Frontend:** single-page `static/index.html` (vanilla JS; all CSS/JS inline)
- **Sessions:** in-memory dict in `api/store.py` (conversation state)
- **Billing/users:** Firestore `users/{uid}` via `services/db.py`

## Deploy
```bash
cd /home/user/tonetitor && gcloud run deploy tonetitor --source . --region asia-southeast1
```
- GCP project `disco-module-487411-m0` (project number 346314536777), region `asia-southeast1`.
- Secrets live in `.env` (gitignored) + Cloud Run env vars — **never commit secrets**. `.env.example` documents the keys.

## Billing — Lemon Squeezy (Merchant of Record)
$5/mo subscription, **3 free sessions** then paywall. NOT Stripe (owner is a China
national on MM2H with no own company/NRIC — LS as MoR needs none and pays to PayPal).

- `api/billing.py` — `/api/access`, `/api/checkout` (LS checkout API), `/api/billing/webhook` (HMAC-SHA256, `X-Signature`)
- `api/session.py` — gates `/start`: unpaid + 3 used → HTTP **402**
- **Paywall is OFF unless `LEMON_API_KEY` is set** (`BILLING_ON`), so the app is fully free until configured. Same guard means the code is always safe to deploy.
- Frontend is **processor-agnostic** (calls `/api/checkout` + `/api/access`; anonymous `uid` in localStorage; paywall modal on 402).
- Config (Cloud Run env): `LEMON_API_KEY`, `LEMON_STORE_ID`, `LEMON_VARIANT_ID`, `LEMON_WEBHOOK_SECRET`, `PUBLIC_BASE_URL`.
- LS refs: store `411198` (USD), variant `1808129` ($5/mo), webhook `111752`.
- Firestore `users/{uid}`: `paid:bool`, `free_used:int`, `provider_ref:str|null`, `updated_at:ISO8601`. Cloud Run SA `346314536777-compute@developer` has `roles/datastore.user`.

## Gotchas / conventions
- **Voice input must be LINEAR16, not webm** — iOS Safari/Chrome can't record webm. Frontend captures raw PCM via Web Audio (`createScriptProcessor`/`_encodePCM16`) and sends `sample_rate`; backend STT = LINEAR16 mono. Don't reintroduce MediaRecorder/webm.
- Mic JS is inline in `static/index.html` (`startListening`/`stopListening`); 60s hard auto-stop cap.
- Root route sets `Cache-Control: no-store`; HTML also has a no-store meta — expect aggressive cache-busting.
- Match the existing compact inline style in `index.html` (underscore-prefixed JS privates).

## Open items (as of 2026-06-18)
- Stripe-backed **identity verification** (via LS) — In Review; needs **Passport** (not MyKad). Required before live (non-test) payments.
- Custom-domain **SSL** provisioning (waiting on Google).
- Get first paying users (launch to r/ChineseLanguage) → revenue evidence for XPRIZE.
- Owner must confirm online income is compatible with **MM2H** visa before taking real payments.
