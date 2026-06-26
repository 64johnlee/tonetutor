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

## 2b. Quora WARM-UP answers (NO link — post 1–2 of these FIRST)
A brand-new Quora account that drops links gets collapsed. Post 1–2 of these genuine, zero-promo answers first (set credential = "Native Mandarin speaker & voice actor"), then the §2 tool-mention answers over the next days. Search each question (or a close variant) → Answer → paste → tweak a word or two. Pace: 1–2/day.

**Q: "Why are Mandarin tones so hard / how do I get them right?"** → Tones are hard to *produce consistently* under load, not to hear. (1) Third tone is usually a low dip, not a full V. (2) Learn tone sandhi as a habit (3+3→2+3; 不/一 shifts). (3) Practise in 2-syllable chunks (朋友, 谢谢), not single characters. (4) Over-exaggerate at first — learners always under-do tones. Record yourself to catch flat tones.

**Q: "When do I use 了 (le)?"** → Not a past-tense marker (Chinese has no tense). Two jobs: (1) completed action after the verb — 我吃了饭; (2) change of state, sentence-final — 下雨了 / 我知道了. Don't sprinkle on every past sentence (昨天我很忙 = no 了) or habits (我每天喝咖啡 = no 了). Ask: did something *complete* or *change*? If neither, no 了.

**Q: "Best way to learn/remember Chinese characters?"** → Don't memorise stroke-by-stroke as pictures. Characters = reusable components. (1) Learn common radicals (氵木心口…); most characters decode (妈=女+马sound, 河=氵+可sound). (2) Group by shared component (请/清/情/晴 share 青). (3) SRS the high-frequency ~1,000 first. (4) Read a lot slightly below level. It gets easier as you go, not harder.

**Q: "Difference between 的 / 得 / 地?"** → All *de*, three jobs, sort by position: 的 before a NOUN (我的书, 红色的车); 得 after a VERB before a degree/result complement (说得很好, 跑得快); 地 before a VERB for manner (慢慢地走, 认真地学). Test: noun after→的; "how well" after verb→得; "in what manner" before verb→地. (Casual texting: many natives just use 的 for all.)

**Q: "How do measure words work / 个 vs others?"** → Number + MEASURE WORD + noun (三本书). 个 is the universal default — use it if you blank, always understood. Worth learning early: 本(books) 张(flat: paper/tables/tickets) 只(animals/one of a pair) 条(long thin: fish/roads/trousers) 杯·瓶(drinks) 件(clothing/matters). Best tip: learn the measure word *with* the noun as a chunk (一张桌子), not separately.

**Q: "How do I improve my Chinese listening?"** → It's speed + connected speech, not vocab. (1) Intensive > extensive early — replay one short clip 5–10× until you catch it all. (2) Bilingual subs → Chinese-only → none, same material. (3) Shadow (repeat a beat behind). (4) Listen *below* your reading level. (5) Make peace with ambiguity — get the gist, keep going. Graded podcasts/slowed dialogues first.

**Posting order:** warm-up (no link) → "practice speaking by myself" (§2, strongest fit) → rest of §2 over following days.

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

---

## 6. OWNED Discord community — "ToneTutor — Mandarin HSK" (no gatekeeper)
**Invite: `discord.gg/zcjwSfDZ`** (created 2026-06-26, owner = john). Channels: `#general` · `📢 announcements` · `🎯 hsk-scores` (post your card!) · `🗣️ speaking-tips` · `🐛 feedback`.
**Linked from:** all 9 SEO pages + the `/hsk-speaking-test` landing footer + the app's **end-of-test/score-card screen** ("💬 Compare scores… join our Discord"). Fill it from owned traffic.
**Why it matters:** UNLIKE Quora (deletes self-promo) or 中英交流 (permission-gated), this is an owned channel that **can't be deleted or gatekept**.
**Bot + MCP (later, at ~10+ members):** wire `barryyip0625/mcp-discord` with a bot token → auto "HSK card of the day" in #hsk-scores + welcome bot. Bot is a separate identity (can't post as john in OTHER servers — that's by Discord design).

### 6b. #speaking-tips drip queue (paste one every 2–3 days, KL peak — keeps the channel warm)
**Tip #1 (third tone = low dip, not a full V) — POSTED 2026-06-26.** Drip the rest in order:

**Tip #2 — 不 and 一 secretly change tone**
> 不 (bù) and 一 (yī) shift tone by what follows, and natives do it automatically: 不→**bú** before a 4th tone (不是 *bú shì*, 不要 *bú yào*); 一→**yí** before 4th (一个 *yí gè*), **yì** before 1st/2nd/3rd (一天 *yì tiān*). Drill in whole phrases, not as rules. Did anyone else not know 一 changes tone? 👀

**Tip #3 — Not every syllable gets a full tone (轻声)**
> The 2nd syllable in 妈妈, 谢谢, 朋友, 东西 is often **neutral** — light, short, no tone. Over-pronouncing it = robotic. Say 谢谢 with both hard 4th tones, then with the 2nd soft — hear it? What word have you been over-toning? 👇

**Tip #4 — Record + compare (the fastest fix nobody likes)**
> Record yourself saying a sentence, then play a native version of the same line and compare. You'll catch flat tones you *swear* you nailed. Pleco/YouTube/ToneTutor audio = your native reference. Anyone brave enough to post a clip? 🎤

**Tip #5 — Slow down to lock tones, then speed up**
> Rushing flattens tones into mush. Speak **slightly slower than feels natural** while locking tones in — speed returns once they're automatic. Slow + correct beats fast + wrong. What's harder for you: tones, or natural speed? 👇

(Refill the queue when it runs low — same source as the Quora warm-ups: tones / 了 / characters / 的得地 / measure words / listening.)

---

## 7. Video drip queue (built 2026-06-26 — post 1/day at KL peak)
1080×1920 shorts built via `python3 tools/build_short.py <a|b|c>` → MP4s in `C:\Users\User\` (brand dark+red, YaHei font renders Chinese). Post one per day in order via `post_tiktok.py` + `post_x_video.py` + `post_ig_reel.py`. NEVER post at midnight KL.

**A — `hsk_v_canpass_hsk6.mp4`** (10s, "Can you pass HSK 6 speaking?")
> Could you actually pass HSK 6 *speaking*? 99% can't 😅 An AI rates your spoken Mandarin in 3 min — find your real level free 🎯 link in IG bio @johnlee007 #HSK #HSK6 #LearnChinese #Mandarin #中文 #chineselanguage

**B — `hsk_v_tip_thirdtone.mp4`** (12s, third-tone native tip)
> Native-speaker tip most courses get wrong: the 3rd tone is a LOW DIP, not a fall-rise "V" 🤯 你好 = ní-hǎo (first syllable low & short). Free HSK speaking test + more tips 🎯 link in IG bio @johnlee007 #LearnChinese #Mandarin #中文 #chinesetones #HSK #语言学习

**C — `hsk_v_which_246.mp4`** (12s, "Which one are YOU?" HSK 2/4/6)
> An AI pegs your spoken Mandarin in 3 min — which one are YOU? HSK 2, 4, or 6? Drop your level 👇 free test, link in IG bio @johnlee007 #HSK #LearnChinese #Mandarin #中文 #fyp #chinesetok

Extend: add a spec to `tools/build_short.py` SPECS dict + rebuild.
