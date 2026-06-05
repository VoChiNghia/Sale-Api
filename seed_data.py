from decimal import Decimal
from datetime import datetime, timedelta
import os

from app.core.security import hash_password
from app.db.base import Base
from app.db.database import SessionLocal, engine
from app.models.cart_item_model import CartItem
from app.models.cart_model import Cart
from app.models.category_model import Category
from app.models.customer_model import Customer
from app.models.order_detail_model import OrderDetail
from app.models.order_model import Order
from app.models.payment_model import Payment
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

REPORT_ORDER_SPECS = [
    {
        "days_ago": 1,
        "customer_index": 0,
        "status": "PAID",
        "payment_method": "CASH",
        "items": [(0, 2), (7, 1), (15, 1)],
    },
    {
        "days_ago": 2,
        "customer_index": 1,
        "status": "PAID",
        "payment_method": "BANK_TRANSFER",
        "items": [(1, 1), (8, 2)],
    },
    {
        "days_ago": 3,
        "customer_index": 2,
        "status": "PAID",
        "payment_method": "MOMO",
        "items": [(2, 3), (9, 1)],
    },
    {
        "days_ago": 4,
        "customer_index": 3,
        "status": "PAID",
        "payment_method": "CASH",
        "items": [(3, 1), (10, 2), (17, 1)],
    },
    {
        "days_ago": 5,
        "customer_index": 4,
        "status": "PENDING",
        "payment_method": "BANK_TRANSFER",
        "items": [(4, 2), (11, 1)],
    },
    {
        "days_ago": 7,
        "customer_index": 0,
        "status": "PAID",
        "payment_method": "CASH",
        "items": [(0, 1), (14, 2), (21, 1)],
    },
    {
        "days_ago": 9,
        "customer_index": 5,
        "status": "PAID",
        "payment_method": "BANK_TRANSFER",
        "items": [(5, 2), (12, 2)],
    },
    {
        "days_ago": 11,
        "customer_index": 6,
        "status": "CANCELLED",
        "payment_method": "CASH",
        "items": [(6, 1), (13, 1)],
    },
    {
        "days_ago": 14,
        "customer_index": 1,
        "status": "PAID",
        "payment_method": "MOMO",
        "items": [(8, 1), (16, 2), (24, 1)],
    },
    {
        "days_ago": 18,
        "customer_index": 7,
        "status": "PAID",
        "payment_method": "CASH",
        "items": [(18, 2), (25, 1)],
    },
    {
        "days_ago": 23,
        "customer_index": 8,
        "status": "PAID",
        "payment_method": "BANK_TRANSFER",
        "items": [(20, 3), (28, 1)],
    },
    {
        "days_ago": 29,
        "customer_index": 9,
        "status": "PAID",
        "payment_method": "CASH",
        "items": [(30, 2), (35, 1), (40, 1)],
    },
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
            description=f"Danh mục {name}",
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
                description=f"Sản phẩm {category.category_name} màu {suffix}",
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
            full_name=f"Khách hàng {index}",
            email=email,
            phone=f"091{index:07d}",
            address=f"Địa chỉ khách hàng {index}",
        )
        db.add(customer)
        created += 1

    db.commit()
    return created


def seed_carts(db):
    exists = db.query(Cart).first()

    if exists:
        return 0, 0

    customer = db.query(Customer).order_by(Customer.customer_id).first()
    customer_user = db.query(User).filter(User.username == "customer").first()
    products = db.query(Product).filter(
        Product.status == "ACTIVE",
        Product.stock_quantity > 0
    ).order_by(Product.product_id).limit(3).all()

    if not customer or not products:
        return 0, 0

    cart = Cart(
        user_id=customer_user.user_id if customer_user else None,
        customer_id=customer.customer_id,
        status="OPEN",
    )
    db.add(cart)
    db.flush()

    item_count = 0
    quantities = [1, 2, 1]

    for product, quantity in zip(products, quantities):
        quantity = min(quantity, product.stock_quantity)

        if quantity <= 0:
            continue

        unit_price = Decimal(product.price)
        cart_item = CartItem(
            cart_id=cart.cart_id,
            product_id=product.product_id,
            quantity=quantity,
            unit_price=unit_price,
            total_price=unit_price * quantity,
        )
        db.add(cart_item)
        item_count += 1

    if item_count == 0:
        db.rollback()
        return 0, 0

    db.commit()
    return 1, item_count


def seed_report_data(db):
    exists = db.query(Order).filter(
        Order.order_code.like("RPTDEMO%")
    ).first()

    if exists:
        return 0

    products = db.query(Product).filter(
        Product.status == "ACTIVE"
    ).order_by(Product.product_id).all()
    customers = db.query(Customer).order_by(Customer.customer_id).all()
    customer_user = db.query(User).filter(User.username == "customer").first()

    if not products or not customers:
        return 0

    base_date = datetime.now().replace(
        hour=10,
        minute=0,
        second=0,
        microsecond=0
    )
    created = 0

    for index, spec in enumerate(REPORT_ORDER_SPECS, start=1):
        customer = customers[spec["customer_index"] % len(customers)]
        order_date = base_date - timedelta(days=spec["days_ago"])
        total_amount = Decimal("0")
        order_items = []

        for product_index, quantity in spec["items"]:
            product = products[product_index % len(products)]
            unit_price = Decimal(product.price)
            line_total = unit_price * quantity
            total_amount += line_total
            order_items.append((product, quantity, unit_price, line_total))

        order = Order(
            order_code=f"RPTDEMO{index:04d}",
            user_id=customer_user.user_id if customer_user else None,
            customer_id=customer.customer_id,
            order_date=order_date,
            total_amount=total_amount,
            status=spec["status"],
            note="Seed data for report",
        )
        db.add(order)
        db.flush()

        for product, quantity, unit_price, line_total in order_items:
            detail = OrderDetail(
                order_id=order.order_id,
                product_id=product.product_id,
                quantity=quantity,
                unit_price=unit_price,
                discount=Decimal("0"),
                line_total=line_total,
            )
            db.add(detail)

            if spec["status"] == "PAID":
                product.stock_quantity = max(
                    0,
                    product.stock_quantity - quantity
                )

        if spec["status"] == "PAID":
            payment_status = "SUCCESS"
            paid_at = order_date + timedelta(hours=1)
        elif spec["status"] == "CANCELLED":
            payment_status = "FAILED"
            paid_at = None
        else:
            payment_status = "PENDING"
            paid_at = None

        payment = Payment(
            order_id=order.order_id,
            payment_method=spec["payment_method"],
            amount=total_amount,
            payment_status=payment_status,
            paid_at=paid_at,
            transaction_code=f"RPT-TXN-{index:04d}",
        )
        db.add(payment)
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
        report_order_count = seed_report_data(db)
        cart_count, cart_item_count = seed_carts(db)
        bootstrap_admin = promote_bootstrap_admin(db)

        print("Seed data success")
        print(f"Users created: {user_count}")
        print(f"Categories created: {category_count}")
        print(f"Products created: {product_count}")
        print(f"Customers created: {customer_count}")
        print(f"Report orders created: {report_order_count}")
        print(f"Carts created: {cart_count}")
        print(f"Cart items created: {cart_item_count}")

        if bootstrap_admin:
            print(f"Bootstrap admin promoted: {bootstrap_admin}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
