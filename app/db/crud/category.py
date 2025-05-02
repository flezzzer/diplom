# app/db/crud/category.py

from sqlalchemy.orm import Session
from app.db.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

# Создание категории
def create_category(db: Session, category: CategoryCreate, seller_id: str):
    db_category = Category(
        name=category.name,
        description=category.description,
        seller_id=seller_id  # Привязка категории к продавцу
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Получение категории по id
def get_category(db: Session, category_id: str):
    return db.query(Category).filter(Category.id == category_id).first()

# Получение всех категорий
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()

# Обновление категории
def update_category(db: Session, category_id: str, category: CategoryUpdate, seller_id: str):
    db_category = db.query(Category).filter(Category.id == category_id, Category.seller_id == seller_id).first()
    if db_category:
        if category.name:
            db_category.name = category.name
        if category.description:
            db_category.description = category.description
        db.commit()
        db.refresh(db_category)
    return db_category

# Удаление категории
def delete_category(db: Session, category_id: str, seller_id: str):
    db_category = db.query(Category).filter(Category.id == category_id, Category.seller_id == seller_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
