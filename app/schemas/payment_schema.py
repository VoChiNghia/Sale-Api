from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class PaymentCreate(BaseModel):
    order_id: int
    payment_method: str
    amount: Decimal
    payment_status: str = "SUCCESS"
    transaction_code: Optional[str] = None


class PaymentResponse(BaseModel):
    payment_id: int
    order_id: int
    payment_method: str
    amount: Decimal
    payment_status: str
    paid_at: Optional[datetime]
    transaction_code: Optional[str]

    class Config:
        from_attributes = True