from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from google.cloud import texttospeech

router = APIRouter(prefix="/api", tags=["tts"])

_tts_client = None


def _get_tts_client():
    global _tts_client
    if _tts_client is None:
        _tts_client = texttospeech.TextToSpeechClient()
    return _tts_client


class TTSRequest(BaseModel):
    text: str
    rate: float = 0.9   # speaking rate; frontend sends ~0.6 for the 🐢 slow button


_MAX_SENT_CHARS = 100   # Chirp3-HD 400s on sentences without ending punctuation


def _breakable(text: str) -> str:
    """Insert sentence breaks into overlong punctuation-free stretches so
    Chirp3-HD doesn't reject the request with 'sentences that are too long'."""
    out, run = [], 0
    for ch in text:
        out.append(ch)
        if ch in "。！？.!?\n":
            run = 0
        else:
            run += 1
            if run >= _MAX_SENT_CHARS:
                out.append("。")
                run = 0
    return "".join(out)


@router.post("/tts")
async def synthesize_speech(req: TTSRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")

    client = _get_tts_client()
    synthesis_input = texttospeech.SynthesisInput(text=_breakable(req.text))
    voice = texttospeech.VoiceSelectionParams(
        language_code="cmn-CN",
        name="cmn-CN-Chirp3-HD-Aoede",  # Google's latest AI female Mandarin voice
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=max(0.25, min(2.0, req.rate)),
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")

    return Response(content=response.audio_content, media_type="audio/mpeg")
