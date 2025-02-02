from sqlalchemy.orm import Session
from app.db.models import Review
from app.schemas.reviews import ReviewCreate, ReviewUpdate

# Создание отзыва
def create_review(db: Session, review: ReviewCreate, user_id: int, product_id: int):
    db_review = Review(user_id=user_id, product_id=product_id, rating=review.rating, review_text=review.review_text)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# Получение всех отзывов для товара
def get_reviews_for_product(db: Session, product_id: int):
    return db.query(Review).filter(Review.product_id == product_id).all()


def get_review_by_id(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).all()

# Обновление отзыва
def update_review(db: Session, review_id: int, review: ReviewUpdate):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        if review.rating is not None:
            db_review.rating = review.rating
        if review.review_text:
            db_review.review_text = review.review_text
        db.commit()
        db.refresh(db_review)
    return db_review

# Удаление отзыва
def delete_review(db: Session, review_id: int):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review
