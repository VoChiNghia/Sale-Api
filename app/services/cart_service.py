from sqlalchemy.orm import Session

from app.repositories import cart_repository
from app.schemas.cart_schema import AddCartItem


def get_open_cart(db: Session, customer_id: int, current_user=None):
    cart = cart_repository.get_open_cart(db, customer_id)
    user_id = current_user.user_id if current_user else None

    if not cart:
        return cart_repository.create_cart(db, customer_id, user_id=user_id)

    if (
        cart
        and current_user
        and current_user.role == "CUSTOMER"
        and cart.user_id is None
    ):
        return cart_repository.assign_cart_user(db, cart, current_user.user_id)

    if (
        cart
        and current_user
        and current_user.role == "CUSTOMER"
        and cart.user_id != current_user.user_id
    ):
        raise PermissionError("You do not have permission to view this cart")

    return cart


def get_cart_items(db: Session, cart_id: int, current_user=None):
    cart = cart_repository.get_by_id(db, cart_id)

    if not cart:
        return []

    if (
        current_user
        and current_user.role == "CUSTOMER"
        and cart.user_id != current_user.user_id
    ):
        return []

    return cart_repository.get_cart_items(db, cart_id)


def add_item_to_cart(db: Session, data: AddCartItem, current_user):
    return cart_repository.add_item(
        db=db,
        customer_id=data.customer_id,
        product_id=data.product_id,
        quantity=data.quantity,
        user_id=current_user.user_id
    )
