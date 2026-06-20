# ToneTutor Launch Playbook

**URL:** https://tonetutor.tefusiang.com
**One-liner:** Practice real Mandarin conversations with an AI native speaker that grades your tones in real time.

## Pre-launch checklist (do FIRST — don't launch before these)
- [ ] Lemon Squeezy store **activated** (identity verified) so it takes real payments
- [ ] Walk the full flow once in test mode (3 free → paywall → checkout → unlock)
- [ ] A feedback channel ready (reply email or a simple form)
- [ ] Decide a launch day you can sit at the keyboard for ~3 hrs to reply to comments

## Golden rules (this is what separates a win from a ban)
- **One genuine post per community.** Tailor each — never copy-paste the same text everywhere.
- **Lead with "I built this, want feedback"**, not "buy my product."
- **Reply to every comment fast** on launch day — engagement drives the algorithm + trust.
- **Your moat is YOU**: a bilingual native Mandarin speaker + voice actor. Say it everywhere.
- Don't post to all channels the same day — stagger so you can engage with each.

---

## Reddit — r/ChineseLanguage (post FIRST, tailor a separate one for r/LearnChinese later)
*(⚠️ Check the sub rules + sidebar before posting: r/ChineseLanguage restricts self-promo — you may need a "Resources" flair, or to post in a weekly thread. Comment on a few threads in the days before so you're not a drive-by account. One tailored post per sub — never paste the same text in both.)*

**Title:** I'm a Mandarin voice actor — I built a tool that grades your tones in live conversation. Come tell me where it's wrong.

**Body:**
> I'm a native Mandarin speaker and voice actor. The thing that always bugged me: apps drill vocab and isolated tone pairs, but nobody corrects your **tones in an actual back-and-forth conversation** — which is exactly where learners plateau and start sounding "off."
>
> So I built a thing to scratch that itch. You pick a scenario (ordering food, a job interview, travel) and your HSK level, then have a real conversation — speak or type — and every reply gets graded on **tone + grammar**, with pinyin and audio, plus a summary of what to drill next.
>
> Here's my actual ask: **I don't trust it yet, and you shouldn't either.** Automated tone grading is hard, and this community is the best stress-test on the planet. Go throw deliberately wrong tones at it, try edge cases, and tell me where the feedback is wrong or unhelpful. That's the part I need to get right before I'd ever claim it works.
>
> Free for 3 full conversations (there's a paid tier after, but I'm genuinely not here to sell — I want the accuracy verdict): https://tonetutor.tefusiang.com
>
> Solo build, happy to explain how the tone grading works under the hood.

---

## Hacker News — Show HN
*(⚠️ Per memory: HN was rate-limiting Show HNs from your new account — build a little comment karma first. HN rewards technical candor and punishes hype: no "AI-powered", say the model. Post a weekday morning ET.)*

**Title:** Show HN: A Mandarin tutor that grades your tones in live conversation

**Body:**
> I'm a native Mandarin speaker and voice actor. Every app I tried drills flashcards and isolated tone pairs, but none correct your tones in an actual conversation — which is exactly where learners plateau and sound "off."
>
> ToneTutor drops you into a scenario (ordering food, a job interview), you converse by voice or text with Gemini playing a native speaker, and each reply is scored for tone + grammar with pinyin and audio, plus a summary of what to drill.
>
> The hard part — and the part I'm least sure of — is the tone grading itself. Right now your speech hits Google Cloud STT (cmn-Hans-CN) for a transcript, then Gemini 2.5 Flash grades that transcript for tone + grammar and writes Lin Wei's reply in a single structured-JSON call. The honest limitation: it grades the *transcribed text*, not the raw pitch contour — so if you flub a tone but STT still maps it to the word you meant, the error can slip past. Extracting the actual F0/pitch contour and scoring it against the target tone shape is the obvious next step, and the part I haven't cracked reliably yet — ideas very welcome. I'd genuinely like HN to poke holes in it.
>
> Stack: FastAPI on Cloud Run, Gemini 2.5 Flash, Google STT/TTS. Free for 3 full conversations.
>
> https://tonetutor.tefusiang.com — feedback on tone-grading accuracy especially welcome.

---

## Product Hunt
*(⚠️ Schedule for 12:01am PT — PH days reset on Pacific time and you want a full day to gather upvotes. Have the demo video/GIF ready; PH listings live or die on the thumbnail + first comment. Line up a few people to genuinely try it early.)*
- **Name:** ToneTutor
- **Tagline (≤60 chars):** Mandarin conversation practice that grades your tones
- **Description:** Hold real Mandarin conversations with an AI native speaker. Pick a scenario and your HSK level, speak or type, and get instant tone + grammar feedback with pinyin and audio — plus a summary of what to drill next. Built by a native-speaker voice actor.
- **First comment (maker):** Hi PH 👋 I'm a bilingual Mandarin speaker and voice actor. Tones are where learners struggle most, yet almost every app ignores them in *live* conversation — so I built ToneTutor to scratch that itch. Honest ask: automated tone grading is hard and I'm still proving out the accuracy, so please **try to break it** — throw deliberately wrong tones at it and tell me where the feedback is off. Free for 3 full conversations. That accuracy verdict is the whole thing I'm obsessing over.

---

## 小红书 / Bilibili / RED (leverage your native-speaker angle)
*(⚠️ 小红书 suppresses posts with external links in the body — put the URL in your profile 简介 and write “主页链接” in the caption, or share it only when people comment/DM. Lead with a real personal-share tone, not an ad — RED's algorithm favors 真实分享.)*

**Caption (zh):**
> 母语普通话+配音演员,自己动手做了个 AI 中文口语练习工具。选场景(点餐、面试、旅游)和 HSK 等级,跟 AI 真实对话,每句话都会给你的**声调**和语法打分,带拼音和真人发音,练完还有错误总结。
>
> 说实话,声调评分这块我自己还没完全放心,所以特别想请大家来「找茬」:故意说错声调、上点难度,看看它判得准不准,哪里不对一定告诉我🙏 前 3 次免费。
>
> (链接放主页简介里了~) #学中文 #普通话 #对外汉语 #AI工具 #语言学习

---

## 🇷🇺 Russian (first localization — see GROWTH_HSK.md §6)
*(Russian-speaking HSK learners are huge in Central Asia / CIS — dense Telegram groups, weak competition. Use the HSK version in HSK/CSC communities; use the travel version in China-travel communities. Hook matches their identity — never say "HSK" to travelers.)*

### r/HSK / HSK & CSC communities
**Title:** Носитель языка + актёр озвучки: сделал бесплатный тест разговорного китайского. Проверьте свой уровень HSK — и скажите, где он ошибается.
*(EN: Native speaker + voice actor — I made a free spoken-Chinese test. Check your HSK level, and tell me where it's wrong.)*

**One-liner:** Узнайте свой реальный уровень разговорного HSK за 3 минуты — бесплатно, результат сразу.

**Body:**
> Я носитель китайского и актёр озвучки. Почти все приложения гоняют карточки, но не проверяют, как ты реально говоришь — а именно там все застревают. Сделал тест: поговорите пару минут с ИИ — получите оценку уровня HSK, сильные стороны и над чем работать.
>
> Честно: автооценка произношения и тонов — сложная штука, я ей пока не до конца доверяю. Поэтому прошу: попробуйте её **сломать** (специально наделайте ошибок) и скажите, где она врёт. Бесплатно, 3 минуты: tonetutor.tefusiang.com

### China-travel communities (NO "HSK" — match their identity)
**Hook:** Скоро поездка в Китай? Проверьте за 3 минуты, сколько вы реально сможете сказать по-китайски — бесплатный тест: tonetutor.tefusiang.com
*(EN: Going to China soon? Test in 3 min how much Chinese you can actually speak — free.)*

**Shorter (comments):** Едете в Китай? Узнайте, на каком уровне ваш разговорный китайский — бесплатно, 3 минуты.

### C-drama / donghua fan communities (use "дорамы" — the fan word; NO "HSK")
**Hook:** Смотрите китайские дорамы? А насколько хорошо вы реально говорите по-китайски? Узнайте за 3 минуты — бесплатно: tonetutor.tefusiang.com
*(EN: Watch C-dramas? But how well can you actually speak Chinese? Find out in 3 min — free.)*

**Shorter (comments):** Фанат(ка) китайских дорам? Узнай, на каком уровне твой разговорный китайский — бесплатно, 3 минуты.

> ⚠️ I can't verify Russian myself — have a native speaker eyeball it before a big push, or post once and watch the reception.

---

## Demo clip (15–30s) — reused for X, Product Hunt, TikTok/IG/YT Shorts, and XPRIZE B-roll

**Format:** vertical 9:16, screen-recording of the live app, ~30s master + a 15s trim.
**Mute-first:** burn in captions — assume no sound. Real spoken Mandarin audio is your moat (native voice actor), so DO keep a clean audio track for sound-on viewers.
**The one rule:** the tone-correction moment (a *wrong* tone caught + fixed) is the whole video — get to it fast and make it unmissable (zoom + a soft "ding" + color flip red→green).

### 30s master — shot by shot
| Time | Visual | Burned-in caption | Audio |
|------|--------|-------------------|-------|
| 0:00–0:02 | Cold open on the chat UI, big text slams in | **"Your vocab is fine. Your tones aren't."** | beat / whoosh |
| 0:02–0:05 | Tap scenario **"Restaurant"** + **"HSK 2"** | "Pick a scene + your level." | tap clicks |
| 0:05–0:08 | Tap mic, speak a line (waveform animates) — **deliberately flub one tone** | "Just talk." | your real voice saying the line |
| 0:08–0:14 | **MONEY SHOT** — reply card grades it; one tone flagged **red** with the correction + pinyin. Zoom in. | **"It caught the one tone I got wrong."** | soft "ding" |
| 0:14–0:19 | Lin Wei replies (speaker icon pulsing, plays audio); you redo the line, grade flips **green** | "Fix it. Hear it. Lock it in." | AI reply audio + success chime |
| 0:19–0:24 | Session-summary card slides up (mistakes + what to drill) | "End-of-session report card." | light swell |
| 0:24–0:30 | END CARD: logo + URL | **"Practice free → tonetutor.tefusiang.com"** · small: "built by a native-speaker voice actor" | music resolves |

### 15s trim (for X tweet-1 + fast Shorts)
0:00–0:02 hook → **0:02–0:08 the money shot** (mic → red tone caught, this is the star) → 0:08–0:11 green fix → 0:11–0:15 end card. Drop the scenario-pick and summary beats.

**Production notes:** record at the device's full res then crop to 9:16; hide any debug/URL bars; do 2–3 takes of the spoken line so the flub-then-fix reads clearly; keep total cuts snappy (nothing longer than ~3s on screen).

**Caption (social):** POV: an AI finally tells you *which* Mandarin tone you got wrong — in a real conversation, so you can actually fix it. Free to try 👉 tonetutor.tefusiang.com #LearnChinese #Mandarin #languagelearning #HSK #对外汉语

---

## University Chinese departments — outreach email
**Subject:** Free AI Mandarin conversation tool for your students

**Body:**
> Dear Professor [Name],
>
> I'm a native Mandarin speaker and voice actor. I've built **ToneTutor**, a free web tool where students practice real Mandarin conversations with an AI native speaker that grades their tones and grammar in real time (with pinyin and audio).
>
> It's aimed at exactly the gap your students hit between class and fluency — speaking practice with instant tone feedback, available 24/7. Students can try it free at https://tonetutor.tefusiang.com — no signup required.
>
> If it's useful, I'd be glad to offer your class free access. Would you be open to sharing it with your students, or a quick call?
>
> Thank you for your time,
> [Your name]

*Where to find emails:* university "Asian Studies / Chinese Department / Confucius Institute" faculty pages. Personalize each — generic blasts get ignored/flagged.

---

## X / Twitter (thread)
*(⚠️ Put the link in a REPLY, not tweet 1 — X throttles reach on posts with external links. Attach the 15–30s demo clip to tweet 1; video is what stops the scroll. Tweet 1 is everything — it decides if anyone reads the rest.)*

1/ I'm a Mandarin voice actor — I can hear the exact moment a learner's tone slips. Most apps never catch it, because they drill flashcards, not conversation. So I built something that grades your tones *while you actually talk.* 🧵
2/ The gap: you can ace HSK vocab and still sound "off," because nobody corrects your tones in a real back-and-forth. That's where learners plateau for years.
3/ How it works: pick a scenario (ordering food, a job interview) + your HSK level → have a real conversation by voice or text → every reply gets scored on tone + grammar, with pinyin, audio, and a summary of what to drill.
4/ The honest part: automated tone grading is hard, and I don't fully trust mine yet. I want people to *try to break it* — throw wrong tones at it and tell me where it's off.
5/ Free for 3 full conversations — link below 👇 Tell me if the tone feedback is actually accurate. That's the whole thing I'm trying to get right.
↳ (reply) https://tonetutor.tefusiang.com

---

## After launch
- Collect testimonials + screenshots (XPRIZE needs user evidence)
- Watch Lemon Squeezy revenue + conversion (XPRIZE needs revenue evidence)
- Reply to every comment/DM; iterate on feedback
- A few real paying users + testimonials beats a thousand silent free signups

---

# 📅 Dated Launch Schedule

**Anchor:** XPRIZE "Build with Gemini" deadline = **Aug 17, 2026**. Today = Jun 20, 2026.
**"A" = the day the Lemon Squeezy store clears human review** (payments go live). Launch sequence is offset from A because we must NOT drive traffic before checkout works — a launch-day conversion lost to test mode is the one thing XPRIZE can't replace.

## Track A — Prep NOW (Jun 20 →, not blocked by LS review)
Do all of this *while* waiting on approval so that A+0 is a one-click go.
| Date | Task | Why |
|------|------|-----|
| Jun 20–21 | Record the **15–30s demo clip** (Restaurant · HSK2 → speak a line → tone grade pops → end card) | Hard dependency for X + Product Hunt + Shorts |
| Jun 20–24 | **Warm the HN account** — leave genuine comments on AI/language/Show HN threads | Memory: HN rate-limits Show HNs from new accounts |
| Jun 20–24 | **Warm Reddit** — comment in r/ChineseLanguage + r/LearnChinese; read each sub's self-promo rules/flair | Avoid drive-by-account removal |
| Jun 21 | Write the **HN `[USER: …]` technical line** (how tone grading works + fails) | HN's first question = your credibility |
| Jun 22 | Stand up a **feedback channel** (reply email or simple form) | Capture testimonials = XPRIZE evidence |
| Jun 22 | Put the tonetutor URL in your **小红书 profile bio** | RED throttles in-body links |
| On approval (A) | **Walk the full real-money flow once**: 3 free → paywall → checkout → unlock | Never launch on an unverified live checkout |

## Track B — Launch sequence (offset from approval day A)
Pick an **A that lands on a weekday** you can sit at the keyboard ~3 hrs. Stagger = one channel at a time so you can reply to every comment (the algorithm + trust driver).
| Day | Channel | Notes |
|-----|---------|-------|
| **A+0** | **Reddit — r/ChineseLanguage** | Highest-intent niche, lowest barrier. Post mid-morning their time; reply to every comment all day. |
| **A+1** | **小红书** (+ keep replying to Reddit) | Low-effort, link in bio. |
| **A+2** | **Show HN** | *Only if karma built.* Weekday morning ET; sit on it all day. |
| **A+3** | **Reddit — r/LearnChinese** (separately tailored) + start the **X thread** | Don't reuse the r/ChineseLanguage text. |
| **A+5** | **Product Hunt** | Schedule 12:01am PT; rally a few early genuine testers; reply all day. |
| **A+6 →** | **Shorts (TikTok/IG/YT)** + **university outreach emails** (rolling) | Evergreen; repeat best-performing. |

→ Whole sequence fits in ~1 week. Target **A no later than early July** so revenue + testimonials have 5–6 weeks to accumulate before the submission window.

## Track C — XPRIZE submission runway (fixed dates)
| By date | Task |
|---------|------|
| Continuous | Collect testimonials + screenshots; track LS revenue & conversion rate |
| **Aug 3** | Draft the **500–1000 word narrative**; script + record the **3-min submission video** |
| **Aug 10** | Finalize all submission assets; do a **dry-run** of the Devpost/XPRIZE form |
| **Aug 15** | **Submit (2 days early)** — never trust deadline-day uploads |
| Aug 17 | XPRIZE deadline (hard) |
