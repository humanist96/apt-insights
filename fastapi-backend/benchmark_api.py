"""
API Performance Benchmarking Script

Measures response times for all API endpoints and generates performance report.

Usage:
    # Run benchmarks with default settings
    python benchmark_api.py

    # Custom settings
    python benchmark_api.py --url http://localhost:8000 --requests 100 --warmup 10

    # Save results to file
    python benchmark_api.py --output benchmark_results.json
"""
import asyncio
import argparse
import time
import statistics
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
import structlog

logger = structlog.get_logger(__name__)


class APIBenchmark:
    """API performance benchmarking utility"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize benchmark

        Args:
            base_url: Base URL of the API
        """
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)

    async def measure_endpoint(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        warmup_requests: int = 3,
        test_requests: int = 50
    ) -> Dict[str, Any]:
        """
        Measure endpoint performance

        Args:
            endpoint: API endpoint path
            method: HTTP method
            params: Query parameters
            warmup_requests: Number of warmup requests
            test_requests: Number of test requests

        Returns:
            Performance statistics
        """
        url = f"{self.base_url}{endpoint}"

        # Warmup phase
        logger.info("warmup_phase", endpoint=endpoint, requests=warmup_requests)
        for _ in range(warmup_requests):
            try:
                await self.client.request(method, url, params=params)
            except Exception as e:
                logger.warning("warmup_request_failed", error=str(e))

        # Measurement phase
        logger.info("measurement_phase", endpoint=endpoint, requests=test_requests)
        response_times: List[float] = []
        success_count = 0
        error_count = 0
        status_codes: Dict[int, int] = {}

        for i in range(test_requests):
            start = time.time()
            try:
                response = await self.client.request(method, url, params=params)
                duration_ms = (time.time() - start) * 1000

                response_times.append(duration_ms)
                success_count += 1

                # Track status codes
                status_codes[response.status_code] = status_codes.get(response.status_code, 0) + 1

            except Exception as e:
                duration_ms = (time.time() - start) * 1000
                error_count += 1
                logger.warning(
                    "request_failed",
                    endpoint=endpoint,
                    request=i+1,
                    error=str(e)
                )

        # Calculate statistics
        if response_times:
            sorted_times = sorted(response_times)
            p50_idx = int(len(sorted_times) * 0.50)
            p95_idx = int(len(sorted_times) * 0.95)
            p99_idx = int(len(sorted_times) * 0.99)

            stats = {
                'endpoint': endpoint,
                'method': method,
                'total_requests': test_requests,
                'success_count': success_count,
                'error_count': error_count,
                'status_codes': status_codes,
                'response_times_ms': {
                    'min': min(response_times),
                    'max': max(response_times),
                    'mean': statistics.mean(response_times),
                    'median': statistics.median(response_times),
                    'stdev': statistics.stdev(response_times) if len(response_times) > 1 else 0,
                    'p50': sorted_times[p50_idx],
                    'p95': sorted_times[p95_idx],
                    'p99': sorted_times[p99_idx],
                },
                'requests_per_second': success_count / (sum(response_times) / 1000) if response_times else 0,
            }
        else:
            stats = {
                'endpoint': endpoint,
                'method': method,
                'total_requests': test_requests,
                'success_count': 0,
                'error_count': error_count,
                'error': 'All requests failed'
            }

        return stats

    async def benchmark_all_endpoints(
        self,
        warmup_requests: int = 5,
        test_requests: int = 50
    ) -> Dict[str, Any]:
        """
        Benchmark all API endpoints

        Args:
            warmup_requests: Number of warmup requests per endpoint
            test_requests: Number of test requests per endpoint

        Returns:
            Complete benchmark results
        """
        logger.info("starting_benchmark_suite", warmup=warmup_requests, requests=test_requests)

        endpoints = [
            # Health and info
            {'path': '/health', 'name': 'Health Check'},
            {'path': '/', 'name': 'Root'},

            # Analysis endpoints
            {'path': '/api/v1/analysis/basic-stats', 'name': 'Basic Statistics'},
            {'path': '/api/v1/analysis/price-trend', 'name': 'Price Trend'},
            {'path': '/api/v1/analysis/regional-comparison', 'name': 'Regional Comparison'},
            {'path': '/api/v1/analysis/time-series', 'name': 'Time Series'},

            # Segmentation endpoints
            {'path': '/api/v1/segmentation/area-segments', 'name': 'Area Segments'},
            {'path': '/api/v1/segmentation/price-segments', 'name': 'Price Segments'},

            # Market endpoints
            {'path': '/api/v1/market/seasonal-trends', 'name': 'Seasonal Trends'},
            {'path': '/api/v1/market/price-volatility', 'name': 'Price Volatility'},
        ]

        results = []
        start_time = time.time()

        for endpoint_info in endpoints:
            logger.info("benchmarking_endpoint", endpoint=endpoint_info['path'])

            stats = await self.measure_endpoint(
                endpoint=endpoint_info['path'],
                warmup_requests=warmup_requests,
                test_requests=test_requests
            )

            stats['name'] = endpoint_info['name']
            results.append(stats)

        total_duration = time.time() - start_time

        # Generate summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'base_url': self.base_url,
            'warmup_requests': warmup_requests,
            'test_requests_per_endpoint': test_requests,
            'total_duration_seconds': total_duration,
            'endpoints_tested': len(results),
            'results': results,
        }

        return summary

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


