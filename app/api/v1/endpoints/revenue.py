"""Revenue analytics endpoints."""

from datetime import UTC, datetime, timedelta
from typing import Optional

from dateutil import parser as date_parser
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.database.crud import PaymentCRUD
from app.schemas import RevenueResponse

router = APIRouter()


def ensure_timezone_naive(dt: datetime) -> datetime:
    """Convert datetime to timezone-naive UTC for database queries.

    PostgreSQL TIMESTAMP WITHOUT TIME ZONE columns require naive datetimes.
    If the datetime is timezone-aware, convert to UTC and strip timezone info.
    """
    if dt.tzinfo is not None:
        # Convert to UTC and strip timezone
        return dt.astimezone(UTC).replace(tzinfo=None)
    return dt


@router.get("/total", response_model=RevenueResponse, operation_id="total_revenue")
async def get_total_revenue(
    status: str = "completed",
    db: AsyncSession = Depends(get_db),
):
    """Get total revenue for all time."""
    total, count = await PaymentCRUD.calculate_revenue(db, status=status)

    return RevenueResponse(
        total_revenue=total,
        transaction_count=count,
        period="all_time",
        status_filter=status,
    )


@router.get("/this-month", response_model=RevenueResponse, operation_id="this_month")
async def get_revenue_this_month(
    status: str = "completed",
    db: AsyncSession = Depends(get_db),
):
    """Get revenue for the current month."""
    now = ensure_timezone_naive(datetime.now(UTC))
    start_of_month = datetime(now.year, now.month, 1)

    total, count = await PaymentCRUD.calculate_revenue(
        db, start_date=start_of_month, end_date=now, status=status
    )

    return RevenueResponse(
        total_revenue=total,
        transaction_count=count,
        period=f"this_month_{now.year}_{now.month}",
        start_date=start_of_month.isoformat(),
        end_date=now.isoformat(),
        status_filter=status,
    )


@router.get(
    "/year-to-date", response_model=RevenueResponse, operation_id="year_to_date"
)
async def get_revenue_year_to_date(
    status: str = "completed",
    db: AsyncSession = Depends(get_db),
):
    """Get revenue from January 1st to now."""
    now = ensure_timezone_naive(datetime.now(UTC))
    start_of_year = datetime(now.year, 1, 1)

    total, count = await PaymentCRUD.calculate_revenue(
        db, start_date=start_of_year, end_date=now, status=status
    )

    return RevenueResponse(
        total_revenue=total,
        transaction_count=count,
        period=f"year_to_date_{now.year}",
        start_date=start_of_year.isoformat(),
        end_date=now.isoformat(),
        status_filter=status,
    )


@router.get(
    "/custom-range", response_model=RevenueResponse, operation_id="custom_range"
)
async def get_revenue_custom_range(
    start_date: str,
    end_date: str,
    status: str = "completed",
    db: AsyncSession = Depends(get_db),
):
    """Get revenue for a custom date/time range."""
    try:
        start_dt = ensure_timezone_naive(date_parser.parse(start_date))
        end_dt = ensure_timezone_naive(date_parser.parse(end_date))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format. Use ISO format: {str(e)}",
        ) from e

    if start_dt > end_dt:
        raise HTTPException(
            status_code=400, detail="start_date must be before end_date"
        )

    total, count = await PaymentCRUD.calculate_revenue(
        db, start_date=start_dt, end_date=end_dt, status=status
    )

    return RevenueResponse(
        total_revenue=total,
        transaction_count=count,
        period="custom_range",
        start_date=start_dt.isoformat(),
        end_date=end_dt.isoformat(),
        status_filter=status,
    )


@router.get("/last-n-days", response_model=RevenueResponse, operation_id="last_n_days")
async def get_revenue_last_n_days(
    days: int = 30,
    status: str = "completed",
    db: AsyncSession = Depends(get_db),
):
    """Get revenue for the last N days."""
    if days < 1:
        raise HTTPException(status_code=400, detail="days must be at least 1")

    now = ensure_timezone_naive(datetime.now(UTC))
    start_date = now - timedelta(days=days)

    total, count = await PaymentCRUD.calculate_revenue(
        db, start_date=start_date, end_date=now, status=status
    )

    return RevenueResponse(
        total_revenue=total,
        transaction_count=count,
        period=f"last_{days}_days",
        start_date=start_date.isoformat(),
        end_date=now.isoformat(),
        status_filter=status,
    )


@router.get("/by-category", response_model=dict, operation_id="by_category")
async def get_revenue_by_category(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: str = "completed",
    db: AsyncSession = Depends(get_db),
):
    """Get revenue breakdown by product category."""
    start_dt = None
    end_dt = None

    if start_date:
        try:
            start_dt = ensure_timezone_naive(date_parser.parse(start_date))
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid start_date format: {str(e)}"
            ) from e

    if end_date:
        try:
            end_dt = ensure_timezone_naive(date_parser.parse(end_date))
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid end_date format: {str(e)}"
            ) from e

    categories = await PaymentCRUD.revenue_by_category(
        db, start_date=start_dt, end_date=end_dt, status=status
    )

    total_revenue = sum(cat["revenue"] for cat in categories.values())
    total_count = sum(cat["transaction_count"] for cat in categories.values())

    return {
        "categories": categories,
        "total_revenue": total_revenue,
        "total_transactions": total_count,
        "status_filter": status,
        "start_date": start_date,
        "end_date": end_date,
    }


@router.get("/by-month", response_model=dict, operation_id="by_month")
async def get_revenue_by_month(
    year: int,
    status: str = "completed",
    db: AsyncSession = Depends(get_db),
):
    """Get monthly revenue breakdown for a specific year."""
    months = await PaymentCRUD.revenue_by_month(db, year=year, status=status)

    total_revenue = sum(m["revenue"] for m in months.values())
    total_count = sum(m["transaction_count"] for m in months.values())

    return {
        "year": year,
        "months": months,
        "total_revenue": total_revenue,
        "total_transactions": total_count,
        "status_filter": status,
    }
