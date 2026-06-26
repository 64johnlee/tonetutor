"""SEO landing pages — generated from one template, each targeting a search query
that funnels to the free test. Imported by main.py and served at /<slug>.
Keeps URLs clean (/chinese-speaking-practice) without 8 static files."""

CTA = "/?utm_source=seo&utm_medium=landing&utm_campaign={slug}"

_TMPL = """<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://tonetutor.tefusiang.com/{slug}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="https://tonetutor.tefusiang.com/{slug}"><meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<style>
:root{{--bg:#0D1117;--card:#161B22;--red:#E5534B;--text:#E6EDF3;--mut:#7D8590}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}}
.wrap{{max-width:720px;margin:0 auto;padding:40px 22px 80px}}
.bar{{height:5px;background:var(--red);border-radius:3px;width:64px;margin-bottom:28px}}
h1{{font-size:32px;line-height:1.2;margin:0 0 16px}}h2{{font-size:21px;margin:38px 0 12px}}
p{{color:#c9d1d9}}.lede{{font-size:19px;color:var(--text)}}
.cta{{display:inline-block;background:var(--red);color:#fff;text-decoration:none;font-weight:700;padding:16px 30px;border-radius:12px;margin:24px 0;font-size:18px}}
.note{{background:var(--card);border-left:3px solid var(--red);padding:14px 18px;border-radius:8px;color:#c9d1d9;font-size:15px}}
.brand{{color:var(--red);font-weight:700}}
footer{{color:var(--mut);font-size:14px;margin-top:48px;border-top:1px solid #21262d;padding-top:18px}}
a{{color:var(--red)}}
</style></head><body><div class="wrap">
<div class="bar"></div><p class="brand">● ToneTutor</p>
<h1>{h1}</h1>
<p class="lede">{lede}</p>
<a class="cta" href="{cta}">🎯 Start the free test →</a>
{body}
<div class="note"><strong>Honest note:</strong> the test grades the transcript of what you say (speech-to-text + Gemini), so it's a spoken-level <em>estimate</em> from your grammar, vocabulary and fluency — not a raw pitch-contour tone analyzer. A fast, honest read on where you stand.</div>
<a class="cta" href="{cta}">Test my level free →</a>
<footer>ToneTutor — real Mandarin conversation practice with an AI native speaker that grades your tones in real time. Built by a bilingual native-speaker voice actor. <a href="/">Home</a> · <a href="/hsk-speaking-test">HSK speaking test</a> · <a href="https://discord.gg/zcjwSfDZ">💬 Join our Discord</a></footer>
</div></body></html>"""

_COMMON_BODY = """<h2>How it works</h2>
<p>Pick a scenario and your level, then just talk — speak or type in Mandarin and have a real back-and-forth with "Lin Wei", your AI native speaker, with pinyin, translation and audio on every line. Each reply is graded for tones and grammar, and you finish with a summary (or a score card) of exactly what to drill next. Free for your first 3 sessions, no signup.</p>"""


def _page(slug, title, desc, h1, lede, body):
    return _TMPL.format(slug=slug, title=title, desc=desc, h1=h1, lede=lede,
                        body=body + _COMMON_BODY, cta=CTA.format(slug=slug))


PAGES = {}

PAGES["chinese-speaking-practice"] = _page(
    "chinese-speaking-practice",
    "Chinese Speaking Practice — Practice Mandarin Conversation with an AI (Free) | ToneTutor",
    "Practice Chinese speaking on your own with an AI native speaker. Hold real Mandarin conversations, get instant tone and grammar feedback, free for 3 sessions. No partner or tutor needed.",
    "Chinese speaking practice — without a tutor or a language partner",
    "The hardest part of learning Mandarin isn't the vocabulary — it's finding someone to actually talk to. ToneTutor gives you an AI native speaker available 24/7, so you can practise speaking the moment you want to.",
    "<p>Most learners can read and recognise far more Chinese than they can confidently say out loud. The fix is reps: real, low-stakes conversation where mistakes are cheap and feedback is instant. That's exactly what this is — talk through everyday scenarios, get your tones and grammar checked on every line, and build the muscle memory that turns study into speech.</p>")

PAGES["practice-mandarin-tones"] = _page(
    "practice-mandarin-tones",
    "Practice Mandarin Tones — Get Your Tones Graded in Real Conversation (Free) | ToneTutor",
    "Practise Mandarin tones where it actually matters — in conversation. Speak in Chinese and get your tones and grammar graded in real time by an AI native speaker. Free, no signup.",
    "Practise Mandarin tones in real conversation, not just drills",
    "Drilling isolated tone pairs is the easy part. Keeping your tones right while you're actually talking — thinking about words, grammar and meaning all at once — is where learners plateau and start to sound \"off.\"",
    "<p>ToneTutor closes that gap: instead of flashcards, you hold a real conversation and every reply is checked for tones and grammar in context, with the correct pinyin and native audio so you can hear and fix it. Throw deliberately wrong tones at it and watch it catch them. That in-context feedback is what actually moves your pronunciation.</p>")

_HSK = {
    1: ("the absolute basics — greetings, numbers, and simple two- to three-word sentences", "around 150 core words"),
    2: ("simple, familiar daily topics in short sentences", "around 300 words"),
    3: ("everyday conversation — describing your life, plans and preferences", "around 600 words"),
    4: ("discussing familiar topics fairly fluently, with connectors and longer sentences", "around 1,200 words"),
    5: ("abstract topics, opinions and hypotheticals with good control", "around 2,500 words"),
    6: ("near-native command — nuance, idioms and natural rhythm", "5,000+ words"),
}
for n, (cando, vocab) in _HSK.items():
    s = f"hsk-{n}-speaking-test"
    PAGES[s] = _page(
        s,
        f"HSK {n} Speaking Test — Check If Your Spoken Chinese Reaches HSK {n} (Free) | ToneTutor",
        f"Free HSK {n} speaking test. Have a 3-minute conversation with an AI native speaker and find out if your spoken Mandarin really reaches HSK {n}. Score, strengths and weak points, no signup.",
        f"HSK {n} speaking test — are you really HSK {n} when you talk?",
        f"HSK {n} is about {cando} ({vocab}). But passing HSK {n} on paper and actually speaking at HSK {n} are two different things — and your spoken level is the hard one to judge alone. This free 3-minute test tells you where your speaking really sits.",
        f"<p>Have a short conversation with an AI native speaker; it estimates whether your spoken Mandarin lands at HSK {n}, gives you a 0–100 score, and shows the exact gaps holding you back — then lets you drill them. Whether you're prepping for the exam or just curious, it's a fast, honest gut-check.</p>")
