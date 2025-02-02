from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt

# Конфигурация JWT
SECRET_KEY = "supersecretkey"  # Поменяй на более надежный ключ!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Срок действия токена

# Настройка шифрования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для хеширования пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Функция для генерации JWT-токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Функция для декодирования JWT-токена (не используется в этом файле, но нужна в `auth.py`)
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
