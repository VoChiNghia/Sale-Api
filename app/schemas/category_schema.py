from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    category_name: str
    description: Optional[str] = None

class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class CategoryResponse(BaseModel):
    category_id: int
    category_name: str
    description: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
