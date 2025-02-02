from sqlalchemy.orm import Session
from app.db.models import Order, Product, Cart
from app.schemas.orders import OrderCreate, OrderUpdate
from sqlalchemy import and_

# Создание заказа
def create_order(db: Session, user_id: int, order_data: OrderCreate):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        return {"error": "Cart is empty or does not exist"}

    # Создаем заказ
    db_order = Order(
        user_id=user_id,
        status="pending",  # Новый заказ создается в статусе "pending"
        total_amount=cart.total_amount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Очищаем корзину после оформления заказа
    db.delete(cart)
    db.commit()

    return db_order

# Получение заказа по ID
def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

# Получение всех заказов пользователя
def get_orders_by_user(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

# Обновление статуса заказа
def update_order_status(db: Session, order_id: int, status: str):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order

# Удаление заказа
def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order
