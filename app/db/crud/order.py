from sqlalchemy.orm import Session
# from app.db.crud.order import
from fastapi import HTTPException
from diplom.app.db.crud.cart import get_last_cart_by_user
from uuid import uuid4
from app.db.models import Order, Product, Cart, CartProduct, OrderItem
from app.schemas.orders import OrderCreate, OrderUpdate
from sqlalchemy import and_

# Создание заказа
def create_order_from_cart(db: Session, user_id: str, order_data: OrderCreate):
    cart = get_last_cart_by_user(db, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="No cart found for the user")

    # Подсчитываем общую сумму из корзины
    total_amount = sum(item.price * item.quantity for item in cart.products)
    order_id = str(uuid4())
    new_order = Order(
        id=order_id,
        user_id=user_id,
        total_price=total_amount,
        status="pending"  # или order_data.status, если передаётся
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for cart_product in cart.products:
        order_item = OrderItem(
            order_id=order_id,
            product_id=cart_product.product_id,
            quantity=cart_product.quantity,
            price=cart_product.price
        )
        db.add(order_item)

    db.commit()

    for product in cart.products:
        db.delete(product)

    db.delete(cart)
    db.commit()

    return new_order

# Получение заказа по ID
def get_order_by_id(db: Session, order_id: str):
    return db.query(Order).filter(Order.id == order_id).first()

# Получение всех заказов пользователя
def get_orders_by_user(db: Session, user_id: str):
    return db.query(Order).filter(Order.user_id == user_id).all()

# Обновление статуса заказа
def update_order_status(db: Session, order_id: str, status: str):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order

# Удаление заказа
def delete_order(db: Session, order_id: str):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order
