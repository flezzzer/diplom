from datetime import datetime, timedelta
from sqlalchemy.future import select
from .session import get_clickhouse_session
from .pg_session import get_pg_session
import logging
# from app.db.session import get_pg_session, get_clickhouse_client
from app.celery_app import celery
import asyncio
from sqlalchemy import text
from asgiref.sync import sync_to_async

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@celery.task
def sync_postgres_to_clickhouse():
    """Задача для синхронизации данных между PostgreSQL и ClickHouse."""
    last_sync_time = datetime.utcnow() - timedelta(minutes=1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(sync_data(last_sync_time))


from clickhouse_driver import Client

from clickhouse_driver import Client
import os

def get_clickhouse_client():
    return Client(
        host=os.getenv("CLICKHOUSE_HOST", "clickhouse"),
        port=int(os.getenv("CLICKHOUSE_PORT", 9000)),
        user=os.getenv("CLICKHOUSE_USER", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD", ""),
        database=os.getenv("CLICKHOUSE_DB", "default")
    )


from asyncpg.pgproto.pgproto import UUID as PG_UUID
import uuid
def clean_data(data):
    cleaned = []
    for row in data:
        cleaned_row = {}
        for column, value in row._mapping.items():
            if value is None:
                cleaned_row[column] = ''
            elif isinstance(value, uuid.UUID):
                cleaned_row[column] = str(value)
            elif column == 'price' or column == 'total_price':
                cleaned_row[column] = float(value) if value is not None else 0.0
            else:
                cleaned_row[column] = value
        cleaned.append(cleaned_row)
    return cleaned



async def sync_data(last_sync_time):
    """Асинхронная функция для синхронизации данных с PostgreSQL в ClickHouse."""
    try:
        async for session in get_pg_session():  # используем async for
            tables = [
                'cart_products',
                'carts',
                'categories',
                'order_items',
                'orders',
                'products',
                'reviews',
                'sellers',
                'users'
            ]

            for table in tables:
                logging.info(f"Обрабатываем таблицу {table}.")

                query = text(f"""
                SELECT * FROM {table}
                WHERE updated_at >= :last_sync_time
                """)
                result = await session.execute(query, {'last_sync_time': last_sync_time})
                data = result.fetchall()

                if data:
                    clickhouse_client = get_clickhouse_client()

                    data = clean_data(data)

                    insert_query = f"INSERT INTO {table} VALUES"
                    clickhouse_client.execute(insert_query, data)
                    logging.info(f"Данные из таблицы {table} успешно вставлены в ClickHouse.")
                else:
                    logging.info(f"Нет новых данных для таблицы {table}.")
    except Exception as e:
        logging.error(f"Ошибка синхронизации данных для PostgreSQL в ClickHouse: {e}")
        raise e

