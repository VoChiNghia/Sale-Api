from sqlalchemy.orm import Session

from app.models.cart_model import Cart
from app.models.cart_item_model import CartItem
from app.models.customer_model import Customer
from app.models.product_model import Product


def get_open_cart(db: Session, customer_id: int):
    return db.query(Cart).filter(
        Cart.customer_id == customer_id,
        Cart.status == "OPEN"
    ).first()


def get_by_id(db: Session, cart_id: int):
    return db.query(Cart).filter(Cart.cart_id == cart_id).first()


def create_cart(db: Session, customer_id: int, user_id: int | None = None):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()

    if not customer:
        raise ValueError("Customer not found")

    cart = Cart(customer_id=customer_id, user_id=user_id, status="OPEN")
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def assign_cart_user(db: Session, cart: Cart, user_id: int):
    cart.user_id = user_id
    db.commit()
    db.refresh(cart)
    return cart


def get_cart_items(db: Session, cart_id: int):
    return db.query(CartItem).filter(CartItem.cart_id == cart_id).all()


def add_item(
    db: Session,
    customer_id: int,
    product_id: int,
    quantity: int,
    user_id: int | None = None,
    user_role: str | None = None
):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    product = db.query(Product).filter(
        Product.product_id == product_id,
        Product.status == "ACTIVE"
    ).first()

    if not product:
        raise ValueError("Product not found or inactive")

    if quantity > product.stock_quantity:
        raise ValueError("Quantity exceeds stock")

    cart = get_open_cart(db, customer_id)

    is_customer_user = user_role and user_role.strip().upper() == "CUSTOMER"

    if not cart:
        cart_user_id = user_id if is_customer_user else None
        cart = create_cart(db, customer_id, user_id=cart_user_id)
    elif is_customer_user and cart.user_id is None:
        cart = assign_cart_user(db, cart, user_id)
    elif is_customer_user and cart.user_id != user_id:
        raise ValueError("You do not have permission to update this cart")

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id,
        CartItem.product_id == product_id
    ).first()

    unit_price = product.price

    if cart_item:
        new_quantity = cart_item.quantity + quantity

        if new_quantity > product.stock_quantity:
            raise ValueError("Quantity exceeds stock")

        cart_item.quantity = new_quantity
        cart_item.total_price = new_quantity * unit_price
    else:
        cart_item = CartItem(
            cart_id=cart.cart_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            total_price=quantity * unit_price
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart_item
