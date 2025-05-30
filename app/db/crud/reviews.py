from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.db.models import Review
from app.schemas.reviews import ReviewCreate, ReviewUpdate

async def create_review(db: AsyncSession, review: ReviewCreate, user_id: str, product_id: str):
    db_review = Review(
        user_id=user_id,
        product_id=product_id,
        rating=review.rating,
        review_text=review.review_text
    )
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

async def get_reviews_for_product(db: AsyncSession, product_id: str):
    result = await db.execute(select(Review).filter(Review.product_id == product_id))
    return result.scalars().all()

async def get_review_by_id(db: AsyncSession, review_id: str):
    result = await db.execute(select(Review).filter(Review.id == review_id))
    return result.scalars().first()

async def update_review(db: AsyncSession, review_id: str, review: ReviewUpdate):
    result = await db.execute(select(Review).filter(Review.id == review_id))
    db_review = result.scalars().first()
    if db_review:
        if review.rating is not None:
            db_review.rating = review.rating
        if review.review_text:
            db_review.review_text = review.review_text
        await db.commit()
        await db.refresh(db_review)
    return db_review

async def delete_review(db: AsyncSession, review_id: str):
    result = await db.execute(select(Review).filter(Review.id == review_id))
    db_review = result.scalars().first()
    if db_review:
        await db.delete(db_review)
        await db.commit()
    return db_review
