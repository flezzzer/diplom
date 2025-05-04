from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.db.models import Product
from app.schemas.products import ProductCreate, ProductUpdate

# Создание нового продукта
async def create_product(db: AsyncSession, product: ProductCreate, seller_id: str):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
        seller_id=seller_id  # Привязка к продавцу
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Получение продукта по id
async def get_product(db: AsyncSession, product_id: str):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    return result.scalars().first()

# Получение всех продуктов
async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()

# Обновление данных продукта
async def update_product(db: AsyncSession, product_id: str, product: ProductUpdate, seller_id: str):
    result = await db.execute(select(Product).filter(Product.id == product_id, Product.seller_id == seller_id))
    db_product = result.scalars().first()
    if db_product:
        if product.name:
            db_product.name = product.name
        if product.description:
            db_product.description = product.description
        if product.price:
            db_product.price = product.price
        await db.commit()
        await db.refresh(db_product)
    return db_product

# Удаление продукта
async def delete_product(db: AsyncSession, product_id: str, seller_id: str):
    result = await db.execute(select(Product).filter(Product.id == product_id, Product.seller_id == seller_id))
    db_product = result.scalars().first()
    if db_product:
        await db.delete(db_product)
        await db.commit()
    return db_product
