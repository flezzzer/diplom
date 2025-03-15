# app/api/v1/statistics.py

from fastapi import APIRouter, Depends, HTTPException
from app.core.statistics import (
    get_total_products_count,
    get_total_orders_count,
    get_total_revenue,
    get_order_status_count
)

router = APIRouter(prefix="/sellers", tags=["Sellers"])

@router.get("/{seller_id}/statistics")
async def get_seller_statistics(seller_id: int):
    total_products = await get_total_products_count(seller_id)
    total_orders = await get_total_orders_count(seller_id)
    total_revenue = await get_total_revenue(seller_id)
    order_status_counts = await get_order_status_count(seller_id)

    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "order_status_counts": order_status_counts
    }
