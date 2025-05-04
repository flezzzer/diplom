from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ReviewBase(BaseModel):
    rating: float
    review_text: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    rating: Optional[float] = None
    review_text: Optional[str] = None

class ReviewInDB(ReviewBase):
    id: UUID  # Используем UUID для id
    user_id: UUID  # Используем UUID для user_id
    product_id: UUID  # Используем UUID для product_id
    created_at: datetime

    class Config:
        orm_mode = True

class ReviewOut(ReviewInDB):
    pass
