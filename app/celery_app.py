from celery import Celery
from celery.schedules import crontab

# celery = Celery(
#     "diplom",
#     broker="redis://localhost:6379/0",          # имя контейнера как hostname
#     backend="redis://localhost:6379/0",         # не обязательно, но можно
#     result_backend="redis://localhost:6379/0",  # явно указывать можно
#     broker_transport_options={"visibility_timeout": 3600}
# )
#
# celery.autodiscover_tasks(["app.db"])
#
# celery.conf.beat_schedule = {
#     "sync-every-5-minutes": {
#         "task": "app.db.celery_task.sync_postgres_to_clickhouse",
#         "schedule": crontab(minute="*/5"),  # Каждые 5 минут
#     },
# }
# celery.conf.timezone = "UTC"

# celery_app.py

from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "diplom",
    broker="redis://redis_cache:6379/0",
    backend="redis://redis_cache:6379/0",
    result_backend="redis://redis_cache:6379/0",
    broker_transport_options={"visibility_timeout": 3600},
)

celery.autodiscover_tasks(['app.db.celery_task'])

celery.conf.beat_schedule = {
    "sync-every-5-minutes": {
        "task": "app.db.celery_task.sync_postgres_to_clickhouse",
        "schedule": crontab(minute="*/5"),
    }
}
celery.conf.timezone = "UTC"


