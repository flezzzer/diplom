from fastapi import APIRouter, Depends
from statistics import mean, median
import numpy as np
from app.db.async_session import get_clickhouse_client
from app.core.statistics import (
    get_total_products_count,
    get_total_orders_count,
    get_total_revenue,
    get_order_status_count,
    get_category_statistics,
    get_product_statistics,
    get_order_statistics_by_date,
    get_total_product_views,            # Реализовать при необходимости
    get_product_counts_by_date          # Реализовать при необходимости
)

router = APIRouter(prefix="/sellers", tags=["Sellers"])

@router.get("/{seller_id}/revenue-trend")
async def get_revenue_trend(seller_id: str):
    stats = await get_order_statistics_by_date(seller_id)
    stats = sorted(stats, key=lambda x: x['date'])

    trend = []
    for i in range(1, len(stats)):
        prev = stats[i - 1]['total_revenue']
        curr = stats[i]['total_revenue']
        growth = ((curr - prev) / prev * 100) if prev else 0
        trend.append({
            "date": stats[i]["date"],
            "revenue": curr,
            "growth_percent": round(growth, 2)
        })
    return trend

@router.get("/{seller_id}/average-order-value")
async def get_average_order_value(seller_id: str):
    orders = await get_order_statistics_by_date(seller_id)
    revenues = [day["total_revenue"] / day["order_count"] for day in orders if day["order_count"] > 0]
    if not revenues:
        return {"average_order_value": 0, "median_order_value": 0}
    return {
        "average_order_value": round(mean(revenues), 2),
        "median_order_value": round(median(revenues), 2)
    }

@router.get("/{seller_id}/conversion-rate")
async def get_conversion_rate(seller_id: str):
    total_orders = await get_total_orders_count(seller_id)
    total_views = await get_total_product_views(seller_id)  # Реализовать отдельно
    conversion = (total_orders / total_views * 100) if total_views else 0
    return {"conversion_rate_percent": round(conversion, 2)}

@router.get("/{seller_id}/top-products")
async def get_top_selling_products(seller_id: str):
    stats = await get_product_statistics(seller_id)
    sorted_stats = sorted(stats, key=lambda x: x["revenue"], reverse=True)
    top_5 = sorted_stats[:5]
    total_revenue = sum(p["revenue"] for p in stats)
    for p in top_5:
        p["revenue_share_percent"] = round((p["revenue"] / total_revenue * 100), 2) if total_revenue else 0
    return top_5

@router.get("/{seller_id}/order-product-correlation")
async def get_order_product_correlation(seller_id: str):
    orders_by_day = await get_order_statistics_by_date(seller_id)
    product_counts_by_day = await get_product_counts_by_date(seller_id)  # Реализовать отдельно

    if len(orders_by_day) != len(product_counts_by_day):
        return {"error": "Дата-сеты не совпадают по длине"}

    orders = [day["order_count"] for day in orders_by_day]
    products = [day["product_count"] for day in product_counts_by_day]

    correlation = float(np.corrcoef(orders, products)[0, 1])
    return {"correlation_orders_products": round(correlation, 2)}
