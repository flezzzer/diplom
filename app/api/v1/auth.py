from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserRegister, UserLogin, UserBase
from app.db.crud.user import create_user, get_user_by_email
from app.db.pg_session import get_pg_session
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserBase)
async def register(user: UserRegister, db: AsyncSession = Depends(get_pg_session)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = await create_user(db, user)
    return new_user

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_pg_session)):
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"id": str(db_user.id), "email": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
