"""
Comprehensive API Benchmark Suite

Benchmarks all API endpoints and generates performance report with percentiles.

Usage:
    python scripts/benchmark.py --host http://localhost:8000 --output benchmark_report.json
"""

import requests
import time
import statistics
import json
import argparse
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import sys


@dataclass
class BenchmarkResult:
    """Single benchmark result"""
    endpoint: str
    method: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    min_time_ms: float
    max_time_ms: float
    mean_time_ms: float
    median_time_ms: float
    p95_time_ms: float
    p99_time_ms: float
    requests_per_second: float
    total_duration_sec: float
    errors: List[str]


class APIBenchmark:
    """Benchmark API endpoints"""

    def __init__(self, base_url: str):
        """
        Initialize benchmark

        Args:
            base_url: API base URL
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def benchmark_endpoint(
        self,
        endpoint: str,
        method: str = "POST",
        payload: Optional[Dict[str, Any]] = None,
        iterations: int = 100,
        warmup: int = 5
    ) -> BenchmarkResult:
        """
        Benchmark single endpoint

        Args:
            endpoint: API endpoint path
            method: HTTP method
            payload: Request payload
            iterations: Number of benchmark iterations
            warmup: Number of warmup requests

        Returns:
            Benchmark result with statistics
        """
        url = f"{self.base_url}{endpoint}"
        response_times = []
        errors = []
        successful = 0
        failed = 0

        # Warmup phase
        print(f"  Warming up ({warmup} requests)...", end=' ', flush=True)
        for _ in range(warmup):
            try:
                if method == "POST":
                    self.session.post(url, json=payload, timeout=30)
                else:
                    self.session.get(url, timeout=30)
            except Exception:
                pass
        print("done")

        # Benchmark phase
        print(f"  Benchmarking ({iterations} requests)...", end=' ', flush=True)
        start_time = time.time()

        for i in range(iterations):
            request_start = time.time()

            try:
                if method == "POST":
                    response = self.session.post(url, json=payload, timeout=30)
                else:
                    response = self.session.get(url, timeout=30)

                request_end = time.time()
                response_time_ms = (request_end - request_start) * 1000

                if response.status_code == 200:
                    successful += 1
                    response_times.append(response_time_ms)
                else:
                    failed += 1
                    errors.append(f"HTTP {response.status_code}: {response.text[:100]}")

            except Exception as e:
                failed += 1
                errors.append(f"Request error: {str(e)}")

        end_time = time.time()
        total_duration = end_time - start_time
        print("done")

        # Calculate statistics
        if response_times:
            response_times.sort()
            n = len(response_times)

            result = BenchmarkResult(
                endpoint=endpoint,
                method=method,
                total_requests=iterations,
                successful_requests=successful,
                failed_requests=failed,
                min_time_ms=min(response_times),
                max_time_ms=max(response_times),
                mean_time_ms=statistics.mean(response_times),
                median_time_ms=statistics.median(response_times),
                p95_time_ms=response_times[int(n * 0.95)] if n > 0 else 0,
                p99_time_ms=response_times[int(n * 0.99)] if n > 0 else 0,
                requests_per_second=successful / total_duration if total_duration > 0 else 0,
                total_duration_sec=total_duration,
                errors=list(set(errors))[:5]  # Unique errors, max 5
            )
        else:
            result = BenchmarkResult(
                endpoint=endpoint,
                method=method,
                total_requests=iterations,
                successful_requests=0,
                failed_requests=iterations,
                min_time_ms=0,
                max_time_ms=0,
                mean_time_ms=0,
                median_time_ms=0,
                p95_time_ms=0,
                p99_time_ms=0,
                requests_per_second=0,
                total_duration_sec=total_duration,
                errors=errors[:5]
            )

        return result

    def benchmark_all_endpoints(self, iterations: int = 100) -> List[BenchmarkResult]:
        """
        Benchmark all API endpoints

        Args:
            iterations: Number of iterations per endpoint

        Returns:
            List of benchmark results
        """
        # Test data
        base_payload = {
            "region_filter": "강남구",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }

        # All endpoints with their payloads
        endpoints = [
            # Analysis endpoints
            ("/api/v1/analysis/basic-stats", "POST", base_payload),
            ("/api/v1/analysis/price-trend", "POST", {**base_payload, "group_by": "month"}),
            ("/api/v1/analysis/regional", "POST", {
                "regions": ["강남구", "서초구"],
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "top_n": 10
            }),

            # Segmentation endpoints
            ("/api/v1/segmentation/by-area", "POST", {**base_payload, "bins": [50, 60, 85, 100, 135]}),
            ("/api/v1/segmentation/by-floor", "POST", base_payload),
            ("/api/v1/segmentation/by-build-year", "POST", base_payload),
            ("/api/v1/segmentation/by-apartment", "POST", {**base_payload, "min_count": 5}),
            ("/api/v1/segmentation/apartment-detail", "POST", {
                **base_payload,
                "apt_name": "래미안"
            }),

            # Premium endpoints
            ("/api/v1/premium/price-per-area", "POST", base_payload),
            ("/api/v1/premium/price-per-area-trend", "POST", base_payload),
            ("/api/v1/premium/floor-premium", "POST", base_payload),
            ("/api/v1/premium/building-age-premium", "POST", base_payload),

            # Investment endpoints
            ("/api/v1/investment/jeonse-ratio", "POST", base_payload),
            ("/api/v1/investment/gap-investment", "POST", {**base_payload, "min_gap_ratio": 0.7}),
            ("/api/v1/investment/bargain-sales", "POST", {**base_payload, "threshold_pct": 10.0}),

            # Market endpoints
            ("/api/v1/market/rent-vs-jeonse", "POST", base_payload),
            ("/api/v1/market/dealing-type", "POST", base_payload),
            ("/api/v1/market/buyer-seller-type", "POST", base_payload),
            ("/api/v1/market/cancelled-deals", "POST", base_payload),
            ("/api/v1/market/period-summary", "POST", base_payload),
            ("/api/v1/market/baseline-summary", "POST", base_payload),
            ("/api/v1/market/compare-periods", "POST", {
                "current_start_date": "2023-07-01",
                "current_end_date": "2023-12-31",
                "previous_start_date": "2023-01-01",
                "previous_end_date": "2023-06-30",
                "region_filter": "강남구",
                "current_label": "H2 2023",
                "previous_label": "H1 2023"
            }),
            ("/api/v1/market/signals", "POST", base_payload),

            # Health endpoint
            ("/health", "GET", None),
        ]

        results = []

        print("\n" + "="*80)
        print("BENCHMARKING ALL ENDPOINTS")
        print("="*80)

        for i, (endpoint, method, payload) in enumerate(endpoints, 1):
            print(f"\n[{i}/{len(endpoints)}] {method} {endpoint}")
            result = self.benchmark_endpoint(endpoint, method, payload, iterations)
            results.append(result)

        return results

    def generate_report(
        self,
        results: List[BenchmarkResult],
        output_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate benchmark report

        Args:
            results: List of benchmark results
            output_file: Optional output file path

        Returns:
            Report dictionary
        """
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "base_url": self.base_url,
            "total_endpoints": len(results),
            "summary": {
                "total_requests": sum(r.total_requests for r in results),
                "successful_requests": sum(r.successful_requests for r in results),
                "failed_requests": sum(r.failed_requests for r in results),
                "avg_response_time_ms": statistics.mean([r.mean_time_ms for r in results if r.mean_time_ms > 0]),
                "avg_p95_ms": statistics.mean([r.p95_time_ms for r in results if r.p95_time_ms > 0]),
                "avg_p99_ms": statistics.mean([r.p99_time_ms for r in results if r.p99_time_ms > 0]),
            },
            "endpoints": [asdict(r) for r in results]
        }

        # Find slowest endpoints
        sorted_by_p95 = sorted(results, key=lambda x: x.p95_time_ms, reverse=True)
        report["slowest_endpoints"] = [
            {
                "endpoint": r.endpoint,
                "p95_ms": r.p95_ms,
                "mean_ms": r.mean_time_ms
            }
            for r in sorted_by_p95[:10]
        ]

        # Find fastest endpoints
        sorted_by_p95_asc = sorted(
            [r for r in results if r.p95_time_ms > 0],
            key=lambda x: x.p95_time_ms
        )
        report["fastest_endpoints"] = [
            {
                "endpoint": r.endpoint,
                "p95_ms": r.p95_ms,
                "mean_ms": r.mean_time_ms
            }
            for r in sorted_by_p95_asc[:10]
        ]

        # Failed endpoints
        failed = [r for r in results if r.failed_requests > 0]
        if failed:
            report["failed_endpoints"] = [
                {
                    "endpoint": r.endpoint,
                    "failed_count": r.failed_requests,
                    "errors": r.errors
                }
                for r in failed
            ]

        # Save to file
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n\nReport saved to: {output_file}")

        return report

    def print_report(self, results: List[BenchmarkResult]) -> None:
        """
        Print benchmark report to console

        Args:
            results: List of benchmark results
        """
        print("\n" + "="*80)
        print("BENCHMARK REPORT")
        print("="*80)

        # Summary
        total_requests = sum(r.total_requests for r in results)
        successful = sum(r.successful_requests for r in results)
        failed = sum(r.failed_requests for r in results)

        print(f"\nTotal Endpoints: {len(results)}")
        print(f"Total Requests: {total_requests}")
        print(f"Successful: {successful} ({successful/total_requests*100:.1f}%)")
        print(f"Failed: {failed} ({failed/total_requests*100:.1f}%)" if failed > 0 else "Failed: 0")

        # Performance summary
        valid_results = [r for r in results if r.mean_time_ms > 0]
        if valid_results:
            print(f"\nAverage Response Time: {statistics.mean([r.mean_time_ms for r in valid_results]):.2f}ms")
            print(f"Average p95: {statistics.mean([r.p95_time_ms for r in valid_results]):.2f}ms")
            print(f"Average p99: {statistics.mean([r.p99_time_ms for r in valid_results]):.2f}ms")

        # Slowest endpoints
        print("\n" + "-"*80)
        print("TOP 10 SLOWEST ENDPOINTS (by p95)")
        print("-"*80)

        sorted_by_p95 = sorted(results, key=lambda x: x.p95_time_ms, reverse=True)[:10]
        for i, result in enumerate(sorted_by_p95, 1):
            print(f"\n{i}. {result.endpoint}")
            print(f"   Mean: {result.mean_time_ms:.2f}ms | Median: {result.median_time_ms:.2f}ms")
            print(f"   p95: {result.p95_time_ms:.2f}ms | p99: {result.p99_time_ms:.2f}ms")
            print(f"   Min: {result.min_time_ms:.2f}ms | Max: {result.max_time_ms:.2f}ms")
            print(f"   Success: {result.successful_requests}/{result.total_requests}")

        # Failed endpoints
        failed_endpoints = [r for r in results if r.failed_requests > 0]
        if failed_endpoints:
            print("\n" + "-"*80)
            print("FAILED ENDPOINTS")
            print("-"*80)
            for result in failed_endpoints:
                print(f"\n{result.endpoint}")
                print(f"   Failed: {result.failed_requests}/{result.total_requests}")
                if result.errors:
                    print(f"   Errors: {result.errors[0]}")


