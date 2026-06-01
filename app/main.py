from fastapi import FastAPI
from app.db.database import engine

from app.db.base import Base
# Import models so SQLAlchemy registers all tables before create_all.
import app.models.user_model  # noqa: F401
import app.models.category_model  # noqa: F401
import app.models.product_model  # noqa: F401
import app.models.customer_model  # noqa: F401
import app.models.cart_model  # noqa: F401
import app.models.cart_item_model  # noqa: F401
import app.models.order_model  # noqa: F401
import app.models.order_detail_model  # noqa: F401
import app.models.payment_model  # noqa: F401
from app.routers import auth_router, cart_router, category_router, customer_router, order_router, payment_router, product_router, report_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Sales API",
    description="API for managing sales data",
    version="1.0.0"
)

app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(customer_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)
app.include_router(payment_router.router)
app.include_router(auth_router.router)
app.include_router(report_router.router)
