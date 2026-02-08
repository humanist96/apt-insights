#!/bin/bash

# Comprehensive Optimization Script
# Runs all optimization tasks in sequence

set -e

echo "========================================="
echo "APARTMENT ANALYSIS API - OPTIMIZATION"
echo "========================================="

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "WARNING: No virtual environment detected"
    echo "Recommend activating venv first: source venv/bin/activate"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo ""
echo "Project root: $PROJECT_ROOT"
echo ""

# 1. Database Optimization
echo "========================================="
echo "1. DATABASE OPTIMIZATION"
echo "========================================="

if [[ -z "$DATABASE_URL" ]]; then
    echo "WARNING: DATABASE_URL not set"
    echo "Skipping database optimization"
else
    echo "Analyzing slow queries..."
    cd "$PROJECT_ROOT/fastapi-backend"
    python db/query_optimizer.py

    echo ""
    echo "Applying recommended indexes..."
    python -c "from db.query_optimizer import apply_recommended_indexes; import os; apply_recommended_indexes(os.getenv('DATABASE_URL'))"

    echo ""
    echo "✓ Database optimization complete"
fi

# 2. Redis Cache Warming
echo ""
echo "========================================="
echo "2. REDIS CACHE WARMING"
echo "========================================="

if [[ -z "$REDIS_URL" ]]; then
    echo "WARNING: REDIS_URL not set"
    echo "Skipping cache warming"
else
    echo "Warming cache with popular queries..."
    cd "$PROJECT_ROOT/fastapi-backend"
    python cache/cache_warming.py

    echo ""
    echo "✓ Cache warming complete"
fi

# 3. Performance Benchmark
echo ""
echo "========================================="
echo "3. PERFORMANCE BENCHMARK"
echo "========================================="

echo "Checking API health..."
curl -s http://localhost:8000/health > /dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "ERROR: API is not running"
    echo "Start the API first: cd fastapi-backend && uvicorn main:app --reload"
    exit 1
fi

echo "✓ API is healthy"
echo ""

echo "Running performance benchmark..."
cd "$PROJECT_ROOT"
python scripts/benchmark.py --iterations 100 --output "benchmark_$(date +%Y%m%d_%H%M%S).json"

echo ""
echo "✓ Benchmark complete"

# 4. Performance Check
echo ""
echo "========================================="
echo "4. PERFORMANCE VALIDATION"
echo "========================================="

echo "Validating performance targets..."
python "$PROJECT_ROOT/scripts/performance_check.py"

if [[ $? -eq 0 ]]; then
    echo ""
    echo "✓ All performance targets met"
else
    echo ""
    echo "✗ Some performance targets not met"
    echo "Review optimization report above"
fi

# Summary
echo ""
echo "========================================="
echo "OPTIMIZATION COMPLETE"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Review benchmark report (benchmark_*.json)"
echo "  2. Run load test: cd tests/load && locust -f locustfile.py"
echo "  3. Monitor cache hit rate in production"
echo "  4. Schedule regular optimization (cron job)"
echo ""
echo "For more information, see PERFORMANCE_OPTIMIZATION.md"
echo ""
