"""
Simple test script for FastAPI endpoints
Run after starting the server with: python main.py
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def print_response(name: str, response: requests.Response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"Test: {name}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print_response("Root Endpoint", response)
    assert response.status_code == 200


def test_basic_stats_all():
    """Test basic stats with no filters"""
    response = requests.post(
        f"{BASE_URL}/api/v1/analysis/basic-stats",
        json={}
    )
    print_response("Basic Stats (All Data)", response)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "data" in response.json()
    assert "meta" in response.json()


def test_basic_stats_filtered():
    """Test basic stats with region filter"""
    response = requests.post(
        f"{BASE_URL}/api/v1/analysis/basic-stats",
        json={
            "region_filter": "강남구"
        }
    )
    print_response("Basic Stats (Filtered by Region)", response)
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_price_trend():
    """Test price trend endpoint"""
    response = requests.post(
        f"{BASE_URL}/api/v1/analysis/price-trend",
        json={
            "region_filter": "강남구",
            "group_by": "month"
        }
    )
    print_response("Price Trend", response)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "trend_data" in response.json()["data"]


def test_regional_analysis():
    """Test regional analysis endpoint"""
    response = requests.post(
        f"{BASE_URL}/api/v1/analysis/regional",
        json={
            "top_n": 5
        }
    )
    print_response("Regional Analysis (Top 5)", response)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "regions" in response.json()["data"]
    assert len(response.json()["data"]["regions"]) <= 5


def test_validation_error():
    """Test request validation"""
    response = requests.post(
        f"{BASE_URL}/api/v1/analysis/basic-stats",
        json={
            "start_date": "invalid-date"
        }
    )
    print_response("Validation Error Test", response)
    assert response.status_code == 422  # Unprocessable Entity


def test_cache_clear():
    """Test cache clearing"""
    response = requests.post(f"{BASE_URL}/api/v1/analysis/cache/clear")
    print_response("Cache Clear", response)
    assert response.status_code == 200
    assert response.json()["success"] is True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("FastAPI Backend Test Suite")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")

    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root),
        ("Basic Stats (All)", test_basic_stats_all),
        ("Basic Stats (Filtered)", test_basic_stats_filtered),
        ("Price Trend", test_price_trend),
        ("Regional Analysis", test_regional_analysis),
        ("Validation Error", test_validation_error),
        ("Cache Clear", test_cache_clear),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
            print(f"\n✅ {name} - PASSED")
        except AssertionError as e:
            failed += 1
            print(f"\n❌ {name} - FAILED")
            print(f"   Error: {e}")
        except requests.exceptions.ConnectionError:
            print(f"\n❌ {name} - FAILED")
            print(f"   Error: Could not connect to {BASE_URL}")
            print(f"   Make sure the server is running: python main.py")
            failed += 1
            break
        except Exception as e:
            failed += 1
            print(f"\n❌ {name} - FAILED")
            print(f"   Error: {e}")

    print(f"\n{'='*60}")
    print(f"Test Results: {passed} passed, {failed} failed")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    run_all_tests()
