# ToneTutor — Distribution copy (ready to post)

Companion to `LAUNCH.md` (channel playbook), `SEED_LIST.md` (targets), `GROWTH_HSK.md` (strategy).
This file = the **card-curiosity + search-layer** copy built 2026-06-25. Strategy: **lead with the HSK score card / a result, not a product pitch** (curiosity > ads); be where high-intent learners *search/ask*, not just where they scroll.

> ⚠️ Posting reality: this dev box is **IP-banned from Reddit** and **小红书/IG-link/TikTok-link** edits are app-only — so Reddit, 小红书, IG/TikTok bio links are **the user's phone**. Claude runs X / IG-reel / TikTok / YouTube / SEO. See memory `feedback_claude_runs_promo`.

---

## 0. Live SEO landing pages (Layer 1 — search; link these everywhere)
- `/hsk-speaking-test` — "HSK speaking test"
- `/chinese-speaking-practice` — "Chinese speaking practice"
- `/practice-mandarin-tones` — "practice Mandarin tones"
- `/hsk-1-speaking-test` … `/hsk-6-speaking-test` — per-level
- `sitemap.xml` + `robots.txt` live. (Routes in `main.py`; pages generated in `seo_pages.py`.)

## 1. The viral unit — the HSK score card
Assets: `tools/make_hsk_card.py` → `hsk_card_h1..h6.png` (full HSK range) + `hsk_card_reveal.mp4` (level reveal). Post the card + "where do YOU land? drop your score 👇". Track **share_rate ≥ 0.15** (`/api/ev/stats`, token in Cloud Run env / private memory — NOT here).

---

## 2. Quora answers (Layer 1 — high intent; help first, disclose, tool = one option)
Search the question → pick a recent thread → paste & lightly tweak (don't paste identical text everywhere). Keep the disclosure + the honest caveat — that's what stops it reading as spam.

### Q: "How can I practice speaking Chinese if I don't have a language partner?"
Shadowing; record-and-compare; HelloTalk/Tandem/italki; AI conversation tools. *Full disclosure: I'm a native speaker + voice actor and built one (ToneTutor) — an AI that holds a real back-and-forth and grades tones/grammar as you go, free for a few sessions: tonetutor.tefusiang.com/chinese-speaking-practice . Honest caveat: AI grades the transcript, not raw pitch — treat as a guide. Combine 2–3 of the above.*

### Q: "How do I find out my HSK level — especially speaking?"
HSK = reading/listening; HSKK = oral. Speaking is the hard one to self-assess. Mock HSKK, italki assessment, or a quick AI estimate. *Full disclosure — I built a free 3-min spoken-HSK self-test (ToneTutor): estimates level 1–6 + weak points. An estimate from a short chat, not an official score: tonetutor.tefusiang.com/hsk-speaking-test*

### Q: "Best way to practice / fix my Mandarin tones?"
Don't drill in isolation — tones slip in connected speech. Minimal pairs → tones inside full sentences/conversation → record + compare with in-context feedback. *I built a tool that grades tones in live conversation (tonetutor.tefusiang.com/practice-mandarin-tones), so I'm biased — but the principle matters more than the tool: train tones in real speech, not isolation.*

### Q: "Is there an AI to practice Chinese / Mandarin conversation?" (variant)
Yes — a few exist now (Talkpal, etc.). *Disclosure: I built ToneTutor (native-speaker voice actor) — it focuses on grading your tones + grammar in a real conversation and gives an HSK speaking-level score card, which most don't. Free for 3 sessions: tonetutor.tefusiang.com . Try a couple and see which feedback style clicks for you.*

### Q: "How can I improve my spoken Chinese fast?" (variant)
Volume of *output* beats more input: talk daily even badly, get tone+grammar feedback in context, drill the specific mistakes that recur (not random vocab). *I built ToneTutor for exactly this loop (conversation → graded → drill your weak points): tonetutor.tefusiang.com/chinese-speaking-practice — free for a few sessions. But the habit (daily speaking + targeted correction) is what actually moves the needle.*

---

## 3. Discord / language-exchange (Layer 2 — peer tone, HSK is fine here)
Post in a resources/learning channel, **attach `hsk_card_h3.png`**, share your own card first.
> Hey all — native Mandarin speaker + voice actor here. Built a free **3-min spoken-Chinese self-test** (HSK scale): quick voice/text convo with an AI → estimates your spoken HSK level + weak spots + a shareable card. *[attach card]* Honest bit: it grades the transcript, not raw pitch — so it's a spoken-level **estimate**, not a tone analyzer. Since you all know your real level, could you run it and tell me if it's accurate? 🙏 Free, no signup: tonetutor.tefusiang.com/hsk-speaking-test

**Servers:** 中英交流 (76k, `discord.gg/c-e`) · r/ChineseLanguage (`discord.gg/chineselanguage`) · Migaku · Sinolands · GoEast · find more via DISBOARD `chinese-learning`/`mandarin`.

---

## 4. Resource-list outreach (Layer 3 — get listed; mostly contact FORMS)
Template saved in Gmail drafts ("[OUTREACH TEMPLATE]"). Paste into each blog's contact form, fill [Name]/[URL].
**Targets:** Clozemaster, LingoLegend, Hidden Dragon, Lingrow, Novli, Hacking Chinese, The Chairman's Bao.
**Pitch angle:** "a free AI Mandarin *speaking* test — fills the speaking/tone gap your list's apps skip; shareable HSK score card."
**Competitors to differentiate from:** Talkpal, Hidden Dragon (syllable pitch scoring), CPAIT, HanyuAce → ToneTutor = real conversation + tone+grammar grading + shareable HSK card + native voice actor.

---

## 5. High-intent niches (Layer 4 — user's accounts)
CSC / Chinese-Govt-Scholarship groups (HSK is the gate), HSK exam-prep groups, university Chinese departments. Hook: "申 CSC 前先免费测口语够不够 HSK4/5".
