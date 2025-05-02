# app/db/crud/product.py

from sqlalchemy.orm import Session
from app.db.models import Product
from app.schemas.products import ProductCreate, ProductUpdate

# Создание нового продукта
def create_product(db: Session, product: ProductCreate, seller_id: str):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
        seller_id=seller_id  # Привязка к продавцу
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Получение продукта по id
def get_product(db: Session, product_id: str):
    return db.query(Product).filter(Product.id == product_id).first()

# Получение всех продуктов
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

# Обновление данных продукта
def update_product(db: Session, product_id: str, product: ProductUpdate, seller_id: str):
    db_product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller_id).first()
    if db_product:
        if product.name:
            db_product.name = product.name
        if product.description:
            db_product.description = product.description
        if product.price:
            db_product.price = product.price
        db.commit()
        db.refresh(db_product)
    return db_product

# Удаление продукта
def delete_product(db: Session, product_id: str, seller_id: str):
    db_product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
