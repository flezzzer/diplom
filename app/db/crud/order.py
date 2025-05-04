from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from sqlalchemy import delete
from fastapi import HTTPException
from uuid import uuid4
from app.db.models import Order, Product, Cart, CartProduct, OrderItem
from app.schemas.orders import OrderCreate, OrderUpdate
from app.db.crud.cart import get_last_cart_by_user

# Создание заказа из корзины
async def create_order_from_cart(db: AsyncSession, user_id: str, order_data: OrderCreate):
    cart = await get_last_cart_by_user(db, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="No cart found for the user")

    # Подсчитываем общую сумму из корзины
    total_amount = sum(item.price * item.quantity for item in cart.products)
    order_id = str(uuid4())
    new_order = Order(
        id=order_id,
        user_id=user_id,
        total_price=total_amount,
        status="pending",
        created_at=datetime.utcnow()
        # или order_data.status, если передаётся
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    for cart_product in cart.products:
        order_item = OrderItem(
            order_id=order_id,
            product_id=cart_product.product_id,
            quantity=cart_product.quantity,
            price=cart_product.price
        )
        db.add(order_item)

    await db.commit()

    # Удаляем продукты из корзины
    for product in cart.products:
        await db.delete(product)

    await db.delete(cart)
    await db.commit()

    return new_order

# Получение заказа по ID
async def get_order_by_id(db: AsyncSession, order_id: str):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    return result.scalars().first()

# Получение всех заказов пользователя
async def get_orders_by_user(db: AsyncSession, user_id: str):
    result = await db.execute(select(Order).filter(Order.user_id == user_id))
    return result.scalars().all()

# Обновление статуса заказа
async def update_order_status(db: AsyncSession, order_id: str, status: str):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    db_order = result.scalars().first()
    if db_order:
        db_order.status = status
        await db.commit()
        await db.refresh(db_order)
    return db_order

# Удаление заказа
async def delete_order(db: AsyncSession, order_id: str):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    db_order = result.scalars().first()
    if db_order:
        await db.delete(db_order)
        await db.commit()
    return db_order
