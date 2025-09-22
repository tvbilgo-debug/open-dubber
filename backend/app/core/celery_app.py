from celery import Celery
from .config import get_settings

settings = get_settings()

celery_app = Celery(
    "open_dubber",
    broker=settings.broker_url,
    backend=settings.result_backend,
)

# Basic reliable defaults
celery_app.conf.update(
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
