from __future__ import annotations
import os
import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from fastapi.responses import JSONResponse, FileResponse

from ..core.config import get_settings
from ..core.celery_app import celery_app
from ..tasks.pipeline import process_job
from ..tasks.conversion import convert_audio_task

api_router = APIRouter()
settings = get_settings()

VIDEOS_DIR = settings.storage_path() / "videos"
TRANSCRIPTS_DIR = settings.storage_path() / "transcripts"
TRANSLATIONS_DIR = settings.storage_path() / "translations"
DUBS_DIR = settings.storage_path() / "dubs"
AUDIO_DIR = settings.storage_path() / "audio"
for d in (VIDEOS_DIR, TRANSCRIPTS_DIR, TRANSLATIONS_DIR, DUBS_DIR, AUDIO_DIR):
    d.mkdir(parents=True, exist_ok=True)


def _video_path_from_id(vid: str) -> Optional[Path]:
    for p in VIDEOS_DIR.glob(f"{vid}.*"):
        return p
    return None


@api_router.post("/videos/upload")
async def upload_video(file: UploadFile = File(...)):
    # Persist uploaded file to storage/videos
    vid = str(uuid.uuid4())
    ext = Path(file.filename).suffix or ".bin"
    out_path = VIDEOS_DIR / f"{vid}{ext}"
    try:
        contents = await file.read()
        with open(out_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
    return {"video_id": vid, "filename": file.filename, "path": str(out_path)}


class JobRequest:
    def __init__(
        self,
        video_id: str,
        target_languages: List[str],
        transcription_engine: Optional[str] = None,
        translation_engine: Optional[str] = None,
        tts_engine: Optional[str] = None,
    ):
        self.video_id = video_id
        self.target_languages = target_languages
        self.transcription_engine = transcription_engine or settings.transcription_engine
        self.translation_engine = translation_engine or settings.translation_engine
        self.tts_engine = tts_engine or settings.tts_engine


@api_router.post("/jobs")
def create_job(payload: JobRequest = Body(...)):
    video_path = _video_path_from_id(payload.video_id)
    if not video_path:
        raise HTTPException(status_code=404, detail="video not found")

    task = process_job.delay(
        video_path=str(video_path),
        target_languages=payload.target_languages,
        engines={
            "transcription": payload.transcription_engine,
            "translation": payload.translation_engine,
            "tts": payload.tts_engine,
        },
        storage_dir=str(settings.storage_path()),
    )
    return {"job_id": task.id, "status": "queued"}


@api_router.get("/jobs/{job_id}")
def job_status(job_id: str):
    res = celery_app.AsyncResult(job_id)
    data = {
        "job_id": job_id,
        "state": res.state,
        "meta": res.info if isinstance(res.info, dict) else {"detail": str(res.info)},
    }
    return JSONResponse(data)


@api_router.get("/videos/{video_id}/assets")
def list_assets(video_id: str):
    out = {"transcripts": [], "translations": [], "dubs": [], "audio": []}
    out["transcripts"] = [str(p) for p in TRANSCRIPTS_DIR.glob(f"{video_id}_*.txt")]
    out["translations"] = [str(p) for p in TRANSLATIONS_DIR.glob(f"{video_id}_*.txt")]
    out["dubs"] = [str(p) for p in DUBS_DIR.glob(f"{video_id}_*.wav")]
    out["audio"] = [p.name for p in AUDIO_DIR.glob(f"{video_id}.*")]
    return out


@api_router.post("/videos/{video_id}/convert/audio")
def convert_audio(video_id: str, params: dict = Body(default={})):  # type: ignore[override]
    video_path = _video_path_from_id(video_id)
    if not video_path:
        raise HTTPException(status_code=404, detail="video not found")

    fmt = str(params.get("format", "wav")).lower()
    if fmt not in {"wav", "mp3"}:
        raise HTTPException(status_code=400, detail="supported formats: wav, mp3")

    sample_rate = int(params.get("sample_rate", 16000))
    channels = int(params.get("channels", 1))
    bitrate = params.get("bitrate")  # allow "128k" or 128 for mp3

    task = convert_audio_task.delay(
        video_path=str(video_path),
        format=fmt,
        sample_rate=sample_rate,
        channels=channels,
        bitrate=bitrate,
        storage_dir=str(settings.storage_path()),
    )

    return {"job_id": task.id, "status": "queued"}


@api_router.get("/assets/audio/{filename}")
def get_audio_asset(filename: str):
    safe_name = Path(filename).name
    file_path = AUDIO_DIR / safe_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="audio not found")
    # For now we always serve wav
    return FileResponse(str(file_path), media_type="audio/wav", filename=safe_name)
