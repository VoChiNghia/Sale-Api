from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Text
from sqlalchemy.sql import func

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    order_code = Column(String(30), unique=True, nullable=False)
    user_id = Column(Integer, nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    order_date = Column(DateTime, server_default=func.now())
    total_amount = Column(Numeric(18, 2), nullable=False)
    status = Column(String(20), default="PENDING")
    note = Column(Text, nullable=True)