from sqlalchemy.orm import Session
from datetime import datetime
from app.models.cart_model import Cart
from app.models.cart_item_model import CartItem
from app.models.order_model import Order
from app.models.order_detail_model import OrderDetail
from app.models.product_model import Product


def create_order_from_cart(
    db: Session,
    cart_id: int,
    note: str | None = None,
    user_id: int | None = None
):
    cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()

    if not cart:
        raise Exception("Giỏ hàng không tồn tại")

    if cart.status != "OPEN":
        raise Exception("Giỏ hàng không còn mở")

    if user_id is not None and cart.user_id not in (None, user_id):
        raise Exception("Bạn không có quyền tạo đơn hàng từ giỏ hàng này")

    if user_id is not None and cart.user_id is None:
        cart.user_id = user_id

    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

    if len(cart_items) == 0:
        raise Exception("Giỏ hàng đang rỗng")

    total_amount = 0

    for item in cart_items:
        product = db.query(Product).filter(Product.product_id == item.product_id).first()

        if not product:
            raise Exception(f"Sản phẩm ID {item.product_id} không tồn tại")

        if product.stock_quantity < item.quantity:
            raise Exception(f"Sản phẩm {product.product_name} không đủ tồn kho")

        total_amount += item.total_price

    order = Order(
        order_code=f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
        user_id=user_id or cart.user_id,
        customer_id=cart.customer_id,
        total_amount=total_amount,
        status="PENDING",
        note=note
    )

    db.add(order)
    db.flush()

    for item in cart_items:
        product = db.query(Product).filter(Product.product_id == item.product_id).first()

        order_detail = OrderDetail(
            order_id=order.order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount=0,
            line_total=item.total_price
        )

        db.add(order_detail)

        product.stock_quantity -= item.quantity

    cart.status = "CHECKED_OUT"
    cart.updated_at = datetime.now()

    db.commit()
    db.refresh(order)

    return order


def get_orders(db: Session):
    return db.query(Order).all()


def get_orders_by_user_id(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.order_id == order_id).first()
