from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func

from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    payment_method = Column(
        String(30),
        nullable=False
    )

    amount = Column(
        Numeric(18, 2),
        nullable=False
    )

    payment_status = Column(
        String(20),
        default="PENDING"
    )

    paid_at = Column(
        DateTime,
        nullable=True
    )

    transaction_code = Column(
        String(100),
        nullable=True
    )