from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .api.routes import api_router

settings = get_settings()

app = FastAPI(title="Open Dubber API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "env": settings.env,
        "engines": {
            "transcription": settings.transcription_engine,
            "translation": settings.translation_engine,
            "tts": settings.tts_engine,
        },
    }

app.include_router(api_router, prefix=settings.api_prefix)
