from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.users import UserBase
from app.db.crud.user import get_user
from app.db.session import get_db
from app.core.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserBase)
def read_user_me(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_user(db, current_user["id"])
