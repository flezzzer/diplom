from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User
from app.schemas.users import UserRegister, UserUpdate
from app.security import hash_password, verify_password

# Создание пользователя
async def create_user(db: AsyncSession, user: UserRegister):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()  # Асинхронный коммит
    await db.refresh(db_user)  # Асинхронное обновление объекта
    return db_user

# Получение пользователя по id
async def get_user(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

# Получение пользователя по email
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

# Получение всех пользователей
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

# Обновление пользователя
async def update_user(db: AsyncSession, user_id: str, user: UserUpdate):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        if user.username:
            db_user.username = user.username
        if user.email:
            db_user.email = user.email
        if user.full_name:
            db_user.full_name = user.full_name
        if user.is_active is not None:
            db_user.is_active = user.is_active
        await db.commit()  # Асинхронный коммит
        await db.refresh(db_user)  # Асинхронное обновление объекта
    return db_user

# Удаление пользователя
async def delete_user(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        await db.delete(db_user)
        await db.commit()  # Асинхронный коммит
    return db_user
