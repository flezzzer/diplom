from sqlalchemy.orm import Session
from app.db.models import Product
from app.schemas.products import ProductCreate, ProductUpdate

# Создание товара
def create_product(db: Session, product: ProductCreate):
    db_product = Product(name=product.name, description=product.description, price=product.price,
                         stock=product.stock, category_id=product.category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Получение товара по id
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

# Получение всех товаров
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def get_products_by_seller(db:Session, seller_id: int):
    return db.query(Product).filter(Product.seller_id == seller_id)

# Обновление товара
def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        if product.name:
            db_product.name = product.name
        if product.description:
            db_product.description = product.description
        if product.price is not None:
            db_product.price = product.price
        if product.stock is not None:
            db_product.stock = product.stock
        if product.category_id is not None:
            db_product.category_id = product.category_id
        db.commit()
        db.refresh(db_product)
    return db_product

# Удаление товара
def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
