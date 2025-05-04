from celery import Celery
from datetime import datetime, timedelta
from sqlalchemy.future import select
from .session import get_clickhouse_client
from .pg_session import get_pg_session
import logging

# Создаем объект Celery
app = Celery('tasks', broker='redis://localhost:6379/0')

# Задача для синхронизации данных из PostgreSQL в ClickHouse
@app.task
def sync_postgres_to_clickhouse():
    """Задача для синхронизации данных между PostgreSQL и ClickHouse."""

    # Время последней синхронизации (например, 5 минут назад)
    last_sync_time = datetime.utcnow() - timedelta(minutes=5)

    # Получаем сессию PostgreSQL (синхронно)
    session = get_pg_session()  # сделаем синхронным
    try:
        # Получаем данные из PostgreSQL за последние 5 минут для всех таблиц
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

            # Запрос для получения данных за последние 5 минут
            query = f"""
            SELECT * FROM {table}
            WHERE updated_at >= :last_sync_time
            """
            result = session.execute(query, {'last_sync_time': last_sync_time})
            data = result.fetchall()

            if data:
                # Получаем клиент ClickHouse
                clickhouse_client = get_clickhouse_client()

                # Вставляем данные в ClickHouse
                insert_query = f"INSERT INTO {table} VALUES"
                clickhouse_client.execute(insert_query, data)
                logging.info(f"Данные из таблицы {table} успешно вставлены в ClickHouse.")
            else:
                logging.info(f"Нет новых данных для таблицы {table}.")

    except Exception as e:
        logging.error(f"Ошибка синхронизации данных для PostgreSQL в ClickHouse: {e}")
        raise e
