from sqlalchemy.orm import Session

from app.models.customer_model import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Customer).all()

    def get_by_id(self, customer_id: int):
        return self.db.query(Customer).filter(
            Customer.customer_id == customer_id
        ).first()

    def create(self, data: CustomerCreate):
        customer = Customer(**data.model_dump())

        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)

        return customer

    def update(self, customer_id: int, data: CustomerUpdate):
        customer = self.get_by_id(customer_id)

        if not customer:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(customer, key, value)

        self.db.commit()
        self.db.refresh(customer)

        return customer

    def delete(self, customer_id: int):
        customer = self.get_by_id(customer_id)

        if not customer:
            return False

        self.db.delete(customer)
        self.db.commit()

        return True
