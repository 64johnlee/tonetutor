# ToneTutor — AI Mandarin Conversation Tutor

Practice real Mandarin conversations with an AI native speaker. Pick a scenario
(restaurant, shopping, travel, work, making friends, doctor visit) and an HSK
level (1–6), then chat with **Lin Wei**. Every reply is graded for **tone usage**
and accuracy, with pinyin annotation and an end-of-session summary (score, strengths,
mistakes, vocab to review).

🔗 **Live demo:** https://tonetitor-346314536777.asia-southeast1.run.app

> Built for the XPRIZE *Education & Human Potential* category.

## Features

- Conversational practice with Gemini playing a native speaker in-scenario
- Per-reply **tone + grammar grading** with corrections
- **Pinyin ruby annotation** over Mandarin characters
- **Voice input** — speak your reply (cross-browser: iOS Safari/Chrome, Android, desktop)
- HSK 1–6 level selector
- Session summary with animated score ring

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI on Google Cloud Run |
| LLM | Gemini 2.5 Flash via Vertex AI |
| Speech input | Google Cloud Speech-to-Text (`cmn-Hans-CN`, LINEAR16) |
| Audio output | Google Cloud Text-to-Speech (`cmn-CN-Chirp3-HD-Aoede`) |
| Frontend | Single-page HTML + vanilla JS |

## Run locally

```bash
# 1. Configure environment
cp .env.example .env        # then fill in your values

# 2. Install
pip install -r requirements.txt

# 3. Authenticate to Google Cloud (Vertex AI + STT/TTS use ADC)
gcloud auth application-default login

# 4. Start
uvicorn main:app --reload
```

Open http://localhost:8000.

## Deploy (Cloud Run)

```bash
gcloud run deploy tonetitor --source . --region asia-southeast1
```

## License

MIT
