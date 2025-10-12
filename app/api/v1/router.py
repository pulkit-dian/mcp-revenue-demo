"""API v1 routing."""

from fastapi import APIRouter

from app.api.v1.endpoints import revenue

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(revenue.router, prefix="/revenue", tags=["revenue"])
