from sqlalchemy.orm import Session
from app.repositories import order_repository


def create_order_from_cart(
    db: Session,
    cart_id: int,
    note: str | None = None,
    current_user=None
):
    user_role = (
        current_user.role.strip().upper()
        if current_user and current_user.role
        else None
    )

    return order_repository.create_order_from_cart(
        db=db,
        cart_id=cart_id,
        note=note,
        user_id=current_user.user_id if current_user else None,
        user_role=user_role
    )


def get_orders(db: Session, current_user=None):
    if current_user and current_user.role == "CUSTOMER":
        return order_repository.get_orders_by_user_id(db, current_user.user_id)

    return order_repository.get_orders(db)


def get_order_by_id(db: Session, order_id: int, current_user=None):
    order = order_repository.get_order_by_id(db, order_id)

    if (
        order
        and current_user
        and current_user.role == "CUSTOMER"
        and order.user_id != current_user.user_id
    ):
        return None

    return order
