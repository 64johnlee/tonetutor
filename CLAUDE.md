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
- LS refs: store `411198` (USD), **live variant `1832799`** ($5/mo) — ⚠️ test-mode variant `1808129` does NOT carry over to live (LS keeps test & live products separate; a new live product was created), webhook `111752`.
- Firestore `users/{uid}`: `paid:bool`, `free_used:int`, `provider_ref:str|null`, `updated_at:ISO8601`. Cloud Run SA `346314536777-compute@developer` has `roles/datastore.user`.

## Gotchas / conventions
- **Voice input must be LINEAR16, not webm** — iOS Safari/Chrome can't record webm. Frontend captures raw PCM via Web Audio (`createScriptProcessor`/`_encodePCM16`) and sends `sample_rate`; backend STT = LINEAR16 mono. Don't reintroduce MediaRecorder/webm.
- Mic JS is inline in `static/index.html` (`startListening`/`stopListening`); 60s hard auto-stop cap.
- Root route sets `Cache-Control: no-store`; HTML also has a no-store meta — expect aggressive cache-busting.
- Match the existing compact inline style in `index.html` (underscore-prefixed JS privates).

## Promotion & launch plan (HSK reach) — added 2026-06-24
Verbatim per-channel post copy lives in `LAUNCH.md`; target list in `SEED_LIST.md`; strategy in `GROWTH_HSK.md`. This is the synthesized blast plan.

- **🎯 PRIMARY MODE (2026-06-25 pivot): card-curiosity, NOT product-push.** Lead every post with the **HSK score-card itself** + a "where do YOU land? drop your score 👇" hook — a personal RESULT triggers curiosity/comparison (Spotify-Wrapped effect); a product pitch triggers ad-blindness. Dial DOWN the broadcast blast, dial UP a steady drip of card posts + reply-bait. Assets: `tools/make_hsk_card.py` renders full-res cards via the app's `renderScoreCard()` → `hsk_card_h2/h3/h4.png`; `hsk_card_reveal.mp4` = the HSK 2→3→4 reveal video posted to X/IG/TikTok 2026-06-25. The loop: see card → test → get your card (URL baked in) → share → repeat.
- **Viral engine:** the shareable **HSK score-card** is the unit. Gate everything on **share_rate ≥ 0.15** (`GET /api/ev/stats?token=<EV_STATS_TOKEN>` — token is the Cloud Run `EV_STATS_TOKEN` env, NOT committed here); below it, fix the card before scaling.
- **Golden rule (ban-vs-win):** ONE tailored post per community, ~1–2 communities/day, reply to every comment same-day. Match the hook to THEIR identity (never say "HSK" to travelers / C-drama fans). **Reddit can't be posted from this box (IP-banned — owner posts from phone);** Claude can run X / IG / TikTok / YT Shorts.

**Channel tiers (highest-intent first):**
1. **Reddit** — r/HSK, r/ChineseLanguage, r/LearnChinese, r/ChineseLanguageLearning, r/Chinese · **Discord** — 中英交流 (76k), Migaku, GoEast (find via DISBOARD `chinese-learning`/`mandarin`).
2. **High-intent niches 🔥 (pay + share):** CSC / Chinese-Govt-Scholarship applicants (FB + Telegram "CSC Scholarship"; China Admissions / CUCAS); China-bound jobseekers (LinkedIn).
3. **Adjacent pools competitors ignore:** China travel (r/travelchina, r/China, r/chinalife — hook "how much can you actually speak", NEVER "HSK"); C-drama/donghua/C-pop (r/CDrama, r/donghua, Viki); heritage learners (r/ABCDesis, r/Cantonese — "understand but can't speak").
4. **Telegram** (@hsk123456, @ChineseLanguageSelfStudy, the 620-group directory — RU / Central Asia / SEA / Africa) + **FB groups** ("HSK Test Prep", "Learn Chinese + country").
5. **Creators (micro > mega):** DM ~20 micro-creators 10k–200k on TikTok/IG/YT (`#HSK3 #HSK4 #chinesetones`); long-shots: Chinese Zero to Hero, Mandarin Corner, Yoyo Chinese, GoEast.
6. **Owned content (Claude can run):** Shorts (TikTok/IG/YT) of the demo clip (`#LearnChinese #Mandarin #HSK #对外汉语`); X thread @johnlee007; 小红书 (link in bio, 真实分享 tone); helpful YouTube comments. Demo clip = youtube.com/watch?v=6IE9dxBh45o.
7. **Authority / launch:** Show HN (build karma first), Product Hunt (12:01 PT), Hacking Chinese, Chinese-forums.com.
8. **Localization (after RU/ID prove lift):** Russian (CIS Telegram, weak competition) → Indonesian / Vietnamese.

**7-day sequence:** D1 r/HSK → D2 r/ChineseLanguage + X thread → D3 join 5 Telegram + 3 FB (lurk, post own card) → D4 DM 10 micro-creators + 1 Discord → D5 r/LearnChinese + Shorts → D6–7 CSC groups + travel/C-drama (re-hooked). Reply to every comment same-day; that drives the algorithm + trust.

## Open items (as of 2026-06-24)
- **Shipped 2026-06-24:** "Ask your tutor" Gemini copilot — `POST /api/copilot` (`api/copilot.py`, `copilot_turn` in `services/gemini.py`) answers learner questions grounded in the live session (level + history + accumulated tone `weak_points`); returns English explanation, pinyin examples, and optional `drill_focus`. Frontend 🎓 Tutor bottom-sheet with tap-to-speak examples + "Practise this →" (seeds a focused session via existing `focus` pathway). Live on revision `tonetitor-00039-kn9`.
- ✅ **LIVE for real payments since 2026-06-24** — LS store activated (passport verification cleared), test mode OFF, full paid loop verified end-to-end (live checkout `test_mode:false` → webhook 200 → `/api/access` `paid:true`). Cloud Run env uses the live API key + live `LEMON_WEBHOOK_SECRET` + live variant `1832799`.
- Custom-domain **SSL** provisioning (waiting on Google).
- Get first paying users (launch to r/ChineseLanguage) → revenue evidence for XPRIZE.
- Owner must confirm online income is compatible with **MM2H** visa before taking real payments.
