# sellers.py (эндпоинты для продавца)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.products import ProductCreate, ProductUpdate
from app.db.crud.product import create_product, get_product, get_products_by_seller, update_product, delete_product
from app.db.crud.order import update_order_status
from app.db.session import get_db
from app.db.models import Seller, Order
from app.api.v1.statistics import notify_seller


router = APIRouter(prefix="/sellers", tags=["Sellers"])

@router.put("/{seller_id}/orders/{order_id}/status")
async def update_order_status_of_seller(seller_id: int, order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order or order.seller_id != seller_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")

    updated_order = update_order_status(db, order_id, status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Отправляем WebSocket-уведомление
    await notify_seller(seller_id, f"Заказ {order_id} теперь {status}")

    return updated_order

# Создать новый товар для продавца
@router.post("/{seller_id}/products", response_model=ProductCreate)
def create_new_product_for_seller(seller_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    # Проверяем, является ли пользователь продавцом с данным seller_id
    if not db.query(Seller).filter(Seller.id == seller_id).first():
        raise HTTPException(status_code=403, detail="Seller not found or not authorized")
    return create_product(db, product)


# Получить все товары продавца
@router.get("/{seller_id}/products", response_model=list[ProductCreate])
def get_all_products_of_seller(seller_id: int, db: Session = Depends(get_db)):
    # Получаем все товары данного продавца
    products = get_products_by_seller(db, seller_id)
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this seller")
    return products


# Обновить товар продавца
@router.put("/{seller_id}/products/{product_id}", response_model=ProductCreate)
def update_product_of_seller(seller_id: int, product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    # Проверка, является ли товар принадлежностью продавца
    product_db = get_product(db, product_id)
    if product_db and product_db.seller_id != seller_id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this product")

    updated_product = update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


# Удалить товар продавца
@router.delete("/{seller_id}/products/{product_id}")
def delete_product_of_seller(seller_id: int, product_id: int, db: Session = Depends(get_db)):
    # Проверка, является ли товар принадлежностью продавца
    product_db = get_product(db, product_id)
    if product_db and product_db.seller_id != seller_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")

    deleted_product = delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


# # Получить все заказы продавца
# @router.get("/{seller_id}/orders")
# def get_orders_of_seller(seller_id: int, db: Session = Depends(get_db)):
#     # Получаем все заказы для данного продавца
#     orders = get_orders_by_seller(db, seller_id)
#     if not orders:
#         raise HTTPException(status_code=404, detail="No orders found for this seller")
#     return orders


# Обновить статус заказа продавца (например, от "pending" к "completed")
@router.put("/{seller_id}/orders/{order_id}/status")
def update_order_status_of_seller(seller_id: int, order_id: int, status: str, db: Session = Depends(get_db)):
    # Проверяем, принадлежит ли заказ этому продавцу
    order = db.query(Order).filter(Order.id == order_id).first()
    if order and order.seller_id != seller_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")

    # Обновляем статус
    updated_order = update_order_status(db, order_id, status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")

    return updated_order
