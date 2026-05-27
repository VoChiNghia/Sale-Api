from sqlalchemy.orm import Session

from app.repositories import product_repository
from app.schemas.product_schema import ProductCreate, ProductUpdate


def get_products(db: Session):
    return product_repository.get_all(db)


def get_product(db: Session, product_id: int):
    return product_repository.get_by_id(db, product_id)


def create_product(db: Session, data: ProductCreate):
    return product_repository.create(db, data)


def update_product(db: Session, product_id: int, data: ProductUpdate):
    return product_repository.update(db, product_id, data)


def delete_product(db: Session, product_id: int):
    return product_repository.soft_delete(db, product_id)