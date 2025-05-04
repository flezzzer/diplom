from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.db.pg_session import get_pg_session
from app.db.crud.user import get_user
from app.db.crud.sellers import get_seller
from app.security import SECRET_KEY, ALGORITHM

# Используем OAuth2 Password Bearer (токен передается в заголовке Authorization)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Функция для получения текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_pg_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Декодируем JWT-токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Получаем пользователя из базы
    user = await get_user(db, user_id)
    if user is None:
        raise credentials_exception

    return user  # Возвращаем объект пользователя (User)


# Функция для получения текущего продавца
async def get_current_seller(token: str = Depends(oauth2_scheme), db: Session = Depends(get_pg_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Декодируем JWT-токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        seller_id: int = payload.get("id")
        if seller_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Получаем продавца из базы
    seller = await get_seller(db, seller_id)
    if seller is None:
        raise credentials_exception

    return seller  # Возвращаем объект продавца (Seller)
