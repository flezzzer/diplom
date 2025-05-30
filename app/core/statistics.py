from aiochclient import ChClient
from aiohttp import ClientSession
from typing import Dict
from app.db.async_session import get_clickhouse_client
from app.config import redis
import hashlib
import json

async def cache_query(query_key: str, query_func, *args) -> dict:
    cached_data = await redis.get(query_key)
    if cached_data:
        return json.loads(cached_data)  # Возвращаем данные из кеша

    result = await query_func(*args)

    await redis.set(query_key, json.dumps(result), ex=60)  # Данные будут храниться 60 секунд
    return result

async def get_total_products_count(seller_id: str) -> int:
    async def query_func():
        async with get_clickhouse_client() as client:
            query = f"""
                SELECT count() AS product_count
                FROM products
                WHERE seller_id = '{seller_id}'
            """
            row = await client.fetchrow(query)
            return {"product_count": row["product_count"]}

    query_key = f"total_products_count:{seller_id}"
    return await cache_query(query_key, query_func)

async def get_total_orders_count(seller_id: str) -> int:
    async def query_func():
        async with get_clickhouse_client() as client:
            query = f"""
                SELECT count(DISTINCT oi.order_id) AS order_count
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE p.seller_id = '{seller_id}'
            """
            row = await client.fetchrow(query)
            return {"order_count": row["order_count"]}

    query_key = f"total_orders_count:{seller_id}"
    return await cache_query(query_key, query_func)

async def get_total_revenue(seller_id: str) -> float:
    async def query_func():
        async with get_clickhouse_client() as client:
            query = f"""
                SELECT sum(oi.price * oi.quantity) AS total_revenue
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE p.seller_id = '{seller_id}'
            """
            row = await client.fetchrow(query)
            return {"total_revenue": float(row["total_revenue"] or 0)}

    query_key = f"total_revenue:{seller_id}"
    return await cache_query(query_key, query_func)

async def get_order_status_count(seller_id: str) -> Dict[str, int]:
    async def query_func():
        async with get_clickhouse_client() as client:
            query = f"""
                SELECT o.status AS status, count(DISTINCT o.id) AS count
                FROM orders o
                JOIN order_items oi ON o.id = oi.order_id
                JOIN products p ON oi.product_id = p.id
                WHERE p.seller_id = '{seller_id}'
                GROUP BY o.status
            """
            rows = await client.fetch(query)
            counts = {"pending": 0, "completed": 0, "cancelled": 0}
            for row in rows:
                counts[row["status"]] = row["count"]
            return counts

    query_key = f"order_status_count:{seller_id}"
    return await cache_query(query_key, query_func)

async def get_category_statistics(seller_id: str) -> Dict[str, Dict[str, int]]:
    async def query_func():
        async with get_clickhouse_client() as client:
            query = f"""
                SELECT
                    c.name AS category_name,
                    count(DISTINCT p.id) AS product_count,
                    count(DISTINCT oi.order_id) AS order_count,
                    sum(oi.price * oi.quantity) AS revenue
                FROM categories c
                JOIN products p ON p.category_id = c.id
                LEFT JOIN order_items oi ON p.id = oi.product_id
                WHERE p.seller_id = '{seller_id}'
                GROUP BY c.name
                ORDER BY revenue DESC
            """
            rows = await client.fetch(query)
            category_stats = {}
            for row in rows:
                category_stats[row["category_name"]] = {
                    "product_count": row["product_count"],
                    "order_count": row["order_count"],
                    "revenue": row["revenue"]
                }
            return category_stats

    query_key = f"category_statistics:{seller_id}"
    return await cache_query(query_key, query_func)

async def get_product_statistics(seller_id: str) -> Dict[str, Dict[str, int]]:
    async def query_func():
        async with get_clickhouse_client() as client:
            query = f"""
                SELECT
                    p.name AS product_name,
                    count(DISTINCT oi.order_id) AS orders,
                    sum(oi.quantity) AS units_sold,
                    sum(oi.price * oi.quantity) AS revenue,
                    round(
                        100 * sum(oi.price * oi.quantity) /
                        sum(sum(oi.price * oi.quantity)) OVER (), 2
                    ) AS revenue_percent
                FROM products p
                LEFT JOIN order_items oi ON p.id = oi.product_id
                WHERE p.seller_id = '{seller_id}'
                GROUP BY p.id, p.name
                ORDER BY revenue DESC
            """
            rows = await client.fetch(query)
            product_stats = {}
            for row in rows:
                product_stats[row["product_name"]] = {
                    "orders": row["orders"],
                    "units_sold": row["units_sold"],
                    "revenue": row["revenue"],
                    "revenue_percent": row["revenue_percent"]
                }
            return product_stats

    query_key = f"product_statistics:{seller_id}"
    return await cache_query(query_key, query_func)

async def get_order_statistics_by_date(seller_id: str) -> Dict[str, Dict[str, int]]:
    async def query_func():
        async with get_clickhouse_client() as client:
            query = f"""
                SELECT
                    toStartOfDay(o.updated_at) AS order_date,
                    count(DISTINCT o.id) AS order_count,
                    sum(oi.price * oi.quantity) AS revenue
                FROM orders o
                JOIN order_items oi ON o.id = oi.order_id
                JOIN products p ON oi.product_id = p.id
                WHERE p.seller_id = '{seller_id}'
                GROUP BY order_date
                ORDER BY order_date
            """
            rows = await client.fetch(query)
            order_stats_by_date = {}
            for row in rows:
                order_stats_by_date[str(row["order_date"])] = {
                    "order_count": row["order_count"],
                    "revenue": row["revenue"]
                }
            return order_stats_by_date

    query_key = f"order_statistics_by_date:{seller_id}"
    return await cache_query(query_key, query_func)

async def get_total_product_views(seller_id: str) -> int:
    async def query_func():
        async with get_clickhouse_client() as client:
            query = f"""
                SELECT count(*) AS view_count
                FROM product_views
                WHERE seller_id = '{seller_id}'
            """
            row = await client.fetchrow(query)
            return {"view_count": row["view_count"]}

    query_key = f"total_product_views:{seller_id}"
    result = await cache_query(query_key, query_func)
    return result["view_count"]

async def get_product_counts_by_date(seller_id: str) -> list:
    async def query_func():
        async with get_clickhouse_client() as client:
            query = f"""
                SELECT
                    toDate(updated_at) AS date,
                    count() AS product_count
                FROM products
                WHERE seller_id = '{seller_id}'
                GROUP BY date
                ORDER BY date
            """
            rows = await client.fetch(query)
            return [
                {
                    "date": str(row["date"]),
                    "product_count": row["product_count"]
                }
                for row in rows
            ]

    query_key = f"product_counts_by_date:{seller_id}"
    return await cache_query(query_key, query_func)


