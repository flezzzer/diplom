from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.sellers import SellerLogin, SellerOut, SellerCreate
from app.schemas.products import ProductCreate, ProductUpdate, ProductOut
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.orders import OrderStatusUpdate
from app.db.crud.product import create_product, get_product, get_products, update_product, delete_product
from app.db.crud.order import update_order_status
from app.db.crud.sellers import create_seller, authenticate_seller
from app.db.crud.category import create_category, get_categories, update_category, delete_category
from app.db.session import get_db
from app.security import create_access_token
from app.core.auth import get_current_seller
from app.db.models import Seller, Order, Category
from app.api.v1.statistics import notify_seller

router = APIRouter(prefix="/sellers", tags=["Sellers"])

# Регистрация продавца
@router.post("/register", response_model=SellerOut)
def register(seller: SellerCreate, db: Session = Depends(get_db)):
    existing_seller = db.query(Seller).filter(Seller.email == seller.email).first()
    if existing_seller:
        raise HTTPException(status_code=400, detail="Seller with this email already exists.")
    new_seller = create_seller(db, seller)
    return new_seller

# Логин продавца
@router.post("/login")
def login(seller: SellerLogin, db: Session = Depends(get_db)):
    db_seller = authenticate_seller(db, seller)
    if not db_seller:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"id": db_seller.id, "email": db_seller.email})
    return {"access_token": token, "token_type": "bearer"}

# Получить текущего авторизованного продавца
def get_current_seller_from_token(db: Session, token: str = Depends(get_current_seller)):
    seller = db.query(Seller).filter(Seller.id == token.get("id")).first()
    if not seller:
        raise HTTPException(status_code=403, detail="Seller not found")
    return seller

# Обновить статус заказа продавца
@router.put("/{seller_id}/orders/{order_id}/status", response_model=OrderStatusUpdate)
async def update_order_status_of_seller(seller_id: int, order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order or order.seller_id != seller_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")

    updated_order = update_order_status(db, order_id, status)

    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")

    await notify_seller(seller_id, f"Заказ {order_id} теперь {status}")

    return OrderStatusUpdate(
        order_id=order_id,
        status=status,
        message="Статус заказа успешно обновлен"
    )