def print_benchmark_results(results: Dict[str, Any]):
    """
    Print benchmark results in a readable format

    Args:
        results: Benchmark results dictionary
    """
    print("\n" + "="*80)
    print("📊 API Performance Benchmark Results")
    print("="*80)
    print(f"\nBase URL: {results['base_url']}")
    print(f"Timestamp: {results['timestamp']}")
    print(f"Warmup Requests: {results['warmup_requests']}")
    print(f"Test Requests per Endpoint: {results['test_requests_per_endpoint']}")
    print(f"Total Duration: {results['total_duration_seconds']:.2f}s")
    print(f"\n{'Endpoint':<40} {'Mean':>10} {'P50':>10} {'P95':>10} {'P99':>10}")
    print("-"*80)

    for endpoint in results['results']:
        name = endpoint.get('name', endpoint['endpoint'])[:38]

        if 'response_times_ms' in endpoint:
            rt = endpoint['response_times_ms']
            print(
                f"{name:<40} "
                f"{rt['mean']:>9.1f}ms "
                f"{rt['p50']:>9.1f}ms "
                f"{rt['p95']:>9.1f}ms "
                f"{rt['p99']:>9.1f}ms"
            )
        else:
            print(f"{name:<40} {'ERROR'}")

    print("="*80)

    # Performance targets
    print("\n📈 Performance Assessment")
    print("-"*80)

    targets_met = 0
    targets_failed = 0

    for endpoint in results['results']:
        if 'response_times_ms' not in endpoint:
            continue

        p95 = endpoint['response_times_ms']['p95']
        name = endpoint.get('name', endpoint['endpoint'])

        # Target: p95 < 500ms for all endpoints
        if p95 < 500:
            status = "✅ PASS"
            targets_met += 1
        else:
            status = "❌ FAIL"
            targets_failed += 1

        print(f"{status} {name}: P95 = {p95:.1f}ms (target: <500ms)")

    print("-"*80)
    print(f"Targets Met: {targets_met}/{targets_met + targets_failed}")
    print("="*80 + "\n")


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='API performance benchmarking tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '--url',
        default='http://localhost:8000',
        help='Base URL of the API (default: http://localhost:8000)'
    )

    parser.add_argument(
        '--requests',
        type=int,
        default=50,
        help='Number of test requests per endpoint (default: 50)'
    )

    parser.add_argument(
        '--warmup',
        type=int,
        default=5,
        help='Number of warmup requests per endpoint (default: 5)'
    )

    parser.add_argument(
        '--output',
        help='Save results to JSON file'
    )

    args = parser.parse_args()

    # Run benchmark
    benchmark = APIBenchmark(base_url=args.url)

    try:
        results = await benchmark.benchmark_all_endpoints(
            warmup_requests=args.warmup,
            test_requests=args.requests
        )

        # Print results
        print_benchmark_results(results)

        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Results saved to: {args.output}\n")

    finally:
        await benchmark.close()

    return 0


if __name__ == '__main__':
    asyncio.run(main())
