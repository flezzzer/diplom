import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

# URL базы данных PostgreSQL
from app.config import DATABASE_URL_POSTGRES

DATABASE_URL = DATABASE_URL_POSTGRES

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_pg_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    from app.db.models import User, Product, Order, Seller, Category, Review, Cart, OrderItem, CartProduct

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def execute_query(query, session: AsyncSession):
    try:
        result = await session.execute(query)
        await session.commit()
        return result
    except SQLAlchemyError as e:
        await session.rollback()
        raise e
