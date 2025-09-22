SHELL := /bin/bash

.PHONY: help dev up down logs api worker fmt

help:
	@echo "Targets: dev, up, down, logs, api, worker"

up:
	docker compose up --build -d

 down:
	docker compose down

logs:
	docker compose logs -f --tail=200

dev:
	docker compose up --build

api:
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

worker:
	celery -A backend.app.core.celery_app.celery_app worker -l info
