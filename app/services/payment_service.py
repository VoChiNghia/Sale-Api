from sqlalchemy.orm import Session

from app.repositories import order_repository
from app.repositories import payment_repository
from app.schemas.payment_schema import PaymentCreate


def get_payments(db: Session, current_user=None):
    if current_user and current_user.role == "CUSTOMER":
        return payment_repository.get_all_by_user_id(db, current_user.user_id)

    return payment_repository.get_all(db)


def get_payment(db: Session, payment_id: int, current_user=None):
    payment = payment_repository.get_by_id(db, payment_id)

    if not payment:
        return None

    order = order_repository.get_order_by_id(db, payment.order_id)

    if (
        current_user
        and current_user.role == "CUSTOMER"
        and (not order or order.user_id != current_user.user_id)
    ):
        return None

    return payment


def create_payment(db: Session, data: PaymentCreate, current_user=None):
    order = order_repository.get_order_by_id(db, data.order_id)

    if (
        current_user
        and current_user.role == "CUSTOMER"
        and (not order or order.user_id != current_user.user_id)
    ):
        raise Exception("Bạn không có quyền thanh toán đơn hàng này")

    return payment_repository.create(db, data)


def delete_payment(db: Session, payment_id: int):
    return payment_repository.delete(db, payment_id)
