from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserBase
from app.db.crud.user import get_user
from app.db.pg_session import get_pg_session  # Импортируем get_pg_session
from app.core.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserBase)
async def read_user_me(db: AsyncSession = Depends(get_pg_session), current_user: dict = Depends(get_current_user)):  # Используем get_pg_session
    return await get_user(db, current_user.id)
