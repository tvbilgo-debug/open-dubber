# Contributing to Open Dubber

Thanks for your interest in contributing! This guide explains how to set up your environment, propose changes, and follow our conventions.

## Development Setup
- Requirements: Docker + Docker Compose, Node 20+, Python 3.11+
- Quickstart (Docker):
  - cp .env.example .env
  - docker compose up --build
  - Frontend: http://localhost:3000, API: http://localhost:8000

## Project Structure
- backend/: FastAPI API, Celery tasks, pluggable engines
- frontend/: Next.js UI
- storage/: Local dev artifact store

## Branching & Workflow
- Use GitHub Flow: create a feature branch from main, open a PR when ready.
- Ensure CI passes locally if possible.

## Commit Messages
- Follow Conventional Commits: feat:, fix:, chore:, docs:, refactor:, test:
  - feat(backend): add whisper.cpp transcription runner
  - fix(frontend): handle upload error state

## Code Style
- Python: aim for readable, typed code; prefer pydantic models; add small unit tests where practical.
- TypeScript/React: functional components, hooks, minimal state; avoid unnecessary deps.
- Keep changes small and focused.

## Tests
- Backend: pytest (planned); for now, add minimal unit tests where trivial.
- Frontend: add lightweight tests (Vitest/Jest) as we grow.

## Pull Requests
- Fill out the PR template.
- Include screenshots/logs for UI or runtime changes when helpful.
- Update README/docs when necessary.

## Security
- Do not include credentials in code or logs. Use environment variables.

## License
- By contributing, you agree your contributions are licensed under the project’s MIT License.
