import os
from aiohttp import ClientSession
from aiochclient import ChClient
from contextlib import asynccontextmanager
from urllib.parse import urlparse
from app.config import DATABASE_URL

@asynccontextmanager
async def get_clickhouse_client():
    parsed = urlparse(DATABASE_URL)
    host = f"http://{parsed.hostname}:{parsed.port or 8123}"
    user = parsed.username or "default"
    password = parsed.password or ""
    database = parsed.path.lstrip("/") or "default"

    async with ClientSession() as session:
        client = ChClient(session, url=host, user=user, password=password, database=database)
        yield client
