from celery import Celery
from datetime import timedelta

celery_app = Celery(
    "my_project",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


celery_app.conf.imports = (
    "services.celery.report",
)


celery_app.conf.beat_schedule = {
    "hello-world-every-10-seconds": {
        "task": "services.celery.report.hello_world",
        "schedule": timedelta(seconds=10),
    }
}

celery_app.conf.timezone = "UTC"