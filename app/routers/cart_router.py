from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_customer
from app.core.response import success_response, error_response
from app.db.database import get_db
from app.schemas.cart_schema import AddCartItem
from app.services import cart_service

router = APIRouter(
    prefix="/carts",
    tags=["Carts"]
)


@router.get("/open/{customer_id}")
def get_open_cart(customer_id: int, db: Session = Depends(get_db), current_user = Depends(require_customer)):
    cart = cart_service.get_open_cart(db, customer_id, current_user)

    if not cart:
        return error_response(message="Open cart not found", status_code=404)

    return success_response(data=cart)


@router.get("/{cart_id}/items")
def get_cart_items(cart_id: int, db: Session = Depends(get_db), current_user = Depends(require_customer)):
    items = cart_service.get_cart_items(db, cart_id, current_user)
    return success_response(data=items)


@router.post("/items")
def add_item_to_cart(data: AddCartItem, db: Session = Depends(get_db), current_user = Depends(require_customer)):
    try:
        item = cart_service.add_item_to_cart(db, data, current_user)
        return success_response(data=item, status_code=201)
    except ValueError as ex:
        return error_response(message=str(ex), status_code=400)
