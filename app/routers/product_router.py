from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_staff_or_admin
from app.core.response import success_response, error_response
from app.db.database import get_db
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services import product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = product_service.get_products(db)
    return success_response(data=products)


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)

    if not product:
        return error_response(message="Product not found", status_code=404)

    return success_response(data=product)


@router.post("/")
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_staff_or_admin)
):
    product = product_service.create_product(db, data)
    return success_response(data=product, status_code=201)


@router.put("/{product_id}")
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_staff_or_admin)
):
    product = product_service.update_product(db, product_id, data)

    if not product:
        return error_response(message="Product not found", status_code=404)

    return success_response(data=product)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user = Depends(require_staff_or_admin)):
    success = product_service.delete_product(db, product_id)

    if not success:
        return error_response(message="Product not found", status_code=404)

    return success_response(message="Product deleted")
