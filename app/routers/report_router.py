from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.auth import require_staff_or_admin
from app.core.response import error_response, success_response
from app.db.database import get_db
from app.services import report_service


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/overview")
def get_sales_overview(
    start_date: date | None = None,
    end_date: date | None = None,
    low_stock_threshold: int = Query(default=10, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(require_staff_or_admin)
):
    try:
        overview = report_service.get_sales_overview(
            db,
            start_date=start_date,
            end_date=end_date,
            low_stock_threshold=low_stock_threshold
        )
        return success_response(data=overview)
    except ValueError as e:
        return error_response(message=str(e), status_code=400)


@router.get("/revenue-by-day")
def get_revenue_by_day(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_staff_or_admin)
):
    try:
        report = report_service.get_revenue_by_day(
            db,
            start_date=start_date,
            end_date=end_date
        )
        return success_response(data=report)
    except ValueError as e:
        return error_response(message=str(e), status_code=400)


@router.get("/top-products")
def get_top_products(
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = Query(default=10, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(require_staff_or_admin)
):
    try:
        products = report_service.get_top_products(
            db,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        return success_response(data=products)
    except ValueError as e:
        return error_response(message=str(e), status_code=400)


@router.get("/top-customers")
def get_top_customers(
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = Query(default=10, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(require_staff_or_admin)
):
    try:
        customers = report_service.get_top_customers(
            db,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        return success_response(data=customers)
    except ValueError as e:
        return error_response(message=str(e), status_code=400)


@router.get("/low-stock-products")
def get_low_stock_products(
    threshold: int = Query(default=10, ge=0),
    limit: int = Query(default=20, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(require_staff_or_admin)
):
    products = report_service.get_low_stock_products(
        db,
        threshold=threshold,
        limit=limit
    )
    return success_response(data=products)
