import os

# Настройки подключения к базе данных ClickHouse
DATABASE_URL = os.getenv("DATABASE_URL", "clickhouse://default:@localhost:8123/default")
