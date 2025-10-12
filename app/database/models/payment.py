# pylint: disable=too-few-public-methods
"""Payment database model."""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DateTime, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class Payment(Base):
    """Payment transaction model."""

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    customer_id: Mapped[str] = mapped_column(String(100), index=True)
    customer_email: Mapped[str] = mapped_column(String(255))
    customer_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Payment details
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), index=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    payment_method: Mapped[str] = mapped_column(String(50))

    # Status tracking
    status: Mapped[str] = mapped_column(String(20), default="completed", index=True)

    # Product/service information
    product_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    product_category: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, index=True
    )

    # Additional metadata
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    extra_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    payment_date: Mapped[datetime] = mapped_column(
        DateTime, index=True, default=lambda: datetime.now(UTC)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Composite indexes for query optimization
    __table_args__ = (
        Index("idx_payment_date_status", "payment_date", "status"),
        Index("idx_payment_date_category", "payment_date", "product_category"),
        Index("idx_customer_payment_date", "customer_id", "payment_date"),
    )
