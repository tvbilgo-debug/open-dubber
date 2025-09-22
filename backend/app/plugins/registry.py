from __future__ import annotations
from pathlib import Path

def transcribe(video_path: str, engine: str = "dummy") -> str:
    # In a real implementation, extract audio via ffmpeg and call appropriate engine
    # Here we return a dummy transcript
    return "[DUMMY TRANSCRIPT] Hello, world. This is a placeholder transcript."


def translate(text: str, target_lang: str, engine: str = "dummy") -> str:
    return f"[DUMMY {target_lang}] {text}"


def synthesize(text: str, target_lang: str, engine: str = "dummy", out_dir: Path | str = ".", base_name: str = "output") -> str:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    # For now, create a placeholder WAV as a zero-byte or minimal file; real TTS would render audio
    wav_path = out_dir / f"{base_name}.wav"
    if not wav_path.exists():
        # write a small headerless placeholder to indicate artifact
        wav_path.write_bytes(b"")
    return str(wav_path)
