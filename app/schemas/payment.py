"""Pydantic schemas for payment API - Read-only responses."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PaymentResponse(BaseModel):
    """Schema for payment response."""

    id: int
    transaction_id: str
    customer_id: str
    customer_email: str
    customer_name: Optional[str]

    amount: float
    currency: str
    payment_method: str

    status: str

    product_name: Optional[str]
    product_category: Optional[str]

    description: Optional[str]
    extra_data: Optional[str]

    payment_date: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentListResponse(BaseModel):
    """Schema for paginated payment list."""

    payments: List[PaymentResponse]
    total: int
    limit: int
    offset: int


class RevenueResponse(BaseModel):
    """Schema for revenue query responses."""

    total_revenue: float = Field(..., description="Total revenue amount")
    transaction_count: int = Field(..., description="Number of transactions")
    period: str = Field(..., description="Time period description")
    start_date: Optional[str] = Field(None, description="Start date of the period")
    end_date: Optional[str] = Field(None, description="End date of the period")
    status_filter: str = Field(..., description="Payment status filter applied")
    currency: str = Field(default="USD", description="Currency of the revenue")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_revenue": 125478.50,
                "transaction_count": 342,
                "period": "this_month_2024_10",
                "start_date": "2024-10-01T00:00:00Z",
                "end_date": "2024-10-12T15:30:00Z",
                "status_filter": "completed",
                "currency": "USD",
            }
        }
    )
