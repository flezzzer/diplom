# celery_config.py
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

# Конфигурация для Celery Beat
app.conf.beat_schedule = {
    'sync_postgres_to_clickhouse_every_5_minutes': {
        'task': 'tasks.sync_postgres_to_clickhouse',
        'schedule': 300.0,  # Каждые 5 минут
    },
}
app.conf.timezone = 'UTC'
