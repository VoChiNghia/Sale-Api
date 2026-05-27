from sqlalchemy.orm import Session
from datetime import datetime

from app.models.payment_model import Payment
from app.models.order_model import Order
from app.schemas.payment_schema import PaymentCreate


def get_all(db: Session):
    return db.query(Payment).all()


def get_all_by_user_id(db: Session, user_id: int):
    return db.query(Payment).join(Order).filter(Order.user_id == user_id).all()


def get_by_id(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.payment_id == payment_id).first()


def create(db: Session, data: PaymentCreate):
    order = db.query(Order).filter(Order.order_id == data.order_id).first()

    if not order:
        raise Exception("Đơn hàng không tồn tại")

    if order.status == "CANCELLED":
        raise Exception("Đơn hàng đã hủy, không thể thanh toán")

    if order.status == "PAID":
        raise Exception("Đơn hàng đã thanh toán")

    if data.amount <= 0:
        raise Exception("Số tiền thanh toán phải lớn hơn 0")

    payment = Payment(
        order_id=data.order_id,
        payment_method=data.payment_method,
        amount=data.amount,
        payment_status=data.payment_status,
        paid_at=datetime.now() if data.payment_status == "SUCCESS" else None,
        transaction_code=data.transaction_code
    )

    db.add(payment)

    if data.payment_status == "SUCCESS":
        order.status = "PAID"

    db.commit()
    db.refresh(payment)

    return payment


def delete(db: Session, payment_id: int):
    payment = get_by_id(db, payment_id)

    if not payment:
        return None

    db.delete(payment)
    db.commit()

    return payment
