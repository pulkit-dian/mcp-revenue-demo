"""Payment CRUD operations."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Payment


class PaymentCRUD:
    """CRUD operations for Payment model."""

    @staticmethod
    async def get_by_id(db: AsyncSession, payment_id: int) -> Optional[Payment]:
        """Get payment by ID."""
        result = await db.execute(select(Payment).where(Payment.id == payment_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def list_payments(
        db: AsyncSession,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None,
        customer_id: Optional[str] = None,
    ) -> List[Payment]:
        """List payments with filters."""
        query = select(Payment)

        if status:
            query = query.where(Payment.status == status)
        if customer_id:
            query = query.where(Payment.customer_id == customer_id)

        query = query.order_by(Payment.payment_date.desc()).limit(limit).offset(offset)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def calculate_revenue(
        db: AsyncSession,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: str = "completed",
    ) -> tuple[float, int]:
        """Calculate total revenue and transaction count."""
        query = select(
            func.sum(Payment.amount).label("total"),
            func.count(Payment.id).label("count"),  # pylint: disable=not-callable
        ).where(Payment.status == status)

        if start_date:
            query = query.where(Payment.payment_date >= start_date)
        if end_date:
            query = query.where(Payment.payment_date <= end_date)

        result = await db.execute(query)
        row = result.one()

        return (float(row.total) if row.total else 0.0, row.count)

    @staticmethod
    async def revenue_by_category(
        db: AsyncSession,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: str = "completed",
    ) -> dict:
        """Get revenue breakdown by category."""
        query = select(
            Payment.product_category,
            func.sum(Payment.amount).label("total"),
            func.count(Payment.id).label("count"),  # pylint: disable=not-callable
        ).where(Payment.status == status)

        if start_date:
            query = query.where(Payment.payment_date >= start_date)
        if end_date:
            query = query.where(Payment.payment_date <= end_date)

        query = query.group_by(Payment.product_category)

        result = await db.execute(query)
        rows = result.all()

        categories = {}
        for row in rows:
            category = row.product_category or "uncategorized"
            categories[category] = {
                "revenue": float(row.total) if row.total else 0.0,
                "transaction_count": row.count,
            }

        return categories

    @staticmethod
    async def revenue_by_month(
        db: AsyncSession, year: int, status: str = "completed"
    ) -> dict:
        """Get monthly revenue for a specific year."""
        result = await db.execute(
            select(
                extract("month", Payment.payment_date).label("month"),
                func.sum(Payment.amount).label("total"),
                func.count(Payment.id).label("count"),  # pylint: disable=not-callable
            )
            .where(
                and_(
                    Payment.status == status,
                    extract("year", Payment.payment_date) == year,
                )
            )
            .group_by(extract("month", Payment.payment_date))
            .order_by(extract("month", Payment.payment_date))
        )

        rows = result.all()

        months = {}
        for row in rows:
            month_num = int(row.month)
            months[month_num] = {
                "month": month_num,
                "revenue": float(row.total) if row.total else 0.0,
                "transaction_count": row.count,
            }

        return months
