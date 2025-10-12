"""Main FastAPI application with MCP integration for payment revenue tracking."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from app.api.v1.router import api_router
from app.core.config import settings
from app.database import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    await init_db()
    yield


# Create FastAPI app
app = FastAPI(
    title="Payment Revenue MCP Server",
    description="MCP server for tracking and querying payment revenue with advanced time-based filtering",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)


# Health check endpoint
@app.get("/", tags=["health"])
async def health():
    """Health check endpoint."""
    return "Hello World!"


# Include API v1 routes
app.include_router(api_router, prefix="/api/v1")


# Initialize MCP integration
mcp = FastApiMCP(
    app,
    name="Payment Revenue Tracker",
    description="AI-powered payment and revenue tracking system with advanced time-based queries",
    include_tags=["revenue"],
)
mcp.mount()
