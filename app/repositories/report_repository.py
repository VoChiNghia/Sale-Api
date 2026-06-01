from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.category_model import Category
from app.models.customer_model import Customer
from app.models.order_detail_model import OrderDetail
from app.models.order_model import Order
from app.models.payment_model import Payment
from app.models.product_model import Product


def _date_range_filter(column, start_date: date | None, end_date: date | None):
    filters = []

    if start_date:
        filters.append(column >= datetime.combine(start_date, time.min))

    if end_date:
        filters.append(column <= datetime.combine(end_date, time.max))

    return filters


def _decimal(value) -> Decimal:
    if value is None:
        return Decimal("0")

    return Decimal(value)


def get_sales_overview(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    low_stock_threshold: int = 10
):
    order_filters = _date_range_filter(Order.order_date, start_date, end_date)
    payment_filters = [
        Payment.payment_status == "SUCCESS",
        Payment.paid_at.isnot(None),
        *_date_range_filter(Payment.paid_at, start_date, end_date),
    ]

    total_orders = db.query(func.count(Order.order_id)).filter(*order_filters).scalar() or 0
    paid_orders = db.query(func.count(Order.order_id)).filter(
        *order_filters,
        Order.status == "PAID"
    ).scalar() or 0
    pending_orders = db.query(func.count(Order.order_id)).filter(
        *order_filters,
        Order.status == "PENDING"
    ).scalar() or 0
    cancelled_orders = db.query(func.count(Order.order_id)).filter(
        *order_filters,
        Order.status == "CANCELLED"
    ).scalar() or 0

    total_revenue = _decimal(
        db.query(func.coalesce(func.sum(Payment.amount), 0))
        .filter(*payment_filters)
        .scalar()
    )

    average_order_value = Decimal("0")
    if paid_orders > 0:
        average_order_value = total_revenue / paid_orders

    return {
        "total_orders": total_orders,
        "paid_orders": paid_orders,
        "pending_orders": pending_orders,
        "cancelled_orders": cancelled_orders,
        "total_revenue": total_revenue,
        "average_order_value": average_order_value,
        "total_customers": db.query(func.count(Customer.customer_id)).scalar() or 0,
        "total_products": db.query(func.count(Product.product_id)).filter(
            Product.status != "DELETED"
        ).scalar() or 0,
        "low_stock_products": db.query(func.count(Product.product_id)).filter(
            Product.status == "ACTIVE",
            Product.stock_quantity <= low_stock_threshold
        ).scalar() or 0,
    }


def get_revenue_by_day(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None
):
    report_date = func.date(Payment.paid_at).label("report_date")
    rows = db.query(
        report_date,
        func.count(func.distinct(Payment.order_id)).label("order_count"),
        func.coalesce(func.sum(Payment.amount), 0).label("revenue"),
    ).filter(
        Payment.payment_status == "SUCCESS",
        Payment.paid_at.isnot(None),
        *_date_range_filter(Payment.paid_at, start_date, end_date),
    ).group_by(
        report_date
    ).order_by(
        report_date
    ).all()

    return [
        {
            "report_date": row.report_date,
            "order_count": row.order_count,
            "revenue": _decimal(row.revenue),
        }
        for row in rows
    ]


def get_top_products(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 10
):
    rows = db.query(
        Product.product_id,
        Product.product_name,
        func.coalesce(func.sum(OrderDetail.quantity), 0).label("quantity_sold"),
        func.coalesce(func.sum(OrderDetail.line_total), 0).label("revenue"),
    ).join(
        OrderDetail,
        OrderDetail.product_id == Product.product_id
    ).join(
        Order,
        Order.order_id == OrderDetail.order_id
    ).join(
        Payment,
        Payment.order_id == Order.order_id
    ).filter(
        Payment.payment_status == "SUCCESS",
        Payment.paid_at.isnot(None),
        *_date_range_filter(Payment.paid_at, start_date, end_date),
    ).group_by(
        Product.product_id,
        Product.product_name
    ).order_by(
        func.sum(OrderDetail.quantity).desc()
    ).limit(limit).all()

    return [
        {
            "product_id": row.product_id,
            "product_name": row.product_name,
            "quantity_sold": int(row.quantity_sold or 0),
            "revenue": _decimal(row.revenue),
        }
        for row in rows
    ]


def get_top_customers(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 10
):
    rows = db.query(
        Customer.customer_id,
        Customer.full_name,
        func.count(func.distinct(Order.order_id)).label("order_count"),
        func.coalesce(func.sum(Payment.amount), 0).label("total_spent"),
    ).join(
        Order,
        Order.customer_id == Customer.customer_id
    ).join(
        Payment,
        Payment.order_id == Order.order_id
    ).filter(
        Payment.payment_status == "SUCCESS",
        Payment.paid_at.isnot(None),
        *_date_range_filter(Payment.paid_at, start_date, end_date),
    ).group_by(
        Customer.customer_id,
        Customer.full_name
    ).order_by(
        func.sum(Payment.amount).desc()
    ).limit(limit).all()

    return [
        {
            "customer_id": row.customer_id,
            "full_name": row.full_name,
            "order_count": row.order_count,
            "total_spent": _decimal(row.total_spent),
        }
        for row in rows
    ]


def get_low_stock_products(
    db: Session,
    threshold: int = 10,
    limit: int = 20
):
    rows = db.query(
        Product.product_id,
        Product.product_name,
        Category.category_name,
        Product.stock_quantity,
        Product.price,
    ).join(
        Category,
        Category.category_id == Product.category_id
    ).filter(
        Product.status == "ACTIVE",
        Product.stock_quantity <= threshold
    ).order_by(
        Product.stock_quantity.asc(),
        Product.product_name.asc()
    ).limit(limit).all()

    return [
        {
            "product_id": row.product_id,
            "product_name": row.product_name,
            "category_name": row.category_name,
            "stock_quantity": row.stock_quantity,
            "price": _decimal(row.price),
        }
        for row in rows
    ]
