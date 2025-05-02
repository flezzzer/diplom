from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas.cart import CartCreate
from app.db.crud.cart import (
    get_cart,
    add_product_to_cart,
    remove_product_from_cart,
    delete_cart,
    get_or_create_cart
)
from app.db.session import get_db
from app.db.models import User, Product, Cart
from app.core.auth import get_current_user
from app.schemas.cart_product import CartProductCreate

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=CartCreate)
def read_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_cart(db, current_user.id)


@router.post("/")
def add_product_to_cart_route(
    cart_item: CartProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Получаем или создаём корзину
    cart = get_or_create_cart(db, current_user.id)

    # Проверяем, существует ли товар
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Расчёт общей стоимости товара в корзине
    total_price = product.price * cart_item.quantity

    # Обновляем updated_at вручную (если БД ClickHouse)
    cart.updated_at = datetime.utcnow()
    db.add(cart)
    db.commit()

    return add_product_to_cart(
        db=db,
        user_id=current_user.id,
        cart_id=cart.id,
        product_id=product.id,
        quantity=cart_item.quantity,
        price=total_price
    )


@router.delete("/{product_id}")
def remove_product_from_cart(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return remove_product_from_cart(db, user_id=current_user.id, product_id=product_id)


@router.delete("/")
def clear_user_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_cart(db, user_id=current_user.id)
