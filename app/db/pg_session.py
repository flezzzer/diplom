import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

# URL базы данных PostgreSQL
from app.config import DATABASE_URL_POSTGRES

DATABASE_URL = DATABASE_URL_POSTGRES

# Создание асинхронного движка для подключения
engine = create_async_engine(DATABASE_URL, echo=True)

# Сессия для работы с БД
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс для всех моделей
Base = declarative_base()

# Dependency для FastAPI
async def get_pg_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Функция для инициализации базы данных (создание таблиц)
async def init_db():
    # Импортируем модели
    from app.db.models import User, Product, Order, Seller, Category, Review, Cart, OrderItem, CartProduct

    async with engine.begin() as conn:
        # Создаем все таблицы в базе данных, если они не существуют
        await conn.run_sync(Base.metadata.create_all)

# Функция для работы с транзакциями
async def execute_query(query, session: AsyncSession):
    try:
        # Выполнение запроса
        result = await session.execute(query)
        await session.commit()
        return result
    except SQLAlchemyError as e:
        # Если ошибка, откатываем транзакцию
        await session.rollback()
        raise e
