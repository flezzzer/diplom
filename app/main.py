from fastapi import FastAPI
import asyncio
from app.api.v1 import user, product, order, reviews, cart, auth, category, sellers, statistics, notify
from app.api.v1.notify import start_receiving_notifications
from app.db.session import init_db as init_clickhouse
from app.db.pg_session import init_db as init_pg
from fastapi.middleware.cors import CORSMiddleware
from app.db.celery_task import sync_postgres_to_clickhouse

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
    # Инициализация PostgreSQL и ClickHouse
    await init_pg()
    init_clickhouse()  # sync, оставляем без await

    # Запуск фоновой задачи
    app.state.task = asyncio.create_task(start_receiving_notifications())
    sync_postgres_to_clickhouse.delay()


@app.on_event("shutdown")
async def shutdown_event():
    app.state.task.cancel()
    await app.state.task


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # На проде лучше ограничить
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
