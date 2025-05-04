from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Seller
from app.security import hash_password, verify_password
from app.schemas.sellers import SellerCreate, SellerUpdate, SellerLogin
import uuid

# Создание нового продавца
async def create_seller(db: AsyncSession, seller: SellerCreate):
    hashed_password = hash_password(seller.password)  # Хэшируем пароль перед сохранением
    db_seller = Seller(
        name=seller.name,
        email=seller.email,
        password=hashed_password,
        username=seller.username,
        # phone=seller.phone,
        # address=seller.address
    )
    db.add(db_seller)
    await db.commit()
    await db.refresh(db_seller)
    return db_seller

# Функция для аутентификации продавца (проверка логина и пароля)
async def authenticate_seller(db: AsyncSession, seller: SellerLogin):
    result = await db.execute(select(Seller).filter(Seller.email == seller.email))
    db_seller = result.scalars().first()
    if not db_seller or not verify_password(seller.password, db_seller.password):
        return None
    return db_seller

# Получение продавца по id
async def get_seller(db: AsyncSession, seller_id: uuid.UUID):
    result = await db.execute(select(Seller).filter(Seller.id == seller_id))
    return result.scalars().first()

# Получение продавца по email
async def get_seller_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Seller).filter(Seller.email == email))
    return result.scalars().first()

# Получение всех продавцов
async def get_sellers(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Seller).offset(skip).limit(limit))
    return result.scalars().all()

# Обновление данных продавца
async def update_seller(db: AsyncSession, seller_id: uuid.UUID, seller: SellerUpdate):
    result = await db.execute(select(Seller).filter(Seller.id == seller_id))
    db_seller = result.scalars().first()
    if db_seller:
        if seller.name:
            db_seller.name = seller.name
        if seller.email:
            db_seller.email = seller.email
        if seller.phone:
            db_seller.phone = seller.phone
        if seller.address:
            db_seller.address = seller.address
        await db.commit()
        await db.refresh(db_seller)
    return db_seller

# Удаление продавца
async def delete_seller(db: AsyncSession, seller_id: uuid.UUID):
    result = await db.execute(select(Seller).filter(Seller.id == seller_id))
    db_seller = result.scalars().first()
    if db_seller:
        await db.delete(db_seller)
        await db.commit()
    return db_seller
