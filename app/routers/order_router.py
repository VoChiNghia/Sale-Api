from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.order_schema import OrderCreateFromCart
from app.core.auth import get_current_user, require_customer
from app.core.response import success_response, error_response
from app.services import order_service

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/create-from-cart")
def create_order_from_cart(data: OrderCreateFromCart, db: Session = Depends(get_db), current_user = Depends(require_customer)):
    try:
        order = order_service.create_order_from_cart(
            db=db,
            cart_id=data.cart_id,
            note=data.note,
            current_user=current_user
        )
        return success_response(data=order, status_code=201)
    except Exception as e:
        return error_response(message=str(e), status_code=400)


@router.get("/")
def get_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    orders = order_service.get_orders(db, current_user=current_user)
    return success_response(data=orders)


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = order_service.get_order_by_id(
        db,
        order_id,
        current_user=current_user
    )

    if not order:
        return error_response(message="Không tìm thấy đơn hàng", status_code=404)

    return success_response(data=order)
