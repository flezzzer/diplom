from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.reviews import ReviewCreate, ReviewUpdate
from app.db.crud.reviews import create_review, get_reviews_for_product, get_review_by_id, update_review, delete_review
from app.db.session import get_db
from app.core.auth import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewCreate)
def create_new_review(review: ReviewCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_review(db, user_id=current_user.id, review_data=review)

@router.get("/{review_id}", response_model=ReviewCreate)
def read_review(review_id: str, db: Session = Depends(get_db)):
    review = get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.get("/product/{product_id}", response_model=list[ReviewCreate])
def read_reviews_by_product(product_id: str, db: Session = Depends(get_db)):
    return get_reviews_for_product(db, product_id)

@router.put("/{review_id}")
def update_review_info(review_id: str, review: ReviewUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return update_review(db, review_id, review, current_user.id)

@router.delete("/{review_id}")
def delete_review_by_id(review_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return delete_review(db, review_id, current_user.id)
