from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.products import ProductCreate, ProductUpdate, ProductBase
from app.db.crud.product import (
    create_product,
    get_product,
    get_products,
    update_product as update_product_crud,
    delete_product as delete_product_crud
)
from app.db.session import get_db
from app.core.auth import get_current_seller
from app.db.models import User

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductBase)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_seller: User = Depends(get_current_seller)
):
    return create_product(db, product, seller_id=current_seller.id)

@router.get("/{product_id}", response_model=ProductBase)
def read_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=list[ProductBase])
def read_products(
    db: Session = Depends(get_db)
):
    return get_products(db)

@router.put("/{product_id}", response_model=ProductBase)
def update_product_info(
    product_id: str,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_seller: User = Depends(get_current_seller)
):
    updated_product = update_product_crud(db, product_id, product, seller_id=current_seller.id)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found or not owned by the current seller")
    return updated_product

@router.delete("/{product_id}")
def delete_product_by_id(
    product_id: str,
    db: Session = Depends(get_db),
    current_seller: User = Depends(get_current_seller)
):
    deleted_product = delete_product_crud(db, product_id, seller_id=current_seller.id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found or not owned by the current seller")
    return {"message": "Product successfully deleted"}
