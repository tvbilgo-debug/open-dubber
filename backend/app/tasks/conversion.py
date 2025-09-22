from __future__ import annotations
from pathlib import Path
from typing import Optional

from ..core.celery_app import celery_app
from ..utils.ffmpeg import transcode_audio


@celery_app.task(bind=True, name="conversion.convert_audio")
def convert_audio_task(
    self,
    *,
    video_path: str,
    format: str = "wav",
    sample_rate: int = 16000,
    channels: int = 1,
    bitrate: Optional[str | int] = None,
    storage_dir: str,
):
    video_id = Path(video_path).stem
    audio_dir = Path(storage_dir) / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    out_filename = f"{video_id}.{format.lower()}"
    out_path = audio_dir / out_filename

    self.update_state(state="STARTED", meta={"step": "ffmpeg", "format": format})
    transcode_audio(video_path, str(out_path), format=format, sample_rate=sample_rate, channels=channels, bitrate=bitrate)

    url_path = f"/api/assets/audio/{out_filename}"
    return {"filename": out_filename, "url": url_path, "format": format.lower()}
