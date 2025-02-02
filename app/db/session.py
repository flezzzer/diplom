from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from clickhouse_sqlalchemy import make_session, get_declarative_base
from app.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

Base = get_declarative_base()

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = make_session(engine)

def init_db():
    """Инициализация базы данных и создание всех таблиц."""
    try:
        Base.metadata.create_all(bind=engine)
        # Base.metadata.drop_all(bind=engine)
        logger.info("База данных инициализирована.")
    except Exception as e:
        logger.error(f"Ошибка инициализации базы данных: {str(e)}")
        raise

def get_db():
    """Функция для получения сессии для работы с базой данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
