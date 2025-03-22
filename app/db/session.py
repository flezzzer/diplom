from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from clickhouse_sqlalchemy import make_session, get_declarative_base
from app.config import DATABASE_URL
import logging
import clickhouse_connect
from fastapi import Depends


def parse_database_url(url: str):
    scheme, rest = url.split("://")
    user_pass, host_port_db = rest.split("@")
    user, password = user_pass.split(":")
    host, port_db = host_port_db.split(":")
    port, database = port_db.split("/")
    return {
        "user": user,
        "password": password,
        "host": host,
        "port": int(port),
        "database": database
    }


# Получаем параметры подключения из DATABASE_URL
config = parse_database_url(DATABASE_URL)

# Создаем асинхронного клиента для ClickHouse
async_client = clickhouse_connect.get_client(
    host=config['host'],
    port=config['port'],
    username=config['user'],
    password=config['password'],
    database=config['database']
)


# Функция для получения асинхронного соединения
async def async_session():
    return async_client


logger = logging.getLogger(__name__)

Base = get_declarative_base()

# Создаем подключение к базе данных через SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)


# Функция для инициализации базы данных с учётом SET
def init_db():
    """Инициализация базы данных и создание всех таблиц."""
    try:
        # Выполняем команду SET через execute на асинхронном клиенте


        # Создание всех таблиц в базе данных
        # Base.metadata.drop_all(bind=engine)
        async_client.command("SET allow_create_index_without_type=1;")
        Base.metadata.create_all(bind=engine)
        logger.info("База данных инициализирована.")
    except Exception as e:
        logger.error(f"Ошибка инициализации базы данных: {str(e)}")
        raise


# Создаем сессии для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = make_session(engine)


# Функция для получения сессии для работы с базой данных
def get_db():
    """Функция для получения сессии для работы с базой данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
