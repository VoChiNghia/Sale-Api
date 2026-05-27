from sqlalchemy.orm import Session

from app.repositories import category_repository
from app.schemas.category_schema import CategoryCreate, CategoryUpdate

def get_categories(db: Session):
    return category_repository.get_all(db)


def get_category(db: Session, category_id: int):
    return category_repository.get_by_id(db, category_id)


def create_category(db: Session, data: CategoryCreate):
    return category_repository.create(db, data)


def update_category(db: Session, category_id: int, data: CategoryUpdate):
    return category_repository.update(db, category_id, data)


def delete_category(db: Session, category_id: int):
    return category_repository.delete(db, category_id)