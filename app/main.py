from fastapi import FastAPI
import asyncio
import time
import redis
from app.api.v1 import user, product, order, reviews, cart, auth, category, sellers, statistics, notify
from app.api.v1.notify import start_receiving_notifications
from app.db.session import init_db as init_clickhouse
from app.db.pg_session import init_db as init_pg
from app.db.celery_task import sync_postgres_to_clickhouse  # Импорт задачи (она уже зарегистрирована через @celery.task)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Подключение роутов
app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(category.router)
app.include_router(reviews.router)
app.include_router(cart.router)
app.include_router(auth.router)
app.include_router(sellers.router)
app.include_router(statistics.router)
app.include_router(notify.router)


@app.on_event("startup")
async def startup_event():
    await init_pg()
    init_clickhouse()
    app.state.task = asyncio.create_task(start_receiving_notifications())

    # Задержка 2 секунды перед отправкой задачи — даём Redis и Celery подняться
    asyncio.create_task(delayed_sync())

async def delayed_sync():
    await asyncio.sleep(2)
    try:
        sync_postgres_to_clickhouse.delay()
        print("Задача на синхронизацию отправлена.")
    except Exception as e:
        print(f"Ошибка при отправке задачи в Celery: {e}")


    # Отправка задачи в очередь

    # sync_postgres_to_clickhouse.delay()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.task.cancel()
    await app.state.task

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
