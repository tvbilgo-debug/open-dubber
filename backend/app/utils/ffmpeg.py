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


def transcode_audio(
    video_path: str | Path,
    out_path: str | Path,
    *,
    format: str = "wav",
    sample_rate: int = 16000,
    channels: int = 1,
    bitrate: str | int | None = None,
) -> Path:
    """
    Transcode audio track from a video into WAV or MP3 using ffmpeg.

    WAV: pcm_s16le, 16-bit. MP3: libmp3lame with optional bitrate (e.g., 128k).
    """
    fmt = format.lower()
    if fmt not in {"wav", "mp3"}:
        raise ValueError(f"unsupported format: {format}")

    video = Path(video_path)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "wav":
        cmd = [
            "ffmpeg", "-y", "-i", str(video), "-vn",
            "-acodec", "pcm_s16le",
            "-ar", str(sample_rate),
            "-ac", str(channels),
            str(out),
        ]
    else:  # mp3
        cmd = [
            "ffmpeg", "-y", "-i", str(video), "-vn",
            "-acodec", "libmp3lame",
            "-ar", str(sample_rate),
            "-ac", str(channels),
        ]
        if bitrate is not None:
            br = f"{bitrate}k" if isinstance(bitrate, int) else str(bitrate)
            cmd.extend(["-b:a", br])
        cmd.append(str(out))

    subprocess.run(cmd, check=True)
    return out
