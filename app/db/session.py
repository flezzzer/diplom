import clickhouse_connect
import logging
import os

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "clickhouse")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT", "8123")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "default")


# Функция для подключения к ClickHouse
def get_clickhouse_client():
    """
    Возвращает клиент для работы с ClickHouse.
    """
    client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE
    )
    return client


def init_db():
    """
    Инициализирует ClickHouse: создает базу данных и таблицы, если их нет.
    """
    try:
        import logging
        import clickhouse_connect

        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD
        )

        client.command(f"CREATE DATABASE IF NOT EXISTS {CLICKHOUSE_DATABASE}")
        client.command(f"USE {CLICKHOUSE_DATABASE}")

        client.command("""
        CREATE TABLE IF NOT EXISTS users (
            id String,
            username String,
            email String,
            hashed_password String,
            created_at DateTime,
            updated_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY id;
        """)

        client.command("""
        CREATE TABLE IF NOT EXISTS categories (
            id String,
            name String,
            description String,
            seller_id String,
            updated_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY id;
        """)

        client.command("""
        CREATE TABLE IF NOT EXISTS products (
            id String,
            name String,
            description String,
            price Float32,
            category_id String,
            seller_id String,
            created_at DateTime,
            updated_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY id;
        """)

        client.command("""
        CREATE TABLE IF NOT EXISTS sellers (
            id String,
            username String,
            password String,
            name String,
            email String,
            phone String,
            address String,
            updated_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY id;
        """)

        client.command("""
        CREATE TABLE IF NOT EXISTS carts (
            id String,
            user_id String,
            updated_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY id;
        """)

        client.command("""
        CREATE TABLE IF NOT EXISTS cart_products (
            id String,
            cart_id String,
            product_id String,
            quantity Float32,
            price Float32,
            updated_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY id;
        """)

        client.command("""
        CREATE TABLE IF NOT EXISTS orders (
            id String,
            user_id String,
            total_price Float32,
            status String,
            updated_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY id;
        """)

        client.command("""
        CREATE TABLE IF NOT EXISTS order_items (
            id String,
            order_id String,
            product_id String,
            quantity Float32,
            price Float32,
            updated_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY id;
        """)

        client.command("""
        CREATE TABLE IF NOT EXISTS reviews (
            id String,
            user_id String,
            product_id String,
            rating Float32,
            review_text String,
            created_at DateTime,
            updated_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY id;
        """)

        logging.info("ClickHouse база данных и таблицы успешно инициализированы.")

    except Exception as e:
        logging.error(f"Ошибка инициализации базы данных ClickHouse: {e}")
        raise



def get_clickhouse_session():
    """
    Функция для получения синхронной сессии для работы с ClickHouse.
    """
    try:
        client = get_clickhouse_client()
        yield client
    finally:
        pass
