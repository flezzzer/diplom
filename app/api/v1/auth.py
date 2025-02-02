from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.users import UserRegister, UserLogin, UserBase
from app.db.crud.user import create_user, get_user_by_email
from app.db.session import get_db
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserBase)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user)
    return new_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"id": db_user.id, "email": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
