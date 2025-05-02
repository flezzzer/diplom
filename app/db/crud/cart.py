from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert, delete
from datetime import datetime

from app.db.models import Cart, Product, CartProduct
from app.schemas.cart import CartUpdate
from fastapi import HTTPException


def get_or_create_cart(db: Session, user_id: str):
    cart = get_cart(db, user_id)
    if not cart:
        cart = create_cart(db, user_id)
    return cart


def create_cart(db: Session, user_id: str):
    db_cart = Cart(user_id=user_id, updated_at=datetime.utcnow())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def get_cart(db: Session, user_id: str):
    return db.query(Cart).filter(Cart.user_id == user_id).first()


def update_cart(db: Session, cart_id: str, cart: CartUpdate):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if db_cart and cart.quantity is not None:
        db_cart.quantity = cart.quantity
        db_cart.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_cart)
    return db_cart


def delete_cart(db: Session, user_id: str):
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if db_cart:
        db.delete(db_cart)
        db.commit()
    return db_cart


def add_product_to_cart(db: Session, user_id: str, cart_id: str, product_id: str, quantity: int, price: float):
    stmt = select(CartProduct).where(
        CartProduct.cart_id == cart_id,
        CartProduct.product_id == product_id
    )
    existing = db.execute(stmt).scalar_one_or_none()

    if existing:
        stmt = update(CartProduct).where(
            CartProduct.cart_id == cart_id,
            CartProduct.product_id == product_id
        ).values(
            quantity=existing.quantity + quantity,
            price=price
        )
        db.execute(stmt)
    else:
        stmt = insert(CartProduct).values(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
            price=price
        )
        db.execute(stmt)

    # Обновляем дату корзины
    db.query(Cart).filter(Cart.id == cart_id).update(
        {"updated_at": datetime.utcnow()}
    )

    db.commit()
    return {"message": "Product added to cart successfully."}


def remove_product_from_cart(db: Session, user_id: str, product_id: str):
    cart = get_cart(db, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    stmt = delete(CartProduct).where(
        CartProduct.cart_id == cart.id,
        CartProduct.product_id == product_id
    )
    db.execute(stmt)

    # Обновляем дату корзины
    db.query(Cart).filter(Cart.id == cart.id).update(
        {"updated_at": datetime.utcnow()}
    )

    db.commit()
    return {"message": "Product removed from cart successfully."}


def get_cart_items(db: Session, cart_product_table, cart_id: str):
    stmt = (
        select(Product)
        .join(cart_product_table, cart_product_table.c.product_id == Product.id)
        .where(cart_product_table.c.cart_id == cart_id)
    )
    result = db.execute(stmt).scalars().all()
    return result


def get_last_cart_by_user(db: Session, user_id: str):
    return (
        db.query(Cart)
        .filter(Cart.user_id == user_id)
        .order_by(Cart.updated_at.desc())
        .first()
    )
