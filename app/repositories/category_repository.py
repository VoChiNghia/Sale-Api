from sqlalchemy.orm import Session
from app.models.category_model import  Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate

def get_all(db: Session):
    return db.query(Category).filter(Category.status != "DELETED").all()

def get_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.category_id == category_id, Category.status != "DELETED").first()

def create(db: Session, category: CategoryCreate):
    category = Category(
        category_name=category.category_name,
        description=category.description
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update(db: Session, category_id: int, category_update: CategoryUpdate):
    category = get_by_id(db, category_id)
    if not category:
        return None

    for key, value in category_update.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category

def delete(db: Session, category_id: int):
    category = get_by_id(db, category_id)
    if not category:
        return False
    category.status = "DELETED"
    db.commit()
    db.refresh(category)
    return True
