from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success_response, error_response
from app.db.database import get_db
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = auth_service.register(db, data)

        return success_response(
            data={
                "user_id": user.user_id,
                "username": user.username,
                "role": user.role
            },
            message="Đăng ký thành công",
            status_code=201
        )

    except Exception as e:
        return error_response(message=str(e), status_code=400)


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        token = auth_service.login(db, data)
        return success_response(data=token)

    except Exception as e:
        return error_response(message=str(e), status_code=400)
