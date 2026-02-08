"""
Redis Cache Warming Script

Pre-populates Redis cache with frequently accessed data on application startup
or on-demand via CLI.

Usage:
    # Warm cache on startup
    python cache_warming.py --startup

    # Warm specific endpoints
    python cache_warming.py --endpoints basic-stats price-trend

    # Full cache warming
    python cache_warming.py --full
"""
import sys
import asyncio
import argparse
from pathlib import Path
from typing import List, Optional
import structlog

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.analyzer_service import AnalyzerService
from backend.cache.redis_client import get_redis_cache

logger = structlog.get_logger(__name__)


class CacheWarmer:
    """Cache warming utility for frequently accessed data"""

    def __init__(self):
        """Initialize cache warmer"""
        self.analyzer = AnalyzerService()
        self.cache = get_redis_cache()

    async def warm_basic_stats(self) -> bool:
        """
        Warm cache for basic statistics endpoint

        Returns:
            True if successful
        """
        try:
            logger.info("warming_basic_stats")

            # Load and cache basic statistics
            result = self.analyzer.get_basic_stats()

            logger.info(
                "basic_stats_warmed",
                total_count=result.get('stats', {}).get('total_count', 0)
            )
            return True
        except Exception as e:
            logger.error("basic_stats_warming_failed", error=str(e))
            return False

    async def warm_price_trend(self) -> bool:
        """
        Warm cache for price trend endpoint

        Returns:
            True if successful
        """
        try:
            logger.info("warming_price_trend")

            # Load and cache price trend data
            result = self.analyzer.get_price_trend()

            logger.info(
                "price_trend_warmed",
                data_points=len(result.get('trend_data', []))
            )
            return True
        except Exception as e:
            logger.error("price_trend_warming_failed", error=str(e))
            return False

    async def warm_regional_comparison(self) -> bool:
        """
        Warm cache for regional comparison endpoint

        Returns:
            True if successful
        """
        try:
            logger.info("warming_regional_comparison")

            # Load and cache regional comparison data
            result = self.analyzer.get_regional_comparison()

            logger.info(
                "regional_comparison_warmed",
                regions=len(result.get('comparison', {}).get('regions', []))
            )
            return True
        except Exception as e:
            logger.error("regional_comparison_warming_failed", error=str(e))
            return False

    async def warm_all(self) -> dict:
        """
        Warm all frequently accessed endpoints

        Returns:
            Dictionary with warming results
        """
        logger.info("starting_full_cache_warming")

        results = {
            'basic_stats': await self.warm_basic_stats(),
            'price_trend': await self.warm_price_trend(),
            'regional_comparison': await self.warm_regional_comparison(),
        }

        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)

        logger.info(
            "cache_warming_completed",
            success=success_count,
            total=total_count,
            success_rate=f"{(success_count/total_count)*100:.1f}%"
        )

        return results

    async def warm_specific(self, endpoints: List[str]) -> dict:
        """
        Warm specific endpoints

        Args:
            endpoints: List of endpoint names to warm

        Returns:
            Dictionary with warming results
        """
        logger.info("warming_specific_endpoints", endpoints=endpoints)

        endpoint_map = {
            'basic-stats': self.warm_basic_stats,
            'price-trend': self.warm_price_trend,
            'regional-comparison': self.warm_regional_comparison,
        }

        results = {}
        for endpoint in endpoints:
            if endpoint in endpoint_map:
                results[endpoint] = await endpoint_map[endpoint]()
            else:
                logger.warning("unknown_endpoint", endpoint=endpoint)
                results[endpoint] = False

        return results


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Redis cache warming utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Startup warming (critical endpoints only)
  python cache_warming.py --startup

  # Full cache warming
  python cache_warming.py --full

  # Specific endpoints
  python cache_warming.py --endpoints basic-stats price-trend
        """
    )

    parser.add_argument(
        '--startup',
        action='store_true',
        help='Warm critical endpoints for startup'
    )

    parser.add_argument(
        '--full',
        action='store_true',
        help='Warm all endpoints'
    )

    parser.add_argument(
        '--endpoints',
        nargs='+',
        help='Specific endpoints to warm'
    )

    args = parser.parse_args()

    # Initialize warmer
    warmer = CacheWarmer()

    # Check Redis connection
    if not warmer.cache or not warmer.cache.is_connected():
        logger.error("redis_not_available")
        print("\n❌ Redis cache is not available")
        print("   - Ensure Redis server is running")
        print("   - Check USE_REDIS=true in .env")
        return 1

    # Execute warming based on arguments
    if args.startup:
        logger.info("startup_warming_mode")
        # Warm only critical endpoints for fast startup
        results = await warmer.warm_specific(['basic-stats'])
    elif args.full:
        logger.info("full_warming_mode")
        results = await warmer.warm_all()
    elif args.endpoints:
        results = await warmer.warm_specific(args.endpoints)
    else:
        # Default: startup mode
        results = await warmer.warm_specific(['basic-stats'])

    # Print results
    print("\n" + "="*60)
    print("📊 Cache Warming Results")
    print("="*60)

    for endpoint, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {endpoint}")

    print("="*60 + "\n")

    return 0 if all(results.values()) else 1


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
