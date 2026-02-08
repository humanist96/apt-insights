"""
Redis Cache Warming and Management

Pre-populate cache with frequently accessed data to improve response times.
"""

import redis
import json
import structlog
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import settings

logger = structlog.get_logger()


class CacheWarmer:
    """Warm up Redis cache with popular queries"""

    def __init__(self, redis_url: str):
        """
        Initialize cache warmer

        Args:
            redis_url: Redis connection URL
        """
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.cache_ttl = 3600  # 1 hour for warmed cache

    def get_cache_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """
        Generate cache key from endpoint and parameters

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Cache key string
        """
        params_str = json.dumps(params, sort_keys=True)
        return f"cache:{endpoint}:{hash(params_str)}"

    def set_cache(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set cache value

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds

        Returns:
            True if successful
        """
        try:
            value_json = json.dumps(value)
            self.redis_client.setex(
                key,
                ttl or self.cache_ttl,
                value_json
            )
            logger.info("cache_set", key=key, ttl=ttl or self.cache_ttl)
            return True
        except Exception as e:
            logger.error("cache_set_failed", key=key, error=str(e))
            return False

    def get_cache(self, key: str) -> Optional[Any]:
        """
        Get cache value

        Args:
            key: Cache key

        Returns:
            Cached value or None
        """
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error("cache_get_failed", key=key, error=str(e))
            return None

    def warm_popular_queries(self) -> int:
        """
        Warm cache with popular query patterns

        Returns:
            Number of queries warmed
        """
        # Popular regions
        regions = ["강남구", "서초구", "송파구", "강동구", "마포구", "용산구"]

        # Date ranges
        now = datetime.now()
        date_ranges = [
            # Last month
            {
                "start_date": (now - timedelta(days=30)).strftime("%Y-%m-%d"),
                "end_date": now.strftime("%Y-%m-%d")
            },
            # Last 3 months
            {
                "start_date": (now - timedelta(days=90)).strftime("%Y-%m-%d"),
                "end_date": now.strftime("%Y-%m-%d")
            },
            # Last 6 months
            {
                "start_date": (now - timedelta(days=180)).strftime("%Y-%m-%d"),
                "end_date": now.strftime("%Y-%m-%d")
            },
            # Last year
            {
                "start_date": (now - timedelta(days=365)).strftime("%Y-%m-%d"),
                "end_date": now.strftime("%Y-%m-%d")
            }
        ]

        # Popular endpoints
        endpoints = [
            "/api/v1/analysis/basic-stats",
            "/api/v1/analysis/price-trend",
            "/api/v1/analysis/regional",
            "/api/v1/segmentation/by-area",
            "/api/v1/investment/jeonse-ratio",
            "/api/v1/market/signals"
        ]

        warmed_count = 0

        # Generate cache keys for popular combinations
        for region in regions:
            for date_range in date_ranges:
                for endpoint in endpoints:
                    params = {
                        "region_filter": region,
                        **date_range
                    }

                    cache_key = self.get_cache_key(endpoint, params)

                    # Mark as warmed (actual data will be populated on first request)
                    # This is a placeholder strategy - in production, you'd fetch actual data
                    self.redis_client.setex(
                        f"warmed:{cache_key}",
                        self.cache_ttl,
                        "true"
                    )

                    warmed_count += 1

        logger.info("cache_warmed", count=warmed_count)
        return warmed_count

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics

        Returns:
            Cache statistics including hit rate, memory usage
        """
        try:
            info = self.redis_client.info()

            stats = {
                "timestamp": datetime.utcnow().isoformat(),
                "total_keys": self.redis_client.dbsize(),
                "memory_used_mb": info.get("used_memory", 0) / (1024 * 1024),
                "memory_used_human": info.get("used_memory_human", "N/A"),
                "total_connections": info.get("total_connections_received", 0),
                "total_commands": info.get("total_commands_processed", 0),
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0),
                "evicted_keys": info.get("evicted_keys", 0),
                "expired_keys": info.get("expired_keys", 0)
            }

            # Calculate hit rate
            total_requests = stats["hits"] + stats["misses"]
            if total_requests > 0:
                stats["hit_rate"] = (stats["hits"] / total_requests) * 100
            else:
                stats["hit_rate"] = 0

            logger.info("cache_stats_retrieved", hit_rate=stats["hit_rate"])
            return stats

        except Exception as e:
            logger.error("failed_to_get_cache_stats", error=str(e))
            return {}

    def clear_cache(self, pattern: Optional[str] = None) -> int:
        """
        Clear cache by pattern

        Args:
            pattern: Redis key pattern (e.g., "cache:*")

        Returns:
            Number of keys deleted
        """
        try:
            if pattern:
                keys = self.redis_client.keys(pattern)
                if keys:
                    deleted = self.redis_client.delete(*keys)
                    logger.info("cache_cleared_by_pattern", pattern=pattern, count=deleted)
                    return deleted
            else:
                self.redis_client.flushdb()
                logger.info("cache_cleared_all")
                return -1  # All keys deleted

            return 0
        except Exception as e:
            logger.error("cache_clear_failed", pattern=pattern, error=str(e))
            return 0

    def batch_invalidate(self, patterns: List[str]) -> int:
        """
        Batch invalidate cache keys by patterns

        Args:
            patterns: List of key patterns to invalidate

        Returns:
            Total number of keys deleted
        """
        total_deleted = 0

        for pattern in patterns:
            deleted = self.clear_cache(pattern)
            total_deleted += deleted if deleted > 0 else 0

        logger.info("batch_invalidate_complete", patterns=patterns, total_deleted=total_deleted)
        return total_deleted

    def monitor_cache_health(self) -> Dict[str, Any]:
        """
        Monitor cache health and return warnings

        Returns:
            Health status with warnings
        """
        stats = self.get_cache_stats()
        health = {
            "status": "healthy",
            "warnings": []
        }

        # Check hit rate
        if stats.get("hit_rate", 0) < 50:
            health["warnings"].append({
                "type": "low_hit_rate",
                "message": f"Cache hit rate is low: {stats['hit_rate']:.2f}%",
                "recommendation": "Consider warming cache with popular queries"
            })

        # Check memory usage
        memory_mb = stats.get("memory_used_mb", 0)
        if memory_mb > 500:  # 500MB threshold
            health["warnings"].append({
                "type": "high_memory",
                "message": f"Cache memory usage is high: {memory_mb:.2f}MB",
                "recommendation": "Consider reducing cache TTL or clearing old entries"
            })

        # Check eviction rate
        evicted = stats.get("evicted_keys", 0)
        if evicted > 1000:
            health["warnings"].append({
                "type": "high_eviction",
                "message": f"High eviction rate: {evicted} keys evicted",
                "recommendation": "Increase Redis max memory or reduce cache size"
            })

        if health["warnings"]:
            health["status"] = "warning"

        return health

    def get_top_keys(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get most frequently accessed cache keys (requires Redis 4.0+)

        Args:
            limit: Number of top keys to return

        Returns:
            List of top keys with access counts
        """
        try:
            # Get all keys (for small datasets)
            all_keys = self.redis_client.keys("cache:*")

            key_stats = []
            for key in all_keys[:1000]:  # Limit to first 1000 keys
                ttl = self.redis_client.ttl(key)
                memory = self.redis_client.memory_usage(key) if hasattr(self.redis_client, 'memory_usage') else 0

                key_stats.append({
                    "key": key,
                    "ttl": ttl,
                    "memory_bytes": memory
                })

            # Sort by memory usage
            key_stats.sort(key=lambda x: x["memory_bytes"], reverse=True)

            return key_stats[:limit]

        except Exception as e:
            logger.error("failed_to_get_top_keys", error=str(e))
            return []


async def run_cache_warming():
    """
    Run cache warming process asynchronously
    """
    try:
        redis_url = settings.REDIS_URL
    except:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    warmer = CacheWarmer(redis_url)

    logger.info("starting_cache_warming")

    # Get initial stats
    initial_stats = warmer.get_cache_stats()
    print("\n" + "="*60)
    print("INITIAL CACHE STATS")
    print("="*60)
    print(f"Total Keys: {initial_stats.get('total_keys', 0)}")
    print(f"Memory Used: {initial_stats.get('memory_used_human', 'N/A')}")
    print(f"Hit Rate: {initial_stats.get('hit_rate', 0):.2f}%")

    # Warm popular queries
    print("\n" + "="*60)
    print("WARMING CACHE WITH POPULAR QUERIES")
    print("="*60)
    warmed_count = warmer.warm_popular_queries()
    print(f"Warmed {warmed_count} query patterns")

    # Get updated stats
    updated_stats = warmer.get_cache_stats()
    print("\n" + "="*60)
    print("UPDATED CACHE STATS")
    print("="*60)
    print(f"Total Keys: {updated_stats.get('total_keys', 0)}")
    print(f"Memory Used: {updated_stats.get('memory_used_human', 'N/A')}")
    print(f"Hit Rate: {updated_stats.get('hit_rate', 0):.2f}%")

    # Check health
    health = warmer.monitor_cache_health()
    print("\n" + "="*60)
    print("CACHE HEALTH")
    print("="*60)
    print(f"Status: {health['status'].upper()}")
    if health['warnings']:
        print("\nWarnings:")
        for warning in health['warnings']:
            print(f"  - [{warning['type']}] {warning['message']}")
            print(f"    Recommendation: {warning['recommendation']}")
    else:
        print("No warnings")

    logger.info("cache_warming_complete", warmed_count=warmed_count)


if __name__ == "__main__":
    asyncio.run(run_cache_warming())
