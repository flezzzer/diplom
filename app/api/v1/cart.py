from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import select

from app.schemas.cart import CartCreate, CartOut
from app.db.crud.cart import (
    get_cart,
    add_product_to_cart,
    remove_product_from_cart,
    delete_cart,
    get_or_create_cart
)
from app.db.pg_session import get_pg_session
from app.db.models import User, Product, Cart
from app.core.auth import get_current_user
from app.schemas.cart_product import CartProductCreate

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=CartCreate)
async def read_cart(
    db: AsyncSession = Depends(get_pg_session),
    current_user: User = Depends(get_current_user)
):
    return await get_cart(db, current_user.id)

@router.post("/")
async def add_product_to_cart_route(
    cart_item: CartProductCreate,
    db: AsyncSession = Depends(get_pg_session),
    current_user: User = Depends(get_current_user)
):
    cart = await get_or_create_cart(db, current_user.id)

    product = await db.execute(select(Product).filter(Product.id == cart_item.product_id))
    product = product.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = product.price * cart_item.quantity

    cart.updated_at = datetime.utcnow()
    db.add(cart)
    await db.commit()

    return await add_product_to_cart(
        db=db,
        user_id=current_user.id,
        cart_id=cart.id,
        product_id=product.id,
        quantity=cart_item.quantity,
        price=total_price
    )

@router.delete("/{product_id}")
async def remove_product_from_cart(
    product_id: str,
    db: AsyncSession = Depends(get_pg_session),
    current_user: User = Depends(get_current_user)
):
    return await remove_product_from_cart(db, user_id=current_user.id, product_id=product_id)

@router.delete("/")
async def clear_user_cart(
    db: AsyncSession = Depends(get_pg_session),
    current_user: User = Depends(get_current_user)
):
    return await delete_cart(db, user_id=current_user.id)
