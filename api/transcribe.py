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
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        audio_channel_count=1,
        language_code="cmn-Hans-CN",
    )
    audio_obj = speech.RecognitionAudio(content=content)

    try:
        response = client.recognize(config=config, audio=audio_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")

    if not response.results:
        return {"transcript": ""}

    return {"transcript": response.results[0].alternatives[0].transcript}
