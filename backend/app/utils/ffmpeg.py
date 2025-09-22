from __future__ import annotations
import subprocess
from pathlib import Path


def extract_audio(
    video_path: str | Path,
    out_path: str | Path,
    sample_rate: int = 16000,
    channels: int = 1,
    codec: str = "pcm_s16le",  # WAV PCM 16-bit
) -> Path:
    """
    Extract audio from a video using ffmpeg.

    Example command:
    ffmpeg -y -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 output.wav
    """
    video = Path(video_path)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video),
        "-vn",
        "-acodec",
        codec,
        "-ar",
        str(sample_rate),
        "-ac",
        str(channels),
        str(out),
    ]
    subprocess.run(cmd, check=True)
    return out
