from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class OrderCreateFromCart(BaseModel):
    cart_id: int
    note: Optional[str] = None


class OrderDetailResponse(BaseModel):
    order_detail_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    discount: Decimal
    line_total: Decimal

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    order_id: int
    order_code: str
    user_id: Optional[int]
    customer_id: int
    order_date: datetime
    total_amount: Decimal
    status: str
    note: Optional[str]
    details: List[OrderDetailResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
