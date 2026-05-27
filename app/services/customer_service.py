from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def get_customers(self):
        return self.customer_repository.get_all()

    def get_customer(self, customer_id: int):
        return self.customer_repository.get_by_id(customer_id)

    def create_customer(self, data: CustomerCreate):
        return self.customer_repository.create(data)

    def update_customer(self, customer_id: int, data: CustomerUpdate):
        return self.customer_repository.update(customer_id, data)

    def delete_customer(self, customer_id: int):
        return self.customer_repository.delete(customer_id)
