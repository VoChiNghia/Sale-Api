from datetime import date

from sqlalchemy.orm import Session

from app.repositories import report_repository


def _validate_date_range(start_date: date | None, end_date: date | None):
    if start_date and end_date and start_date > end_date:
        raise ValueError("start_date không được lớn hơn end_date")


def _normalize_limit(limit: int, max_limit: int = 100):
    if limit <= 0:
        raise ValueError("limit phải lớn hơn 0")

    return min(limit, max_limit)


def _normalize_threshold(threshold: int):
    if threshold < 0:
        raise ValueError("threshold không được nhỏ hơn 0")

    return threshold


def get_sales_overview(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    low_stock_threshold: int = 10
):
    _validate_date_range(start_date, end_date)
    low_stock_threshold = _normalize_threshold(low_stock_threshold)

    return report_repository.get_sales_overview(
        db,
        start_date=start_date,
        end_date=end_date,
        low_stock_threshold=low_stock_threshold
    )


def get_revenue_by_day(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None
):
    _validate_date_range(start_date, end_date)

    return report_repository.get_revenue_by_day(
        db,
        start_date=start_date,
        end_date=end_date
    )


def get_top_products(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 10
):
    _validate_date_range(start_date, end_date)
    limit = _normalize_limit(limit)

    return report_repository.get_top_products(
        db,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )


def get_top_customers(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 10
):
    _validate_date_range(start_date, end_date)
    limit = _normalize_limit(limit)

    return report_repository.get_top_customers(
        db,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )


def get_low_stock_products(
    db: Session,
    threshold: int = 10,
    limit: int = 20
):
    threshold = _normalize_threshold(threshold)
    limit = _normalize_limit(limit)

    return report_repository.get_low_stock_products(
        db,
        threshold=threshold,
        limit=limit
    )
