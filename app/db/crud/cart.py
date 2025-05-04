from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, delete
from datetime import datetime
from app.db.models import Cart, Product, CartProduct
from app.schemas.cart import CartUpdate
from fastapi import HTTPException
from sqlalchemy.orm import selectinload


async def get_or_create_cart(db: AsyncSession, user_id: str):
    cart = await get_cart(db, user_id)
    if not cart:
        cart = await create_cart(db, user_id)
    return cart


async def create_cart(db: AsyncSession, user_id: str):
    db_cart = Cart(user_id=user_id, updated_at=datetime.utcnow())
    db.add(db_cart)
    await db.commit()
    await db.refresh(db_cart)
    return db_cart


async def get_cart(db: AsyncSession, user_id: str):
    result = await db.execute(select(Cart).filter(Cart.user_id == user_id))
    return result.scalars().first()


async def update_cart(db: AsyncSession, cart_id: str, cart: CartUpdate):
    result = await db.execute(select(Cart).filter(Cart.id == cart_id))
    db_cart = result.scalars().first()

    if db_cart and cart.quantity is not None:
        db_cart.quantity = cart.quantity
        db_cart.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_cart)
    return db_cart


async def delete_cart(db: AsyncSession, user_id: str):
    result = await db.execute(select(Cart).filter(Cart.user_id == user_id))
    db_cart = result.scalars().first()

    if db_cart:
        await db.delete(db_cart)
        await db.commit()
    return db_cart


async def add_product_to_cart(db: AsyncSession, user_id: str, cart_id: str, product_id: str, quantity: int, price: float):
    stmt = select(CartProduct).where(
        CartProduct.cart_id == cart_id,
        CartProduct.product_id == product_id
    )
    existing = await db.execute(stmt)
    existing = existing.scalars().first()

    if existing:
        stmt = update(CartProduct).where(
            CartProduct.cart_id == cart_id,
            CartProduct.product_id == product_id
        ).values(
            quantity=existing.quantity + quantity,
            price=price
        )
        await db.execute(stmt)
    else:
        stmt = insert(CartProduct).values(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
            price=price
        )
        await db.execute(stmt)

    # Обновляем дату корзины
    await db.execute(
        update(Cart).where(Cart.id == cart_id).values({"updated_at": datetime.utcnow()})
    )

    await db.commit()
    return {"message": "Product added to cart successfully."}


async def remove_product_from_cart(db: AsyncSession, user_id: str, product_id: str):
    cart = await get_cart(db, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    stmt = delete(CartProduct).where(
        CartProduct.cart_id == cart.id,
        CartProduct.product_id == product_id
    )
    await db.execute(stmt)

    # Обновляем дату корзины
    await db.execute(
        update(Cart).where(Cart.id == cart.id).values({"updated_at": datetime.utcnow()})
    )

    await db.commit()
    return {"message": "Product removed from cart successfully."}


async def get_cart_items(db: AsyncSession, cart_product_table, cart_id: str):
    stmt = (
        select(Product)
        .join(cart_product_table, cart_product_table.c.product_id == Product.id)
        .where(cart_product_table.c.cart_id == cart_id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_last_cart_by_user(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(Cart)
        .options(selectinload(Cart.products))
        .filter(Cart.user_id == user_id)
        .order_by(Cart.updated_at.desc())
    )
    return result.scalars().first()
