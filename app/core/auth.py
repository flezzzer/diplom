from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.db.session import get_db
from app.db.crud.user import get_user
from app.db.crud.sellers import get_seller
from app.security import SECRET_KEY, ALGORITHM

# Используем OAuth2 Password Bearer (токен передается в заголовке Authorization)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Функция для получения текущего пользователя
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    user = get_user(db, user_id)
    if user is None:
        raise credentials_exception

    return user  # Возвращаем объект пользователя (User)


def get_current_seller(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        seller_id: int = payload.get("seller_id")
        if seller_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    seller = get_seller(db, seller_id)
    if seller is None:
        raise credentials_exception
    return seller
