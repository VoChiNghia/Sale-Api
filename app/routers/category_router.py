from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_admin
from app.core.response import success_response, error_response
from app.db.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.services import category_service

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    categories = category_service.get_categories(db)
    return success_response(data=categories)


@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = category_service.get_category(db, category_id)

    if not category:
        return error_response(message="Category not found", status_code=404)
    return success_response(data=category)


@router.post("/")
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    category = category_service.create_category(db, data)
    return success_response(data=category, status_code=201)


@router.put("/{category_id}")
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    category = category_service.update_category(db, category_id, data)

    if not category:
        return error_response(message="Category not found", status_code=404)

    return success_response(data=category)


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    success = category_service.delete_category(db, category_id)

    if not success:
        return error_response(message="Category not found", status_code=404)

    return success_response(message="Category deleted")
