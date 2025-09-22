from __future__ import annotations
import time
from pathlib import Path
from typing import Dict, List

from ..core.celery_app import celery_app
from ..plugins.registry import transcribe, translate, synthesize

@celery_app.task(bind=True, name="pipeline.process_job")
def process_job(self, video_path: str, target_languages: List[str], engines: Dict[str, str], storage_dir: str):
    job_id = self.request.id or "job"
    video_id = Path(video_path).stem
    storage = Path(storage_dir)

    transcripts_dir = storage / "transcripts"
    translations_dir = storage / "translations"
    dubs_dir = storage / "dubs"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    translations_dir.mkdir(parents=True, exist_ok=True)
    dubs_dir.mkdir(parents=True, exist_ok=True)

    self.update_state(state="STARTED", meta={"step": "transcribe"})
    # Dummy transcription returns plain text
    transcript_text = transcribe(video_path, engine=engines.get("transcription", "dummy"))
    transcript_file = transcripts_dir / f"{video_id}_transcript.txt"
    transcript_file.write_text(transcript_text, encoding="utf-8")

    results = {"transcript": str(transcript_file), "translations": [], "dubs": []}

    for lang in target_languages:
        self.update_state(state="STARTED", meta={"step": f"translate:{lang}"})
        translated_text = translate(transcript_text, target_lang=lang, engine=engines.get("translation", "dummy"))
        tr_file = translations_dir / f"{video_id}_{lang}.txt"
        tr_file.write_text(translated_text, encoding="utf-8")
        results["translations"].append(str(tr_file))

        self.update_state(state="STARTED", meta={"step": f"tts:{lang}"})
        dub_path = synthesize(translated_text, target_lang=lang, engine=engines.get("tts", "dummy"), out_dir=dubs_dir, base_name=f"{video_id}_{lang}")
        results["dubs"].append(str(dub_path))

    return results
