from sqlalchemy.orm import Session

from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate


def get_all(db: Session):
    return db.query(Product).filter(Product.status != "DELETED").all()


def get_by_id(db: Session, product_id: int):
    return db.query(Product).filter(
        Product.product_id == product_id,
        Product.status != "DELETED"
    ).first()


def create(db: Session, data: ProductCreate):
    product = Product(**data.model_dump())

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def update(db: Session, product_id: int, data: ProductUpdate):
    product = get_by_id(db, product_id)

    if not product:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


def soft_delete(db: Session, product_id: int):
    product = get_by_id(db, product_id)

    if not product:
        return False

    product.status = "DELETED"
    db.commit()

    return True
