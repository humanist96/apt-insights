"""
Prometheus Metrics Endpoint
Application and business metrics
"""
from fastapi import APIRouter, Response
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    Info,
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
)
from prometheus_client.multiprocess import MultiProcessCollector
import os
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api", tags=["metrics"])

# Use multiprocess mode for production (when using multiple workers)
if "PROMETHEUS_MULTIPROC_DIR" in os.environ:
    registry = CollectorRegistry()
    MultiProcessCollector(registry)
else:
    from prometheus_client import REGISTRY as registry

# Application info
app_info = Info(
    "apartment_analysis_api",
    "Apartment Transaction Analysis API",
    registry=registry,
)
app_info.info({
    "version": os.getenv("APP_VERSION", "1.0.0"),
    "environment": os.getenv("SENTRY_ENVIRONMENT", "development"),
})

# HTTP request metrics (these are handled by prometheus-fastapi-instrumentator)
# But we can add custom business metrics

# Business metrics
api_requests_total = Counter(
    "api_requests_total",
    "Total API requests by endpoint",
    ["method", "endpoint", "status"],
    registry=registry,
)

analysis_requests_total = Counter(
    "analysis_requests_total",
    "Total analysis requests by type",
    ["analysis_type"],
    registry=registry,
)

analysis_duration_seconds = Histogram(
    "analysis_duration_seconds",
    "Time spent processing analysis requests",
    ["analysis_type"],
    registry=registry,
)

cache_hits_total = Counter(
    "cache_hits_total",
    "Total cache hits",
    ["cache_type"],
    registry=registry,
)

cache_misses_total = Counter(
    "cache_misses_total",
    "Total cache misses",
    ["cache_type"],
    registry=registry,
)

database_queries_total = Counter(
    "database_queries_total",
    "Total database queries",
    ["query_type"],
    registry=registry,
)

database_query_duration_seconds = Histogram(
    "database_query_duration_seconds",
    "Time spent on database queries",
    ["query_type"],
    registry=registry,
)

external_api_requests_total = Counter(
    "external_api_requests_total",
    "Total external API requests",
    ["api_name", "status"],
    registry=registry,
)

external_api_duration_seconds = Histogram(
    "external_api_duration_seconds",
    "Time spent on external API requests",
    ["api_name"],
    registry=registry,
)

# Active connections/sessions
active_connections = Gauge(
    "active_connections",
    "Number of active connections",
    registry=registry,
)

active_database_connections = Gauge(
    "active_database_connections",
    "Number of active database connections",
    registry=registry,
)

# User metrics
authenticated_users = Gauge(
    "authenticated_users",
    "Number of authenticated users in last hour",
    registry=registry,
)

subscription_users_total = Gauge(
    "subscription_users_total",
    "Total number of users with active subscriptions",
    ["plan_type"],
    registry=registry,
)

# Data metrics
total_transactions_in_database = Gauge(
    "total_transactions_in_database",
    "Total number of apartment transactions in database",
    registry=registry,
)

# Error metrics
errors_total = Counter(
    "errors_total",
    "Total errors by type",
    ["error_type", "severity"],
    registry=registry,
)


@router.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint

    Returns:
        Prometheus-formatted metrics
    """
    try:
        metrics_output = generate_latest(registry)
        return Response(
            content=metrics_output,
            media_type=CONTENT_TYPE_LATEST,
        )
    except Exception as e:
        logger.error("metrics_generation_failed", error=str(e))
        return Response(
            content=f"# Error generating metrics: {str(e)}",
            media_type=CONTENT_TYPE_LATEST,
            status_code=500,
        )


# Helper functions to update metrics
def record_analysis_request(analysis_type: str):
    """Record an analysis request"""
    analysis_requests_total.labels(analysis_type=analysis_type).inc()


def record_analysis_duration(analysis_type: str, duration_seconds: float):
    """Record analysis processing time"""
    analysis_duration_seconds.labels(analysis_type=analysis_type).observe(duration_seconds)


def record_cache_hit(cache_type: str = "redis"):
    """Record a cache hit"""
    cache_hits_total.labels(cache_type=cache_type).inc()


def record_cache_miss(cache_type: str = "redis"):
    """Record a cache miss"""
    cache_misses_total.labels(cache_type=cache_type).inc()


def record_database_query(query_type: str, duration_seconds: float):
    """Record a database query"""
    database_queries_total.labels(query_type=query_type).inc()
    database_query_duration_seconds.labels(query_type=query_type).observe(duration_seconds)


def record_external_api_request(api_name: str, status: str, duration_seconds: float):
    """Record an external API request"""
    external_api_requests_total.labels(api_name=api_name, status=status).inc()
    external_api_duration_seconds.labels(api_name=api_name).observe(duration_seconds)


def record_error(error_type: str, severity: str = "error"):
    """Record an error"""
    errors_total.labels(error_type=error_type, severity=severity).inc()


def update_active_connections(count: int):
    """Update active connections gauge"""
    active_connections.set(count)


def update_database_connections(count: int):
    """Update active database connections gauge"""
    active_database_connections.set(count)


def update_subscription_users(plan_type: str, count: int):
    """Update subscription users gauge"""
    subscription_users_total.labels(plan_type=plan_type).set(count)


def update_total_transactions(count: int):
    """Update total transactions in database"""
    total_transactions_in_database.set(count)
