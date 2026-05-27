from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ProductCreate(BaseModel):
    category_id: int
    product_name: str
    description: Optional[str] = None
    price: Decimal
    stock_quantity: int = 0
    image_url: Optional[str] = None


class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    product_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    image_url: Optional[str] = None
    status: Optional[str] = None


class ProductResponse(BaseModel):
    product_id: int
    category_id: int
    product_name: str
    description: Optional[str] = None
    price: Decimal
    stock_quantity: int
    image_url: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
