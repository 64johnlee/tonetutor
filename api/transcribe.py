from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from google.cloud import speech

router = APIRouter(prefix="/api", tags=["transcribe"])

_speech_client = None


def _get_speech_client():
    global _speech_client
    if _speech_client is None:
        _speech_client = speech.SpeechClient()
    return _speech_client


@router.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    sample_rate: int = Form(48000),
):
    content = await audio.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty audio file")

    # Clamp to Google STT's accepted LINEAR16 range (8000–48000 Hz)
    sample_rate = max(8000, min(48000, sample_rate))

    client = _get_speech_client()

    def _build_config(model):
        kwargs = dict(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            audio_channel_count=1,
            language_code="cmn-Hans-CN",
        )
        if model:
            kwargs["model"] = model
        return speech.RecognitionConfig(**kwargs)

    audio_obj = speech.RecognitionAudio(content=content)

    try:
        # "latest_long" is markedly more accurate on conversational Mandarin than the
        # default model. Fall back to the default if it's unavailable so transcription
        # never hard-fails — i.e. no regression vs. the previous behaviour.
        try:
            response = client.recognize(config=_build_config("latest_long"), audio=audio_obj)
        except Exception:
            response = client.recognize(config=_build_config(None), audio=audio_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")

    if not response.results:
        return {"transcript": ""}

    return {"transcript": response.results[0].alternatives[0].transcript}
