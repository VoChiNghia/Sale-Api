from sqlalchemy.orm import Session

from app.models.user_model import User
from app.repositories import user_repository
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token


def register(db: Session, data: RegisterRequest):
    existing_user = user_repository.get_by_username(db, data.username)

    if existing_user:
        raise Exception("Username đã tồn tại")

    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        role="CUSTOMER",
        status="ACTIVE"
    )

    return user_repository.create(db, user)


def login(db: Session, data: LoginRequest):
    user = user_repository.get_by_username(db, data.username)

    if not user:
        raise Exception("Tài khoản không tồn tại")

    if user.status != "ACTIVE":
        raise Exception("Tài khoản đã bị khóa")

    if not verify_password(data.password, user.password_hash):
        raise Exception("Mật khẩu không đúng")

    token = create_access_token({
        "sub": str(user.user_id),
        "username": user.username,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
