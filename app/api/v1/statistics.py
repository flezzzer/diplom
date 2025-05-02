# app/api/v1/statistics.py

from fastapi import APIRouter, Depends, HTTPException
from ...config import redis
from app.core.statistics import (
    get_total_products_count,
    get_total_orders_count,
    get_total_revenue,
    get_order_status_count
)
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict

router = APIRouter()

# Подключенные клиенты (seller_id -> WebSocket)
active_connections: Dict[str, WebSocket] = {}


@router.websocket("/ws/{seller_id}")
async def websocket_endpoint(websocket: WebSocket, seller_id: str):
    await websocket.accept()
    active_connections[seller_id] = websocket  # Запоминаем подключение

    try:
        while True:
            await websocket.receive_text()  # Ожидаем сообщения от клиента (можно не использовать)
    except WebSocketDisconnect:
        del active_connections[seller_id]  # Удаляем при отключении


# Функция для отправки уведомлений
async def notify_seller(seller_id: str, message: str):
    if seller_id in active_connections:
        await active_connections[seller_id].send_text(message)

router = APIRouter(prefix="/sellers", tags=["Sellers"])


@router.get("/{seller_id}/statistics")
async def get_seller_statistics(seller_id: str):
    cache_key = f"seller_stats:{seller_id}"

    # Проверяем, есть ли статистика в кэше
    cached_data = await redis.get(cache_key)
    if cached_data:
        return eval(cached_data)  # Преобразуем строку обратно в словарь

    # Если в кэше нет — собираем статистику
    total_products = await get_total_products_count(seller_id)
    total_orders = await get_total_orders_count(seller_id)
    total_revenue = await get_total_revenue(seller_id)
    order_status_counts = await get_order_status_count(seller_id)

    stats = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "order_status_counts": order_status_counts
    }

    # Кэшируем результат на 60 секунд
    await redis.set(cache_key, str(stats), ex=60)

    return stats
