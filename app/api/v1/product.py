from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.products import ProductCreate, ProductUpdate
from app.db.crud.product import create_product, get_product, get_products, update_product, delete_product
from app.db.session import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductCreate)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.get("/{product_id}", response_model=ProductCreate)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=list[ProductCreate])
def read_products(db: Session = Depends(get_db)):
    return get_products(db)

@router.put("/{product_id}")
def update_product_info(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    return update_product(db, product_id, product)

@router.delete("/{product_id}")
def delete_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return delete_product(db, product_id)
