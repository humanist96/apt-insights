"""
Rate limiting middleware for API endpoints
"""
import time
from collections import defaultdict
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger(__name__)


class RateLimiter:
    """
    In-memory rate limiter with per-IP tracking

    For production, consider using Redis for distributed rate limiting
    """

    def __init__(self):
        # Store: {ip: [(timestamp, count), ...]}
        self.requests: Dict[str, list] = defaultdict(list)
        self.cleanup_interval = 60  # Clean up old entries every 60 seconds
        self.last_cleanup = time.time()

    def is_allowed(
        self,
        ip: str,
        limit: int,
        window: int,
    ) -> Tuple[bool, int, int]:
        """
        Check if request is allowed under rate limit

        Args:
            ip: Client IP address
            limit: Maximum requests allowed in window
            window: Time window in seconds

        Returns:
            Tuple of (is_allowed, requests_made, requests_remaining)
        """
        current_time = time.time()

        # Clean up old entries periodically
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup()

        # Get requests for this IP
        ip_requests = self.requests[ip]

        # Remove requests outside the current window
        cutoff_time = current_time - window
        ip_requests = [req_time for req_time in ip_requests if req_time > cutoff_time]
        self.requests[ip] = ip_requests

        # Check if limit exceeded
        requests_made = len(ip_requests)
        requests_remaining = max(0, limit - requests_made - 1)

        if requests_made >= limit:
            return False, requests_made, 0

        # Add current request
        ip_requests.append(current_time)

        return True, requests_made + 1, requests_remaining

    def _cleanup(self):
        """Remove expired entries to prevent memory growth"""
        current_time = time.time()
        self.last_cleanup = current_time

        # Remove IPs with no recent requests (older than 1 hour)
        cutoff = current_time - 3600
        ips_to_remove = []

        for ip, requests in self.requests.items():
            if not requests or max(requests) < cutoff:
                ips_to_remove.append(ip)

        for ip in ips_to_remove:
            del self.requests[ip]

        if ips_to_remove:
            logger.debug("rate_limiter_cleanup", removed_ips=len(ips_to_remove))


# Global rate limiter instance
rate_limiter = RateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware

    Free tier: 100 requests per hour
    Authenticated users: Based on subscription tier
    """

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Default rate limit (free tier)
        limit = 100
        window = 3600  # 1 hour

        # Check if authenticated (get user from Authorization header)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            # Authenticated users get higher limits
            # This could be enhanced to check subscription tier
            limit = 1000
            window = 3600

        # Check rate limit
        is_allowed, requests_made, requests_remaining = rate_limiter.is_allowed(
            client_ip, limit, window
        )

        # Add rate limit headers to response
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(requests_remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time() + window))

        # If rate limit exceeded, return 429
        if not is_allowed:
            logger.warning(
                "rate_limit_exceeded",
                ip=client_ip,
                requests_made=requests_made,
                limit=limit
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Limit: {limit} requests per hour",
                headers={
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time() + window)),
                },
            )

        return response


def setup_rate_limiting(app):
    """
    Setup rate limiting middleware

    Args:
        app: FastAPI application
    """
    app.add_middleware(RateLimitMiddleware)
    logger.info("rate_limiting_middleware_configured")
