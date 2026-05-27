from pydantic import BaseModel
from typing import Optional


class CartCreate(BaseModel):
    customer_id: int


class AddCartItem(BaseModel):
    customer_id: int
    product_id: int
    quantity: int


class CartItemResponse(BaseModel):
    cart_item_id: int
    cart_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    cart_id: int
    customer_id: int
    status: str

    class Config:
        from_attributes = True