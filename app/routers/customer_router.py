from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_staff_or_admin
from app.core.response import success_response, error_response
from app.db.database import get_db
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate
from app.services.customer_service import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


def get_customer_service(db: Session = Depends(get_db)):
    repository = CustomerRepository(db)
    return CustomerService(repository)


@router.get("/")
def get_customers(
    service: CustomerService = Depends(get_customer_service),
    current_user=Depends(require_staff_or_admin)
):
    customers = service.get_customers()
    return success_response(data=customers)


@router.get("/{customer_id}")
def get_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service),
    current_user=Depends(require_staff_or_admin)
):
    customer = service.get_customer(customer_id)

    if not customer:
        return error_response(message="Customer not found", status_code=404)

    return success_response(data=customer)


@router.post("/")
def create_customer(
    data: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
    current_user=Depends(require_staff_or_admin)
):
    customer = service.create_customer(data)
    return success_response(data=customer, status_code=201)


@router.put("/{customer_id}")
def update_customer(
    customer_id: int,
    data: CustomerUpdate,
    service: CustomerService = Depends(get_customer_service),
    current_user=Depends(require_staff_or_admin)
):
    customer = service.update_customer(customer_id, data)

    if not customer:
        return error_response(message="Customer not found", status_code=404)

    return success_response(data=customer)


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service),
    current_user=Depends(require_staff_or_admin)
):
    success = service.delete_customer(customer_id)

    if not success:
        return error_response(message="Customer not found", status_code=404)

    return success_response(message="Customer deleted")
