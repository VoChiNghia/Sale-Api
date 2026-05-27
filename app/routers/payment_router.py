from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_customer, require_staff_or_admin
from app.core.response import success_response, error_response
from app.db.database import get_db
from app.schemas.payment_schema import PaymentCreate
from app.services import payment_service


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.get("/")
def get_payments(db: Session = Depends(get_db), current_user = Depends(require_customer)):
    payments = payment_service.get_payments(db, current_user=current_user)
    return success_response(data=payments)


@router.get("/{payment_id}")
def get_payment(payment_id: int, db: Session = Depends(get_db), current_user = Depends(require_customer)):
    payment = payment_service.get_payment(
        db,
        payment_id,
        current_user=current_user
    )

    if not payment:
        return error_response(message="Không tìm thấy thanh toán", status_code=404)

    return success_response(data=payment)


@router.post("/")
def create_payment(data: PaymentCreate, db: Session = Depends(get_db), current_user = Depends(require_customer)):
    try:
        payment = payment_service.create_payment(
            db,
            data,
            current_user=current_user
        )
        return success_response(data=payment, status_code=201)
    except Exception as e:
        return error_response(message=str(e), status_code=400)


@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db), current_user = Depends(require_staff_or_admin)):
    payment = payment_service.delete_payment(db, payment_id)

    if not payment:
        return error_response(message="Không tìm thấy thanh toán", status_code=404)

    return success_response(message="Xóa thanh toán thành công")
