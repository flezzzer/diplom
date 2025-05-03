from fastapi import FastAPI
import asyncio
from app.api.v1 import user, product, order, reviews, cart, auth, category, sellers, statistics, notify
from app.api.v1.notify import start_receiving_notifications
from app.db.session import init_db
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
    # Запуск асинхронной задачи при старте
    app.state.task = asyncio.create_task(start_receiving_notifications())

@app.on_event("shutdown")
async def shutdown_event():
    # Завершаем задачу при остановке
    app.state.task.cancel()
    await app.state.task

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любого домена (на проде лучше ограничить)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
# Инициализация базы данных
)
init_db()
