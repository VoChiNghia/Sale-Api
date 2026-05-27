from decimal import Decimal
import os

from app.core.security import hash_password
from app.db.base import Base
from app.db.database import SessionLocal, engine
from app.models.category_model import Category
from app.models.customer_model import Customer
from app.models.product_model import Product
from app.models.user_model import User

# Register all models before create_all.
import app.models.cart_item_model  # noqa: F401
import app.models.cart_model  # noqa: F401
import app.models.category_model  # noqa: F401
import app.models.customer_model  # noqa: F401
import app.models.order_detail_model  # noqa: F401
import app.models.order_model  # noqa: F401
import app.models.payment_model  # noqa: F401
import app.models.product_model  # noqa: F401
import app.models.user_model  # noqa: F401


USERS = [
    {
        "username": "admin",
        "password": "admin123",
        "full_name": "Admin SmartSales",
        "email": "admin@gmail.com",
        "phone": "0900000001",
        "role": "ADMIN",
    },
    {
        "username": "staff",
        "password": "staff123",
        "full_name": "Staff SmartSales",
        "email": "staff@gmail.com",
        "phone": "0900000002",
        "role": "STAFF",
    },
    {
        "username": "customer",
        "password": "customer123",
        "full_name": "Customer Demo",
        "email": "customer@gmail.com",
        "phone": "0900000003",
        "role": "CUSTOMER",
    },
]

CATEGORY_NAMES = [
    "Den LED",
    "Den tro sang",
    "Den bi cau",
    "Den xi nhan",
    "Den hau",
    "Den demi",
    "Coi xe", 
    "Guong xe",
    "Op bao ve",
    "Po do",
    "Tem xe",
    "Phu kien dien",
    "Sac USB xe may",
    "Camera hanh trinh",
    "Do choi xe khac",
]

PRODUCT_SUFFIXES = [
    "X1",
    "X2",
    "Mini",
    "Pro",
    "Titan",
    "Racing",
    "Sport",
]

PRODUCT_PRICES = [
    120000,
    150000,
    180000,
    220000,
    250000,
    300000,
    350000,
]


def seed_users(db):
    created = 0

    for item in USERS:
        exists = db.query(User).filter(User.username == item["username"]).first()

        if exists:
            continue

        user = User(
            username=item["username"],
            password_hash=hash_password(item["password"]),
            full_name=item["full_name"],
            email=item["email"],
            phone=item["phone"],
            role=item["role"],
            status="ACTIVE",
        )
        db.add(user)
        created += 1

    db.commit()
    return created


def promote_bootstrap_admin(db):
    username = os.getenv("BOOTSTRAP_ADMIN_USERNAME")

    if not username:
        return None

    user = db.query(User).filter(User.username == username).first()

    if not user:
        print(f"Bootstrap admin user not found: {username}")
        return None

    user.role = "ADMIN"
    user.status = "ACTIVE"
    db.commit()

    return username


def seed_categories(db):
    created = 0

    for name in CATEGORY_NAMES:
        exists = db.query(Category).filter(Category.category_name == name).first()

        if exists:
            continue

        category = Category(
            category_name=name,
            description=f"Danh muc {name}",
            status="ACTIVE",
        )
        db.add(category)
        created += 1

    db.commit()
    return created


def seed_products(db):
    created = 0
    categories = db.query(Category).all()

    for category in categories:
        for index, suffix in enumerate(PRODUCT_SUFFIXES, start=1):
            product_name = f"{category.category_name} {suffix}"

            exists = db.query(Product).filter(
                Product.product_name == product_name
            ).first()

            if exists:
                continue

            product = Product(
                category_id=category.category_id,
                product_name=product_name,
                description=f"San pham {category.category_name} mau {suffix}",
                price=Decimal(PRODUCT_PRICES[index - 1]),
                stock_quantity=20 + index * 5,
                image_url=(
                    f"https://example.com/products/"
                    f"{category.category_id}_{index}.jpg"
                ),
                status="ACTIVE",
            )
            db.add(product)
            created += 1

    db.commit()
    return created


def seed_customers(db):
    created = 0

    for index in range(1, 21):
        email = f"customer{index}@gmail.com"
        exists = db.query(Customer).filter(Customer.email == email).first()

        if exists:
            continue

        customer = Customer(
            full_name=f"Khach hang {index}",
            email=email,
            phone=f"091{index:07d}",
            address=f"Dia chi khach hang {index}",
        )
        db.add(customer)
        created += 1

    db.commit()
    return created


def seed():
    print("Seeding data...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        user_count = seed_users(db)
        category_count = seed_categories(db)
        product_count = seed_products(db)
        customer_count = seed_customers(db)
        bootstrap_admin = promote_bootstrap_admin(db)

        print("Seed data success")
        print(f"Users created: {user_count}")
        print(f"Categories created: {category_count}")
        print(f"Products created: {product_count}")
        print(f"Customers created: {customer_count}")

        if bootstrap_admin:
            print(f"Bootstrap admin promoted: {bootstrap_admin}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
