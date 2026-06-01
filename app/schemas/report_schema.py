from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ReportDateRange(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class SalesOverviewResponse(BaseModel):
    total_orders: int
    paid_orders: int
    pending_orders: int
    cancelled_orders: int
    total_revenue: Decimal
    average_order_value: Decimal
    total_customers: int
    total_products: int
    low_stock_products: int


class RevenueByDayResponse(BaseModel):
    report_date: date
    order_count: int
    revenue: Decimal


class TopProductResponse(BaseModel):
    product_id: int
    product_name: str
    quantity_sold: int
    revenue: Decimal


class TopCustomerResponse(BaseModel):
    customer_id: int
    full_name: str
    order_count: int
    total_spent: Decimal


class LowStockProductResponse(BaseModel):
    product_id: int
    product_name: str
    category_name: str
    stock_quantity: int
    price: Decimal
