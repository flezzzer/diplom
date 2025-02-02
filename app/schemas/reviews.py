from pydantic import BaseModel
from typing import Optional
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
    id: int
    user_id: int
    product_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ReviewOut(ReviewInDB):
    pass

