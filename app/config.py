import os
import redis.asyncio as redis
import sqlalchemy
import clickhouse_driver

# Настройки подключения к базе данных ClickHouse
DATABASE_URL = os.getenv("DATABASE_URL", "clickhouse://default:@localhost:8123/default")

DATABASE_URL_POSTGRES = os.getenv("DATABASE_URL_POSTGRES", "postgresql+asyncpg://postgres:postgres@localhost:5432/marketplace")

redis = redis.from_url("redis://localhost", decode_responses=True)