def main():
    """Main benchmark runner"""
    parser = argparse.ArgumentParser(description="Benchmark API endpoints")
    parser.add_argument(
        "--host",
        default="http://localhost:8000",
        help="API base URL (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=100,
        help="Number of iterations per endpoint (default: 100)"
    )
    parser.add_argument(
        "--output",
        help="Output file path for JSON report"
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=5,
        help="Number of warmup requests (default: 5)"
    )

    args = parser.parse_args()

    # Check if API is accessible
    try:
        response = requests.get(f"{args.host}/health", timeout=5)
        if response.status_code != 200:
            print(f"ERROR: API health check failed (status {response.status_code})")
            print("Make sure the API is running and accessible")
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: Cannot connect to API at {args.host}")
        print(f"Error: {e}")
        print("\nMake sure the API is running:")
        print("  cd fastapi-backend && uvicorn main:app --reload")
        sys.exit(1)

    print(f"\nBenchmarking API at: {args.host}")
    print(f"Iterations per endpoint: {args.iterations}")
    print(f"Warmup requests: {args.warmup}")

    benchmark = APIBenchmark(args.host)
    results = benchmark.benchmark_all_endpoints(iterations=args.iterations)

    # Print console report
    benchmark.print_report(results)

    # Generate and save JSON report
    output_file = args.output or f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report = benchmark.generate_report(results, output_file)

    print("\n" + "="*80)
    print("Benchmark complete!")
    print("="*80)


if __name__ == "__main__":
    main()
