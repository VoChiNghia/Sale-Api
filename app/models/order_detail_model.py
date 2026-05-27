from sqlalchemy import Column, Integer, Numeric, ForeignKey

from app.db.base import Base


class OrderDetail(Base):
    __tablename__ = "order_details"

    order_detail_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(18, 2), nullable=False)
    discount = Column(Numeric(18, 2), default=0)
    line_total = Column(Numeric(18, 2), nullable=False)