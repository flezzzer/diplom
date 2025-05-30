from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.sellers import SellerLogin, SellerOut, SellerCreate
from app.schemas.products import ProductCreate, ProductUpdate, ProductOut
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.orders import OrderStatusUpdate
from app.db.crud.product import create_product, get_product, get_products, update_product, delete_product
from app.db.crud.order import update_order_status
from app.db.crud.sellers import create_seller, authenticate_seller
from app.db.crud.category import create_category, get_categories, update_category, delete_category
from app.db.pg_session import get_pg_session  # Импортируем get_pg_session
from app.security import create_access_token
from app.core.auth import get_current_seller
from app.db.models import Seller, Order, Category
from app.api.v1.notify import notify_seller

router = APIRouter(prefix="/sellers", tags=["Sellers"])

@router.post("/register", response_model=SellerOut)
async def register(seller: SellerCreate, db: AsyncSession = Depends(get_pg_session)):  # Используем get_pg_session
    result = await db.execute(select(Seller).filter(Seller.email == seller.email))
    existing_seller = result.scalars().first()
    if existing_seller:
        raise HTTPException(status_code=400, detail="Seller with this email already exists.")
    new_seller = await create_seller(db, seller)
    return new_seller

@router.post("/login")
async def login(seller: SellerLogin, db: AsyncSession = Depends(get_pg_session)):  # Используем get_pg_session
    db_seller = await authenticate_seller(db, seller)
    if not db_seller:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"id": str(db_seller.id), "email": db_seller.email})
    return {"access_token": token, "token_type": "bearer"}

async def get_current_seller_from_token(db: AsyncSession, token: str = Depends(get_current_seller)):
    result = await db.execute(select(Seller).filter(Seller.id == token.get("id")))
    seller = result.scalars().first()
    if not seller:
        raise HTTPException(status_code=403, detail="Seller not found")
    return seller

@router.put("/{seller_id}/orders/{order_id}/status", response_model=OrderStatusUpdate)
async def update_order_status_of_seller(
    seller_id: str,
    order_id: str,
    status: str,
    db: AsyncSession = Depends(get_pg_session)  # Используем get_pg_session
):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalars().first()

    if not order or order.seller_id != seller_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")

    updated_order = await update_order_status(db, order_id, status)

    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")

    await notify_seller(seller_id, f"Заказ {order_id} теперь {status}")

    return OrderStatusUpdate(
        order_id=order_id,
        status=status,
        message="Статус заказа успешно обновлен"
    )
