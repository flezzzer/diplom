import os
import redis.asyncio as redis
import sqlalchemy
import clickhouse_driver

# Настройки подключения к базе данных ClickHouse
DATABASE_URL = os.getenv("DATABASE_URL", "clickhouse://default:@localhost:8123/default")

redis = redis.from_url("redis://localhost", decode_responses=True)

