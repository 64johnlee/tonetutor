from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from api.chat import router as chat_router
from api.session import router as session_router
from api.transcribe import router as transcribe_router
from api.tts import router as tts_router
from api.billing import router as billing_router

app = FastAPI(title="ToneTutor", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(session_router)
app.include_router(transcribe_router)
app.include_router(tts_router)
app.include_router(billing_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html", headers={"Cache-Control": "no-store"})


@app.get("/health")
async def health():
    return {"status": "ok"}
