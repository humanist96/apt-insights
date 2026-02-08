"""
Locust Load Testing Suite for Apartment Analysis Platform

Tests API endpoints under various load scenarios:
- Free tier users (10 API calls/day)
- Premium users (unlimited)
- Mixed user scenarios
- Realistic user journeys

Run:
    locust -f tests/load/locustfile.py --host=http://localhost:8000

Web UI: http://localhost:8089
"""

import random
import json
from datetime import datetime, timedelta
from locust import HttpUser, task, between, TaskSet, events
from locust.runners import MasterRunner


class AnalysisTaskSet(TaskSet):
    """Basic analysis tasks (most common user flow)"""

    def on_start(self):
        """Initialize test data"""
        self.regions = ["강남구", "서초구", "송파구", "강동구"]
        self.start_date = "2023-01-01"
        self.end_date = "2023-12-31"

    @task(5)
    def basic_stats(self):
        """Most common endpoint - basic statistics"""
        payload = {
            "region_filter": random.choice(self.regions),
            "start_date": self.start_date,
            "end_date": self.end_date
        }
        with self.client.post(
            "/api/v1/analysis/basic-stats",
            json=payload,
            name="/api/v1/analysis/basic-stats",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    response.success()
                else:
                    response.failure(f"API returned success=false: {data.get('error')}")
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(3)
    def price_trend(self):
        """Price trend analysis"""
        payload = {
            "region_filter": random.choice(self.regions),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "group_by": "month"
        }
        self.client.post("/api/v1/analysis/price-trend", json=payload, name="/api/v1/analysis/price-trend")

    @task(2)
    def regional_analysis(self):
        """Regional comparison"""
        payload = {
            "regions": random.sample(self.regions, 2),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "top_n": 10
        }
        self.client.post("/api/v1/analysis/regional", json=payload, name="/api/v1/analysis/regional")


class SegmentationTaskSet(TaskSet):
    """Segmentation analysis tasks"""

    def on_start(self):
        self.regions = ["강남구", "서초구", "송파구"]
        self.start_date = "2023-01-01"
        self.end_date = "2023-12-31"

    @task(3)
    def by_area(self):
        """Analyze by area"""
        payload = {
            "region_filter": random.choice(self.regions),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "bins": [50, 60, 85, 100, 135]
        }
        self.client.post("/api/v1/segmentation/by-area", json=payload, name="/api/v1/segmentation/by-area")

    @task(2)
    def by_floor(self):
        """Analyze by floor"""
        payload = {
            "region_filter": random.choice(self.regions),
            "start_date": self.start_date,
            "end_date": self.end_date
        }
        self.client.post("/api/v1/segmentation/by-floor", json=payload, name="/api/v1/segmentation/by-floor")

    @task(2)
    def by_apartment(self):
        """Analyze by apartment"""
        payload = {
            "region_filter": random.choice(self.regions),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "min_count": 5
        }
        self.client.post("/api/v1/segmentation/by-apartment", json=payload, name="/api/v1/segmentation/by-apartment")


class InvestmentTaskSet(TaskSet):
    """Investment analysis tasks (premium features)"""

    def on_start(self):
        self.regions = ["강남구", "서초구", "송파구"]
        self.start_date = "2023-01-01"
        self.end_date = "2023-12-31"

    @task(3)
    def jeonse_ratio(self):
        """Calculate jeonse ratio"""
        payload = {
            "region_filter": random.choice(self.regions),
            "start_date": self.start_date,
            "end_date": self.end_date
        }
        self.client.post("/api/v1/investment/jeonse-ratio", json=payload, name="/api/v1/investment/jeonse-ratio")

    @task(2)
    def gap_investment(self):
        """Gap investment analysis"""
        payload = {
            "region_filter": random.choice(self.regions),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "min_gap_ratio": 0.7
        }
        self.client.post("/api/v1/investment/gap-investment", json=payload, name="/api/v1/investment/gap-investment")

    @task(1)
    def bargain_sales(self):
        """Detect bargain sales"""
        payload = {
            "region_filter": random.choice(self.regions),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "threshold_pct": 10.0
        }
        self.client.post("/api/v1/investment/bargain-sales", json=payload, name="/api/v1/investment/bargain-sales")


class MarketTaskSet(TaskSet):
    """Market analysis tasks"""

    def on_start(self):
        self.regions = ["강남구", "서초구", "송파구"]
        self.start_date = "2023-01-01"
        self.end_date = "2023-12-31"

    @task(2)
    def market_signals(self):
        """Detect market signals"""
        payload = {
            "region_filter": random.choice(self.regions),
            "start_date": self.start_date,
            "end_date": self.end_date
        }
        self.client.post("/api/v1/market/signals", json=payload, name="/api/v1/market/signals")

    @task(1)
    def compare_periods(self):
        """Compare time periods"""
        payload = {
            "current_start_date": "2023-07-01",
            "current_end_date": "2023-12-31",
            "previous_start_date": "2023-01-01",
            "previous_end_date": "2023-06-30",
            "region_filter": random.choice(self.regions),
            "current_label": "H2 2023",
            "previous_label": "H1 2023"
        }
        self.client.post("/api/v1/market/compare-periods", json=payload, name="/api/v1/market/compare-periods")


class FreeUserJourney(TaskSet):
    """
    Free tier user journey (10 API calls/day limit)
    - Basic stats lookup
    - Price trend check
    - Regional comparison
    """

    wait_time = between(5, 15)

    def on_start(self):
        self.call_count = 0
        self.daily_limit = 10

    @task
    def user_journey(self):
        """Simulate realistic free user journey"""
        if self.call_count >= self.daily_limit:
            self.interrupt()
            return

        # Step 1: Check basic stats for interested region
        region = random.choice(["강남구", "서초구", "송파구"])
        payload = {
            "region_filter": region,
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }
        self.client.post("/api/v1/analysis/basic-stats", json=payload, name="Free: Basic Stats")
        self.call_count += 1

        if self.call_count >= self.daily_limit:
            return

        # Step 2: Check price trend
        self.client.post("/api/v1/analysis/price-trend", json=payload, name="Free: Price Trend")
        self.call_count += 1

        if self.call_count >= self.daily_limit:
            return

        # Step 3: Compare with another region
        payload["regions"] = [region, random.choice(["강남구", "서초구", "송파구"])]
        self.client.post("/api/v1/analysis/regional", json=payload, name="Free: Regional")
        self.call_count += 1


class PremiumUserJourney(TaskSet):
    """
    Premium user journey (unlimited API calls)
    - Deep analysis across multiple endpoints
    - Investment analysis
    - Market signals
    """

    wait_time = between(2, 5)

    tasks = {
        AnalysisTaskSet: 3,
        SegmentationTaskSet: 2,
        InvestmentTaskSet: 3,
        MarketTaskSet: 2
    }


class FreeUser(HttpUser):
    """Free tier user - limited API calls"""
    weight = 7  # 70% of users
    wait_time = between(10, 30)  # Longer wait between sessions
    tasks = [FreeUserJourney]


class PremiumUser(HttpUser):
    """Premium user - unlimited API calls"""
    weight = 3  # 30% of users
    wait_time = between(3, 8)
    tasks = [PremiumUserJourney]


class PowerUser(HttpUser):
    """Power user - intensive analysis"""
    weight = 1  # 10% of users
    wait_time = between(1, 3)

    @task(2)
    def intensive_analysis(self):
        """Rapid-fire analysis across all endpoints"""
        regions = ["강남구", "서초구", "송파구", "강동구"]
        base_payload = {
            "region_filter": random.choice(regions),
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }

        # Hit multiple endpoints
        endpoints = [
            "/api/v1/analysis/basic-stats",
            "/api/v1/analysis/price-trend",
            "/api/v1/segmentation/by-area",
            "/api/v1/investment/jeonse-ratio",
            "/api/v1/market/signals"
        ]

        for endpoint in random.sample(endpoints, 3):
            self.client.post(endpoint, json=base_payload, name=f"Power: {endpoint}")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Initialize test environment"""
    print("Starting load test...")
    print(f"Target host: {environment.host}")

    if isinstance(environment.runner, MasterRunner):
        print("Running in distributed mode")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Generate test report"""
    print("\n" + "="*60)
    print("LOAD TEST SUMMARY")
    print("="*60)

    stats = environment.stats
    print(f"\nTotal requests: {stats.total.num_requests}")
    print(f"Failed requests: {stats.total.num_failures}")
    print(f"Success rate: {((stats.total.num_requests - stats.total.num_failures) / stats.total.num_requests * 100):.2f}%")
    print(f"Average response time: {stats.total.avg_response_time:.2f}ms")
    print(f"Median response time: {stats.total.median_response_time:.2f}ms")
    print(f"95th percentile: {stats.total.get_response_time_percentile(0.95):.2f}ms")
    print(f"99th percentile: {stats.total.get_response_time_percentile(0.99):.2f}ms")
    print(f"Max response time: {stats.total.max_response_time:.2f}ms")
    print(f"Requests/s: {stats.total.total_rps:.2f}")

    print("\n" + "="*60)
    print("TOP 10 SLOWEST ENDPOINTS")
    print("="*60)

    sorted_stats = sorted(
        [(name, stat) for name, stat in stats.entries.items()],
        key=lambda x: x[1].avg_response_time,
        reverse=True
    )[:10]

    for name, stat in sorted_stats:
        print(f"\n{name}")
        print(f"  Requests: {stat.num_requests}")
        print(f"  Avg: {stat.avg_response_time:.2f}ms")
        print(f"  p95: {stat.get_response_time_percentile(0.95):.2f}ms")
        print(f"  Failures: {stat.num_failures}")


# Custom shape for ramped load testing
from locust import LoadTestShape

class RampedLoadTest(LoadTestShape):
    """
    Gradually ramp up users to test system under increasing load

    Stages:
    - 0-2 min: 10 users (warm-up)
    - 2-5 min: 50 users (normal load)
    - 5-8 min: 100 users (peak load)
    - 8-10 min: 200 users (stress test)
    - 10+ min: Hold at 100 users
    """

    stages = [
        {"duration": 120, "users": 10, "spawn_rate": 1},   # Warm-up
        {"duration": 300, "users": 50, "spawn_rate": 5},   # Normal
        {"duration": 480, "users": 100, "spawn_rate": 10}, # Peak
        {"duration": 600, "users": 200, "spawn_rate": 20}, # Stress
        {"duration": 900, "users": 100, "spawn_rate": 10}, # Sustained
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])

        return None  # Test complete
