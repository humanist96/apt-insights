"""
API usage tracking service
Uses Redis to track API calls per user with daily reset
"""
import os
from datetime import datetime, timedelta
from typing import Optional, Dict
import structlog

try:
    import redis
    from redis import Redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

logger = structlog.get_logger(__name__)

# Configuration
USE_REDIS = os.getenv('USE_REDIS', 'False').lower() == 'true'
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')


class UsageTrackingService:
    """
    Service for tracking API usage per user

    Features:
    - Tracks API calls per user per day
    - Automatic daily reset at midnight
    - Rate limiting support
    - Usage statistics
    """

    def __init__(self, redis_url: str = REDIS_URL):
        """
        Initialize usage tracking service

        Args:
            redis_url: Redis connection URL
        """
        self.logger = logger
        self.redis_url = redis_url
        self.client: Optional[Redis] = None
        self.enabled = USE_REDIS and REDIS_AVAILABLE

        if self.enabled:
            self._connect()
        else:
            self.logger.warning(
                "usage_tracking_disabled",
                reason="Redis not available or disabled",
            )

    def _connect(self):
        """Connect to Redis"""
        try:
            self.client = redis.from_url(
                self.redis_url,
                encoding='utf-8',
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
            )
            self.client.ping()
            self.logger.info("usage_tracking_connected", url=self.redis_url)
        except Exception as e:
            self.logger.error("usage_tracking_connection_failed", error=str(e))
            self.client = None
            self.enabled = False

    def _get_usage_key(self, user_id: str) -> str:
        """
        Generate Redis key for user usage

        Args:
            user_id: User identifier

        Returns:
            Redis key: apt_insights:usage:{user_id}:{date}
        """
        date_str = datetime.now().strftime('%Y-%m-%d')
        return f"apt_insights:usage:{user_id}:{date_str}"

    def _get_ttl_seconds(self) -> int:
        """
        Calculate TTL in seconds until end of day

        Returns:
            Seconds until midnight
        """
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        return int((midnight - now).total_seconds())

    def increment_usage(self, user_id: str) -> int:
        """
        Increment API call count for user

        Args:
            user_id: User identifier

        Returns:
            Current usage count (0 if Redis unavailable)
        """
        if not self.enabled or not self.client:
            return 0

        key = self._get_usage_key(user_id)

        try:
            # Increment counter
            count = self.client.incr(key)

            # Set expiration on first increment of the day
            if count == 1:
                ttl = self._get_ttl_seconds()
                self.client.expire(key, ttl)

            self.logger.debug(
                "usage_incremented",
                user_id=user_id,
                count=count,
            )

            return count

        except Exception as e:
            self.logger.error(
                "usage_increment_error",
                user_id=user_id,
                error=str(e),
            )
            return 0

    def get_usage(self, user_id: str) -> int:
        """
        Get current API call count for user

        Args:
            user_id: User identifier

        Returns:
            Current usage count (0 if not found or Redis unavailable)
        """
        if not self.enabled or not self.client:
            return 0

        key = self._get_usage_key(user_id)

        try:
            count = self.client.get(key)
            return int(count) if count else 0

        except Exception as e:
            self.logger.error(
                "usage_get_error",
                user_id=user_id,
                error=str(e),
            )
            return 0

    def check_rate_limit(
        self,
        user_id: str,
        limit: Optional[int],
    ) -> bool:
        """
        Check if user has exceeded rate limit

        Args:
            user_id: User identifier
            limit: API call limit (None = unlimited)

        Returns:
            True if within limit, False if exceeded
        """
        # Unlimited for premium users
        if limit is None:
            return True

        current_usage = self.get_usage(user_id)

        if current_usage >= limit:
            self.logger.warning(
                "rate_limit_exceeded",
                user_id=user_id,
                current_usage=current_usage,
                limit=limit,
            )
            return False

        return True

    def get_usage_stats(self, user_id: str, limit: Optional[int]) -> Dict:
        """
        Get usage statistics for user

        Args:
            user_id: User identifier
            limit: API call limit (None = unlimited)

        Returns:
            Usage statistics dict
        """
        current_usage = self.get_usage(user_id)

        if limit is None:
            # Premium user
            return {
                "used": current_usage,
                "limit": None,
                "remaining": None,
                "percentage": 0,
                "unlimited": True,
            }

        # Free user
        remaining = max(0, limit - current_usage)
        percentage = (current_usage / limit * 100) if limit > 0 else 0

        return {
            "used": current_usage,
            "limit": limit,
            "remaining": remaining,
            "percentage": round(percentage, 2),
            "unlimited": False,
        }

    def reset_usage(self, user_id: str) -> bool:
        """
        Manually reset usage for user (admin function)

        Args:
            user_id: User identifier

        Returns:
            Success status
        """
        if not self.enabled or not self.client:
            return False

        key = self._get_usage_key(user_id)

        try:
            self.client.delete(key)
            self.logger.info("usage_reset", user_id=user_id)
            return True

        except Exception as e:
            self.logger.error(
                "usage_reset_error",
                user_id=user_id,
                error=str(e),
            )
            return False


# Singleton instance
_usage_tracking_service: Optional[UsageTrackingService] = None


def get_usage_tracking_service() -> UsageTrackingService:
    """
    Get usage tracking service singleton

    Returns:
        UsageTrackingService instance
    """
    global _usage_tracking_service
    if _usage_tracking_service is None:
        _usage_tracking_service = UsageTrackingService()
    return _usage_tracking_service
