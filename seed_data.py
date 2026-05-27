from decimal import Decimal
from datetime import datetime
import random

from app.db.database import SessionLocal, engine
from app.db.base import Base
from app.core.security import hash_password

from app.models.user_model import User
from app.models.category_model import Category
from app.models.product_model import Product
from app.models.customer_model import Customer

# Ensure tables exist before inserting seed data.
import app.models.user_model  # noqa: F401
import app.models.category_model  # noqa: F401
import app.models.product_model  # noqa: F401
import app.models.customer_model  # noqa: F401


db = SessionLocal()

def seed():
    print("Seeding data...")

    Base.metadata.create_all(bind=engine)

    # USERS
    users = [
        User(username="admin", password_hash=hash_password("admin123"), full_name="Admin SmartSales", email="admin@gmail.com", phone="0900000001", role="ADMIN"),
        User(username="staff", password_hash=hash_password("staff123"), full_name="Nhân viên bán hàng", email="staff@gmail.com", phone="0900000002", role="STAFF"),
        User(username="customer", password_hash=hash_password("customer123"), full_name="Khách hàng demo", email="customer@gmail.com", phone="0900000003", role="CUSTOMER"),
    ]

    db.add_all(users)
    db.commit()

    # CATEGORIES
    category_names = [
        "Đèn LED",
        "Đèn trợ sáng",
        "Đèn bi cầu",
        "Đèn xi nhan",
        "Đèn hậu",
        "Đèn demi",
        "Còi xe",
        "Gương xe",
        "Ốp bảo vệ",
        "Pô độ",
        "Tem xe",
        "Phụ kiện điện",
        "Sạc USB xe máy",
        "Camera hành trình",
        "Đồ chơi xe khác",
    ]

    categories = []

    for name in category_names:
        cate = Category(
            category_name=name,
            description=f"Danh mục {name}",
            status="ACTIVE"
        )
        categories.append(cate)

    db.add_all(categories)
    db.commit()

    # PRODUCTS ~ 100 sản phẩm
    product_suffixes = [
        "X1", "X2", "Mini", "Pro", "Titan", "Racing", "Sport",
        "Premium", "Classic", "Ultra", "Plus", "V2", "V3"
    ]

    products = []

    for category in categories:
        for i in range(1, 8):  # 15 category * 7 = 105 products
            suffix = random.choice(product_suffixes)

            price = random.choice([
                120000, 150000, 180000, 220000, 250000,
                300000, 350000, 450000, 550000, 750000,
                950000, 1200000
            ])

            product = Product(
                category_id=category.category_id,
                product_name=f"{category.category_name} {suffix} {i}",
                description=f"Sản phẩm {category.category_name} mẫu {suffix} số {i}",
                price=Decimal(price),
                stock_quantity=random.randint(5, 200),
                image_url=f"https://example.com/products/{category.category_id}_{i}.jpg",
                status="ACTIVE"
            )

            products.append(product)

    db.add_all(products)
    db.commit()

    # CUSTOMERS
    customers = []

    for i in range(1, 21):
        customer = Customer(
            full_name=f"Khách hàng {i}",
            email=f"customer{i}@gmail.com",
            phone=f"091{i:07d}",
            address=f"Địa chỉ khách hàng {i}"
        )
        customers.append(customer)

    db.add_all(customers)
    db.commit()

    print("Seed data success")
    print(f"Users: {len(users)}")
    print(f"Categories: {len(categories)}")
    print(f"Products: {len(products)}")
    print(f"Customers: {len(customers)}")


if __name__ == "__main__":
    seed()
    db.close()