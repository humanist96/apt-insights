"""
Health Check and Metrics Endpoints
Comprehensive health monitoring with dependency checks
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
import structlog
import os
import asyncio

from backend.db.session import get_db_session
from backend.cache.redis_client import get_redis_client
import requests

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api", tags=["health"])


class HealthStatus(BaseModel):
    """Basic health status response"""
    status: str
    service: str
    version: str
    timestamp: str


class DependencyStatus(BaseModel):
    """Individual dependency health status"""
    status: str
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    details: Optional[Dict] = None


class DetailedHealthStatus(BaseModel):
    """Detailed health status with all dependencies"""
    status: str
    service: str
    version: str
    timestamp: str
    dependencies: Dict[str, DependencyStatus]
    uptime_seconds: Optional[float] = None


# Track application start time
APP_START_TIME = datetime.now()


@router.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Basic health check endpoint

    Returns:
        200: Service is healthy
    """
    return {
        "status": "healthy",
        "service": "apartment-transaction-analysis-api",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/health/detailed", response_model=DetailedHealthStatus)
async def detailed_health_check():
    """
    Detailed health check with all dependencies

    Checks:
    - Database connectivity
    - Redis connectivity
    - External API availability (Korean Ministry of Land)

    Returns:
        200: All dependencies healthy
        503: One or more dependencies unhealthy
    """
    start_time = datetime.now()

    dependencies = {
        "database": await check_database(),
        "redis": await check_redis(),
        "external_api": await check_external_api(),
    }

    # Determine overall status
    overall_status = "healthy"
    if any(dep.status == "unhealthy" for dep in dependencies.values()):
        overall_status = "degraded"
    if all(dep.status == "unhealthy" for dep in dependencies.values()):
        overall_status = "unhealthy"

    # Calculate uptime
    uptime = (datetime.now() - APP_START_TIME).total_seconds()

    response = {
        "status": overall_status,
        "service": "apartment-transaction-analysis-api",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "timestamp": datetime.now().isoformat(),
        "dependencies": dependencies,
        "uptime_seconds": uptime,
    }

    # Return 503 if overall status is unhealthy
    if overall_status == "unhealthy":
        logger.error("health_check_failed", dependencies=dependencies)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=response,
        )

    return response


async def check_database() -> DependencyStatus:
    """Check PostgreSQL database connectivity"""
    start_time = datetime.now()

    try:
        db = next(get_db_session())
        # Simple query to check connection
        db.execute("SELECT 1")
        db.close()

        latency = (datetime.now() - start_time).total_seconds() * 1000

        return DependencyStatus(
            status="healthy",
            latency_ms=round(latency, 2),
        )
    except Exception as e:
        logger.error("database_health_check_failed", error=str(e))
        return DependencyStatus(
            status="unhealthy",
            error=str(e),
        )


async def check_redis() -> DependencyStatus:
    """Check Redis connectivity"""
    start_time = datetime.now()

    try:
        redis_client = get_redis_client()

        # Check if Redis is available
        if not redis_client:
            return DependencyStatus(
                status="disabled",
                details={"message": "Redis not configured"},
            )

        # Ping Redis
        redis_client.ping()

        latency = (datetime.now() - start_time).total_seconds() * 1000

        # Get additional info
        info = redis_client.info()
        details = {
            "connected_clients": info.get("connected_clients"),
            "used_memory_human": info.get("used_memory_human"),
            "uptime_in_seconds": info.get("uptime_in_seconds"),
        }

        return DependencyStatus(
            status="healthy",
            latency_ms=round(latency, 2),
            details=details,
        )
    except Exception as e:
        logger.error("redis_health_check_failed", error=str(e))
        return DependencyStatus(
            status="unhealthy",
            error=str(e),
        )


async def check_external_api() -> DependencyStatus:
    """Check external API availability (Korean Ministry of Land)"""
    start_time = datetime.now()

    try:
        # Check if we can reach the external API
        # Using a simple HEAD request to avoid quota usage
        api_url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade"

        response = await asyncio.to_thread(
            requests.head,
            api_url,
            timeout=5,
        )

        latency = (datetime.now() - start_time).total_seconds() * 1000

        # API responds even without valid params
        if response.status_code in [200, 400]:
            return DependencyStatus(
                status="healthy",
                latency_ms=round(latency, 2),
            )
        else:
            return DependencyStatus(
                status="degraded",
                latency_ms=round(latency, 2),
                details={"status_code": response.status_code},
            )
    except Exception as e:
        logger.warning("external_api_health_check_failed", error=str(e))
        return DependencyStatus(
            status="degraded",
            error=str(e),
            details={"message": "External API check failed, but service can continue"},
        )


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness probe for Kubernetes/load balancers

    Returns:
        200: Service is ready to receive traffic
        503: Service is not ready
    """
    # Check critical dependencies
    db_status = await check_database()

    if db_status.status == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready", "reason": "database_unavailable"},
        )

    return {"status": "ready", "timestamp": datetime.now().isoformat()}


@router.get("/health/live")
async def liveness_check():
    """
    Liveness probe for Kubernetes

    Returns:
        200: Service is alive
    """
    return {"status": "alive", "timestamp": datetime.now().isoformat()}
