import os
import redis.asyncio as redis
import sqlalchemy
import clickhouse_driver

DATABASE_URL = os.getenv("DATABASE_URL", "clickhouse://default:@clickhouse:8123/default")

DATABASE_URL_POSTGRES = os.getenv("DATABASE_URL_POSTGRES", "postgresql+asyncpg://postgres:postgres@postgres:5432/marketplace")

redis = redis.from_url("redis://redis_cache:6379", decode_responses=True)
