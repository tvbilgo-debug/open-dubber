# Open Dubber (OSS Video Translation & Dubbing)

An open-source, reliable alternative to VideoDubber with pluggable AI engines, offline/local processing, batching, and enterprise-friendly auditability.

## Core Features (MVP)
- Video upload/import (file; URL import placeholder)
- Transcription (engine-pluggable)
- Translation (engine-pluggable)
- Text-to-Speech voice dubbing (engine-pluggable)
- Timeline assets (transcript, subtitles, dubbed audio) produced per language
- Export-ready artifacts (subtitles and dubbed audio tracks)

## Reliability & OSS Edge
- Multi-engine support (choose Whisper/Whisper.cpp/Deepgram/OpenAI for ASR; MarianMT/NLLB/DeepL for MT; Coqui/ElevenLabs/OpenVoice/Bark for TTS)
- Offline/local mode (Whisper.cpp + ffmpeg)
- Batch processing queue (Celery + Redis)
- Plugin ecosystem for engines and integrations
- Audit logs + determinism switches for reproducibility
- Scalable via Docker/Kubernetes

## Tech Stack
- Frontend: Next.js (React), Tailwind (optional), Video.js (preview)
- Backend: FastAPI (Python), Celery workers, Redis broker, ffmpeg
- Storage: Local disk by default; S3/MinIO configurable
- Database: Postgres (planned)
- Deployment: Docker Compose (dev), Kubernetes (future), GitHub Actions (future)

## Repository Layout
```
open-dubber/
  backend/
    app/
      api/            # FastAPI routes
      core/           # settings, celery, utils
      models/         # pydantic/db models (minimal now)
      plugins/        # pluggable engines (stubs/dummy now)
        transcription/
        translation/
        tts/
      tasks/          # Celery tasks (pipeline)
    requirements.txt
    Dockerfile
  frontend/
    src/
      pages/          # Next.js pages (MVP)
      components/
      styles/
    package.json
    Dockerfile
  storage/            # Local dev artifacts (videos, outputs)
  docs/
  docker-compose.yml
  .env.example
  .gitignore
  LICENSE
  README.md
```

## Quickstart (Dev, Docker)
1) Copy env template
- cp .env.example .env

2) Start services
- docker compose up --build

This will start:
- API at http://localhost:8000 (FastAPI)
- Worker (Celery)
- Redis (broker/backend)
- Frontend at http://localhost:3000

3) Try it
- Open http://localhost:3000
- Upload a video
- Start a job for a target language (e.g., "es")
- Poll job status and check storage/ for artifacts

## Configuration
Environment variables (see .env.example):
- BROKER_URL, RESULT_BACKEND (Redis)
- STORAGE_DIR (local dev: storage)
- TRANSCRIPTION_ENGINE, TRANSLATION_ENGINE, TTS_ENGINE (default: dummy)
- S3/MinIO credentials (optional)

## Engine Plugins
- Transcription: whispercpp, openai, deepgram, dummy
- Translation: marianmt, nllb, deepl, dummy
- TTS: coqui, elevenlabs, openvoice, bark, dummy

Engines are selected via env vars and resolved in app/plugins/registry.py.

## Roadmap
- Real engines (Whisper.cpp runner, MarianMT via transformers, Coqui/ElevenLabs)
- Timeline editor UI and precise A/V alignment
- Subtitles (SRT/VTT) generation + muxing
- Export (mux dubbed audio back into video)
- Audit logs (DB), job reproducibility manifests
- Kubernetes manifests, CI, auth multi-tenant

## License
MIT License. Contributions welcome!
