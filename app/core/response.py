from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(
    data=None,
    message: str = "Thành công",
    status_code: int = 200
):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": jsonable_encoder(data),
            "errors": None
        }
    )


def error_response(
    message: str = "Có lỗi xảy ra",
    errors=None,
    status_code: int = 400
):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None,
            "errors": jsonable_encoder(errors)
        }
    )