from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.workers.tasks"]
)

celery_app.conf.beat_schedule = {
    "run-monitor-checks-every-minute": {
        "task": "app.workers.tasks.schedule_monitor_checks",
        "schedule": 60.0, # Run every minute
    },
}
