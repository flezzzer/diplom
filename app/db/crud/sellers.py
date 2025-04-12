from sqlalchemy.orm import Session
from app.db.models import Seller
from app.security import hash_password, verify_password
from app.schemas.sellers import SellerCreate, SellerUpdate, SellerLogin
import uuid

# Создание нового продавца
def create_seller(db: Session, seller: SellerCreate):
    hashed_password = hash_password(seller.password)  # Хэшируем пароль перед сохранением
    db_seller = Seller(
        name=seller.name,
        email=seller.email,
        password=hashed_password,
        # phone=seller.phone,
        # address=seller.address
    )
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

# Функция для аутентификации продавца (проверка логина и пароля)
def authenticate_seller(db: Session, seller: SellerLogin):
    db_seller = db.query(Seller).filter(Seller.email == seller.email).first()
    if not db_seller or not verify_password(seller.password, db_seller.password):
        return None
    return db_seller

# Получение продавца по id
def get_seller(db: Session, seller_id: uuid.UUID):
    return db.query(Seller).filter(Seller.id == seller_id).first()

# Получение продавца по email
def get_seller_by_email(db: Session, email: str):
    return db.query(Seller).filter(Seller.email == email).first()

# Получение всех продавцов
def get_sellers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Seller).offset(skip).limit(limit).all()

# Обновление данных продавца
def update_seller(db: Session, seller_id: uuid.UUID, seller: SellerUpdate):
    db_seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if db_seller:
        if seller.name:
            db_seller.name = seller.name
        if seller.email:
            db_seller.email = seller.email
        if seller.phone:
            db_seller.phone = seller.phone
        if seller.address:
            db_seller.address = seller.address
        db.commit()
        db.refresh(db_seller)
    return db_seller

# Удаление продавца
def delete_seller(db: Session, seller_id: uuid.UUID):
    db_seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if db_seller:
        db.delete(db_seller)
        db.commit()
    return db_seller
