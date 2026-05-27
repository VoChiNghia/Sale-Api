from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.repositories import user_repository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc hết hạn"
        )

    user = user_repository.get_by_id(db, int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Không tìm thấy user"
        )

    return user

def require_admin(
    current_user = Depends(get_current_user)
):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền ADMIN"
        )

    return current_user


def require_staff_or_admin(
    current_user=Depends(get_current_user)
):
    allowed_roles = ["ADMIN", "STAFF"]

    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập"
        )

    return current_user

def require_customer(
    current_user=Depends(get_current_user)
):
    allowed_roles = [
        "CUSTOMER",
        "STAFF",
        "ADMIN"
    ]

    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền truy cập"
        )

    return current_user
