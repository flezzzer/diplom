from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.reviews import ReviewCreate, ReviewUpdate
from app.db.crud.reviews import create_review, get_reviews_for_product, get_review_by_id, update_review, delete_review
from app.db.pg_session import get_pg_session
from app.core.auth import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewCreate)
async def create_new_review(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_pg_session),
    current_user: dict = Depends(get_current_user)
):
    return await create_review(db, user_id=current_user.id, review_data=review)

@router.get("/{review_id}", response_model=ReviewCreate)
async def read_review(
    review_id: str,
    db: AsyncSession = Depends(get_pg_session)
):
    review = await get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.get("/product/{product_id}", response_model=list[ReviewCreate])
async def read_reviews_by_product(
    product_id: str,
    db: AsyncSession = Depends(get_pg_session)
):
    return await get_reviews_for_product(db, product_id)

@router.put("/{review_id}")
async def update_review_info(
    review_id: str,
    review: ReviewUpdate,
    db: AsyncSession = Depends(get_pg_session),
    current_user: dict = Depends(get_current_user)
):
    return await update_review(db, review_id, review, current_user.id)

@router.delete("/{review_id}")
async def delete_review_by_id(
    review_id: str,
    db: AsyncSession = Depends(get_pg_session),
    current_user: dict = Depends(get_current_user)
):
    return await delete_review(db, review_id, current_user.id)
