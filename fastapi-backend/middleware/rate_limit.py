"""
Rate limiting middleware
Checks API usage limits based on user subscription tier
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

from services.subscription_service import get_subscription_service
from services.usage_tracking import get_usage_tracking_service

logger = structlog.get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce API rate limits

    Features:
    - Checks subscription tier
    - Tracks API usage
    - Returns 429 when limit exceeded
    - Adds usage headers to response
    """

    def __init__(self, app):
        """
        Initialize rate limit middleware

        Args:
            app: FastAPI application
        """
        super().__init__(app)
        self.subscription_service = get_subscription_service()
        self.usage_service = get_usage_tracking_service()

        # Paths exempt from rate limiting
        self.exempt_paths = {
            "/health",
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/subscriptions/plans",
            "/api/v1/subscriptions/current",
            "/api/v1/subscriptions/upgrade",
        }

    def _is_exempt(self, path: str) -> bool:
        """
        Check if path is exempt from rate limiting

        Args:
            path: Request path

        Returns:
            True if exempt
        """
        return path in self.exempt_paths

    def _get_user_id(self, request: Request) -> str:
        """
        Extract user ID from request

        For now, uses a demo user. In production, this would:
        - Parse JWT token
        - Extract user ID from session
        - Use API key

        Args:
            request: HTTP request

        Returns:
            User identifier
        """
        # TODO: Replace with real authentication
        # For now, use header or default to demo user
        return request.headers.get("X-User-Id", "demo_user")

    async def dispatch(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: HTTP request
            call_next: Next middleware handler

        Returns:
            HTTP response
        """
        # Skip exempt paths
        if self._is_exempt(request.url.path):
            return await call_next(request)

        # Get user ID
        user_id = self._get_user_id(request)

        # Get user subscription
        subscription = self.subscription_service.get_user_subscription(user_id)

        # Check rate limit
        api_limit = subscription.api_calls_limit

        if not self.usage_service.check_rate_limit(user_id, api_limit):
            # Rate limit exceeded
            usage_stats = self.usage_service.get_usage_stats(user_id, api_limit)

            logger.warning(
                "rate_limit_exceeded",
                user_id=user_id,
                path=request.url.path,
                usage=usage_stats,
            )

            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "error": "API rate limit exceeded",
                    "message": f"무료 사용자는 하루 {api_limit}회까지 API를 호출할 수 있습니다.",
                    "usage": usage_stats,
                    "upgrade_info": {
                        "message": "프리미엄으로 업그레이드하여 무제한 API 호출을 이용하세요",
                        "upgrade_url": "/subscription",
                    },
                },
                headers={
                    "X-RateLimit-Limit": str(api_limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": "midnight",
                },
            )

        # Increment usage counter
        current_usage = self.usage_service.increment_usage(user_id)

        # Process request
        response = await call_next(request)

        # Add usage headers
        if api_limit is not None:
            remaining = max(0, api_limit - current_usage)
            response.headers["X-RateLimit-Limit"] = str(api_limit)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = "midnight"
        else:
            # Premium user - unlimited
            response.headers["X-RateLimit-Limit"] = "unlimited"

        return response


def setup_rate_limiting(app):
    """
    Setup rate limiting middleware

    Args:
        app: FastAPI application
    """
    app.add_middleware(RateLimitMiddleware)
    logger.info("rate_limiting_middleware_configured")
