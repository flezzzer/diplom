# app/core/statistics.py

from sqlalchemy.orm import Session
from app.db.models import Order, Product
from sqlalchemy.future import select
from app.db.session import async_session


# Получить общее количество продуктов продавца
async def get_total_products_count(db: Session, seller_id: int):
    result = await db.execute(select(Product).filter(Product.seller_id == seller_id))
    products = result.scalars().all()
    return len(products)


# Получить общее количество заказов продавца
async def get_total_orders_count(db: Session, seller_id: int):
    result = await db.execute(select(Order).filter(Order.seller_id == seller_id))
    orders = result.scalars().all()
    return len(orders)


# Получить общий доход продавца
async def get_total_revenue(db: Session, seller_id: int):
    result = await db.execute(select(Order).filter(Order.seller_id == seller_id))
    orders = result.scalars().all()
    total_revenue = sum(order.total_price for order in orders)
    return total_revenue


# Получить статистику по состоянию заказов (pending, completed, cancelled)
async def get_order_status_count(db: Session, seller_id: int):
    status_counts = {
        "pending": 0,
        "completed": 0,
        "cancelled": 0
    }
    result = await db.execute(select(Order).filter(Order.seller_id == seller_id))
    orders = result.scalars().all()

    for order in orders:
        status_counts[order.status] += 1

    return status_counts
