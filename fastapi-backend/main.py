"""
FastAPI Application Entry Point
Korean Apartment Real Estate Transaction Analysis Platform
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import structlog
import os

# Import monitoring configuration
from config.sentry import init_sentry
from config.logging import setup_logging
from prometheus_fastapi_instrumentator import Instrumentator

from middleware import setup_cors, setup_compression, setup_rate_limiting
from middleware.logging import setup_logging_middleware
from routers import (
    analysis_router,
    segmentation_router,
    premium_router,
    investment_router,
    market_router,
    payment_router,
    subscriptions_router,
    export_router,
)
from routers.health import router as health_router
from routers.metrics import router as metrics_router
from auth import auth_router

# Initialize logging first
setup_logging()
logger = structlog.get_logger(__name__)

# Initialize Sentry
init_sentry()

# Create FastAPI application
app = FastAPI(
    title="Apartment Transaction Analysis API",
    description="""
    Korean apartment real estate transaction price analysis platform.

    Provides comprehensive analysis of apartment transaction data including:
    - Basic statistics (count, average/min/max prices, area)
    - Price trends over time
    - Regional comparisons
    - And more advanced analytics

    Data sources:
    - PostgreSQL database (when USE_DATABASE=true)
    - JSON files from api_*/output/ directories (fallback mode)

    **Dataset**: 63,809 apartment transactions from Korean Ministry of Land APIs
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# Setup middleware
setup_compression(app)  # Apply compression first
setup_cors(app)
setup_logging_middleware(app)
setup_rate_limiting(app)

# Setup Prometheus instrumentation
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics", "/health", "/health/.*"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="http_requests_inprogress",
    inprogress_labels=True,
)
instrumentator.instrument(app)

# Include routers
app.include_router(health_router)
app.include_router(metrics_router)
app.include_router(auth_router)
app.include_router(payment_router)
app.include_router(subscriptions_router)
app.include_router(export_router)
app.include_router(analysis_router)
app.include_router(segmentation_router)
app.include_router(premium_router)
app.include_router(investment_router)
app.include_router(market_router)


# Health check endpoint
@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Check if the API is running and healthy",
)
async def health_check():
    """
    Health check endpoint

    Returns:
        Health status and basic information
    """
    return {
        "status": "healthy",
        "service": "apartment-transaction-analysis-api",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


# Root endpoint
@app.get(
    "/",
    tags=["root"],
    summary="API information",
    description="Get basic information about the API",
)
async def root():
    """
    Root endpoint with API information

    Returns:
        API information and available endpoints
    """
    return {
        "service": "Apartment Transaction Analysis API",
        "version": "1.0.0",
        "description": "Korean apartment real estate transaction analysis platform",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "api": "/api/v1/analysis",
        },
        "documentation": "Visit /docs for interactive API documentation",
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors

    Args:
        request: The request that caused the error
        exc: The exception that was raised

    Returns:
        JSON error response
    """
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        error_type=type(exc).__name__,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error occurred",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat(),
        },
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler
    """
    logger.info(
        "application_startup",
        service="apartment-transaction-analysis-api",
        version=os.getenv("APP_VERSION", "1.0.0"),
        environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
    )

    # Expose metrics endpoint
    instrumentator.expose(app, endpoint="/api/metrics", include_in_schema=False)

    # Warm cache on startup (optional, controlled by env var)
    if os.getenv("WARM_CACHE_ON_STARTUP", "false").lower() == "true":
        try:
            from cache_warming import CacheWarmer
            warmer = CacheWarmer()
            await warmer.warm_specific(['basic-stats'])
            logger.info("cache_warming_completed")
        except Exception as e:
            logger.warning("cache_warming_failed", error=str(e))


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler
    """
    logger.info(
        "application_shutdown",
        service="apartment-transaction-analysis-api",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
