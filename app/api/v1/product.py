# app/api/v1/products.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.products import ProductCreate, ProductUpdate
from app.db.crud.product import create_product, get_product, get_products, update_product, delete_product
from app.db.session import get_db
from app.core.auth import get_current_seller  # Зависимость для получения текущего продавца

router = APIRouter(prefix="/products", tags=["Products"])

# Создание нового продукта
@router.post("/", response_model=ProductCreate)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_seller = Depends(get_current_seller)
):
    # Привязка продукта к продавцу через current_seller
    return create_product(db, product, seller_id=current_seller.id)

# Получение продукта по id
@router.get("/{product_id}", response_model=ProductCreate)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Получение всех продуктов
@router.get("/", response_model=list[ProductCreate])
def read_products(db: Session = Depends(get_db)):
    return get_products(db)

# Обновление данных продукта
@router.put("/{product_id}")
def update_product_info(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_seller = Depends(get_current_seller)
):
    # Привязка продукта к продавцу через current_seller
    updated_product = update_product(db, product_id, product, seller_id=current_seller.id)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found or not owned by the current seller")
    return updated_product

# Удаление продукта
@router.delete("/{product_id}")
def delete_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    current_seller = Depends(get_current_seller)
):
    # Привязка продукта к продавцу через current_seller
    deleted_product = delete_product(db, product_id, seller_id=current_seller.id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found or not owned by the current seller")
    return {"message": "Product successfully deleted"}
