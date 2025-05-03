from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from clickhouse_sqlalchemy import make_session, get_declarative_base
from app.config import DATABASE_URL
import logging
import clickhouse_connect
from contextlib import contextmanager
from fastapi import Depends

# Парсим строку подключения к базе данных
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

# Инициализируем синхронный клиент ClickHouse
bootstrap_client = clickhouse_connect.get_client(
    host=config['host'],
    port=config['port'],
    username=config['user'],
    password=config['password'],
    # Без database= для начальной инициализации
)

# 2. Создаём базу, если нужно
bootstrap_client.command("CREATE DATABASE IF NOT EXISTS default")

# Создаем подключение для основной базы данных (ClickHouse)
sync_client = clickhouse_connect.get_client(
    host=config['host'],
    port=config['port'],
    username=config['user'],
    password=config['password'],
    database=config['database']
)

# Создаем движок SQLAlchemy для синхронной работы
engine = create_engine(DATABASE_URL, echo=True)

# Создаем сессию SQLAlchemy для синхронных операций
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Сессия для работы с ClickHouse
session = make_session(engine)

# Определяем Base для SQLAlchemy
Base = get_declarative_base()

# Инициализация базы данных
def init_db():
    """Инициализация базы данных и создание всех таблиц."""
    try:
        # Создание базы, если её нет
        bootstrap_client.command("CREATE DATABASE IF NOT EXISTS default")
        # Выполняем команды для настройки базы
        bootstrap_client.command("SET allow_create_index_without_type=1;")
        # Создание всех таблиц
        Base.metadata.create_all(bind=engine)
        logging.info("База данных инициализирована.")
    except Exception as e:
        logging.error(f"Ошибка инициализации базы данных: {str(e)}")
        raise

# Функция для получения сессии SQLAlchemy
def get_db():
    """Функция для получения синхронной сессии для работы с базой данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для получения сессии для ClickHouse
def get_clickhouse_session():
    """Функция для получения сессии для работы с ClickHouse."""
    try:
        yield session
    finally:
        pass  # Пока не нужно закрывать сессию для clickhouse_connect
