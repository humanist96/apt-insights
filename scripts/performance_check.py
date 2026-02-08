"""
Quick Performance Check Script

Validates that API meets performance targets.

Usage:
    python scripts/performance_check.py
"""

import requests
import time
import sys
from typing import Dict, Any, List
import statistics


class PerformanceChecker:
    """Quick performance validation"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.targets = {
            "p50_ms": 50,
            "p95_ms": 200,
            "p99_ms": 500,
            "error_rate": 0.01,  # 1%
            "success_rate": 0.99  # 99%
        }

    def check_health(self) -> bool:
        """Check API health"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def quick_benchmark(self, iterations: int = 50) -> Dict[str, Any]:
        """
        Run quick performance benchmark

        Args:
            iterations: Number of test iterations

        Returns:
            Performance metrics
        """
        endpoint = "/api/v1/analysis/basic-stats"
        payload = {
            "region_filter": "강남구",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }

        response_times = []
        errors = 0

        print(f"Running {iterations} requests to {endpoint}...")

        for i in range(iterations):
            start = time.time()
            try:
                response = requests.post(
                    f"{self.base_url}{endpoint}",
                    json=payload,
                    timeout=30
                )
                end = time.time()

                if response.status_code == 200:
                    response_times.append((end - start) * 1000)
                else:
                    errors += 1
            except Exception:
                errors += 1

            if (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{iterations}")

        if not response_times:
            return {
                "success": False,
                "error": "No successful requests"
            }

        response_times.sort()
        n = len(response_times)

        metrics = {
            "success": True,
            "total_requests": iterations,
            "successful_requests": len(response_times),
            "failed_requests": errors,
            "error_rate": errors / iterations,
            "success_rate": len(response_times) / iterations,
            "p50_ms": response_times[int(n * 0.50)],
            "p95_ms": response_times[int(n * 0.95)],
            "p99_ms": response_times[int(n * 0.99)] if n > 20 else response_times[-1],
            "min_ms": min(response_times),
            "max_ms": max(response_times),
            "mean_ms": statistics.mean(response_times),
            "median_ms": statistics.median(response_times)
        }

        return metrics

    def check_targets(self, metrics: Dict[str, Any]) -> Dict[str, bool]:
        """
        Check if metrics meet targets

        Args:
            metrics: Performance metrics

        Returns:
            Dict of pass/fail for each target
        """
        results = {}

        for key, target in self.targets.items():
            actual = metrics.get(key, 0)

            if key in ["p50_ms", "p95_ms", "p99_ms"]:
                # Lower is better
                results[key] = actual <= target
            elif key == "error_rate":
                # Lower is better
                results[key] = actual <= target
            elif key == "success_rate":
                # Higher is better
                results[key] = actual >= target

        return results

    def print_report(self, metrics: Dict[str, Any], checks: Dict[str, bool]) -> None:
        """Print performance report"""
        print("\n" + "="*60)
        print("PERFORMANCE CHECK REPORT")
        print("="*60)

        print(f"\nTotal Requests: {metrics['total_requests']}")
        print(f"Successful: {metrics['successful_requests']}")
        print(f"Failed: {metrics['failed_requests']}")
        print(f"Success Rate: {metrics['success_rate']*100:.1f}%")
        print(f"Error Rate: {metrics['error_rate']*100:.1f}%")

        print("\n" + "-"*60)
        print("RESPONSE TIMES")
        print("-"*60)

        print(f"Min:    {metrics['min_ms']:.2f}ms")
        print(f"Mean:   {metrics['mean_ms']:.2f}ms")
        print(f"Median: {metrics['median_ms']:.2f}ms")
        print(f"p50:    {metrics['p50_ms']:.2f}ms")
        print(f"p95:    {metrics['p95_ms']:.2f}ms")
        print(f"p99:    {metrics['p99_ms']:.2f}ms")
        print(f"Max:    {metrics['max_ms']:.2f}ms")

        print("\n" + "-"*60)
        print("TARGET VALIDATION")
        print("-"*60)

        all_passed = True

        for key, passed in checks.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            target = self.targets[key]
            actual = metrics[key]

            if key in ["p50_ms", "p95_ms", "p99_ms"]:
                print(f"{status} | {key}: {actual:.2f}ms (target: < {target}ms)")
            elif key == "error_rate":
                print(f"{status} | {key}: {actual*100:.2f}% (target: < {target*100:.1f}%)")
            elif key == "success_rate":
                print(f"{status} | {key}: {actual*100:.2f}% (target: > {target*100:.1f}%)")

            if not passed:
                all_passed = False

        print("\n" + "="*60)
        if all_passed:
            print("✓ ALL CHECKS PASSED")
        else:
            print("✗ SOME CHECKS FAILED")
        print("="*60)

        return all_passed


def main():
    """Main performance check"""
    checker = PerformanceChecker()

    print("="*60)
    print("APARTMENT ANALYSIS API - PERFORMANCE CHECK")
    print("="*60)

    # Check health
    print("\nChecking API health...")
    if not checker.check_health():
        print("ERROR: API is not healthy or not accessible")
        print("Make sure the API is running:")
        print("  cd fastapi-backend && uvicorn main:app --reload")
        sys.exit(1)
    print("✓ API is healthy")

    # Run benchmark
    print("\nRunning performance benchmark...")
    metrics = checker.quick_benchmark(iterations=50)

    if not metrics.get("success"):
        print(f"ERROR: {metrics.get('error')}")
        sys.exit(1)

    # Check targets
    checks = checker.check_targets(metrics)

    # Print report
    all_passed = checker.print_report(metrics, checks)

    # Exit code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
