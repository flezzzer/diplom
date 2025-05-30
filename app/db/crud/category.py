from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from fastapi import HTTPException

# Создание категории
async def create_category(db: AsyncSession, category: CategoryCreate, seller_id: str):
    db_category = Category(
        name=category.name,
        description=category.description,
        seller_id=seller_id
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_category(db: AsyncSession, category_id: str):
    result = await db.execute(select(Category).filter(Category.id == category_id))
    return result.scalars().first()

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()

async def update_category(db: AsyncSession, category_id: str, category: CategoryUpdate, seller_id: str):
    result = await db.execute(select(Category).filter(Category.id == category_id, Category.seller_id == seller_id))
    db_category = result.scalars().first()
    if db_category:
        if category.name:
            db_category.name = category.name
        if category.description:
            db_category.description = category.description
        await db.commit()
        await db.refresh(db_category)
    return db_category

async def delete_category(db: AsyncSession, category_id: str, seller_id: str):
    result = await db.execute(select(Category).filter(Category.id == category_id, Category.seller_id == seller_id))
    db_category = result.scalars().first()
    if db_category:
        await db.delete(db_category)
        await db.commit()
    return db_category
