from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from typing import Dict
from aiochclient import ChClient
from app.db.async_session import get_clickhouse_client  # новый модуль подключения
from app.config import redis
from app.core.statistics import (
    get_total_products_count,
    get_total_orders_count,
    get_total_revenue,
    get_order_status_count,
    get_category_statistics,
    get_product_statistics,
    get_order_statistics_by_date
)

router = APIRouter()

# # Подключенные клиенты (seller_id -> WebSocket)
# active_connections: Dict[str, WebSocket] = {}
#
# @router.websocket("/ws/{seller_id}")
# async def websocket_endpoint(websocket: WebSocket, seller_id: str):
#     await websocket.accept()
#     active_connections[seller_id] = websocket
#
#     try:
#         while True:
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         del active_connections[seller_id]
#
# # Функция для отправки уведомлений
# async def notify_seller(seller_id: str, message: str):
#     if seller_id in active_connections:
#         await active_connections[seller_id].send_text(message)

router = APIRouter(prefix="/sellers", tags=["Sellers"])

# Получение общей статистики
@router.get("/{seller_id}/statistics")
async def get_seller_statistics(seller_id: str, client: ChClient = Depends(get_clickhouse_client)):
    cache_key = f"seller_stats:{seller_id}"

    cached_data = await redis.get(cache_key)
    if cached_data:
        return eval(cached_data)

    # Получаем статистику из ClickHouse
    total_products = await get_total_products_count(seller_id)
    total_orders = await get_total_orders_count(seller_id)
    total_revenue = await get_total_revenue(seller_id)
    order_status_counts = await get_order_status_count(seller_id)

    stats = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "order_status_counts": order_status_counts,
    }

    await redis.set(cache_key, str(stats), ex=60)
    return stats

# Получение статистики по категориям
@router.get("/{seller_id}/category-statistics")
async def get_category_statistics_report(seller_id: str):
    category_stats = await get_category_statistics(seller_id)
    return category_stats

# Получение статистики по товарам
@router.get("/{seller_id}/product-statistics")
async def get_product_statistics_report(seller_id: str):
    product_stats = await get_product_statistics(seller_id)
    return product_stats

# Получение статистики по датам заказов
@router.get("/{seller_id}/order-statistics-by-date")
async def get_order_statistics_by_date_report(seller_id: str):
    order_stats_by_date = await get_order_statistics_by_date(seller_id)
    return order_stats_by_date
