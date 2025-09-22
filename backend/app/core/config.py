from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    env: str = "development"
    api_prefix: str = "/api"

    broker_url: str = "redis://localhost:6379/0"
    result_backend: str = "redis://localhost:6379/1"

    storage_dir: str = "storage"

    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]

    # Engines
    transcription_engine: str = "dummy"
    translation_engine: str = "dummy"
    tts_engine: str = "dummy"

    class Config:
        env_file = ".env"

    def storage_path(self) -> Path:
        p = Path(self.storage_dir)
        return p if p.is_absolute() else (ROOT_DIR / p)

@lru_cache
def get_settings() -> Settings:
    return Settings()
