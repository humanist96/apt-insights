# Performance Testing - Quick Start Guide

Get started with performance testing and optimization in 5 minutes.

## Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Start services
cd fastapi-backend
uvicorn main:app --reload --port 8000

# In separate terminal, start Redis (if not running)
redis-server

# In separate terminal, ensure PostgreSQL is running
```

## Step 1: Quick Performance Check (2 minutes)

```bash
# Validate API meets performance targets
python scripts/performance_check.py
```

**Expected output**: ✓ ALL CHECKS PASSED

**If failed**: Review PERFORMANCE_OPTIMIZATION.md for troubleshooting

## Step 2: Run Benchmark (5 minutes)

```bash
# Benchmark all endpoints
python scripts/benchmark.py --iterations 50
```

**Expected output**:
- p95 < 200ms
- p99 < 500ms
- Success rate > 99%

## Step 3: Load Test (10 minutes)

```bash
# Install Locust
pip install locust

# Run load test
cd tests/load
locust -f locustfile.py --host=http://localhost:8000

# Open browser
open http://localhost:8089

# Configure test:
# - Number of users: 50
# - Spawn rate: 10
# - Run time: 5m
```

## Step 4: Optimize (5 minutes)

```bash
# Run comprehensive optimization
./scripts/optimize_all.sh
```

**This will**:
- Analyze and fix slow queries
- Add missing database indexes
- Warm Redis cache
- Validate performance improvements

## Step 5: Verify Improvements

```bash
# Re-run performance check
python scripts/performance_check.py

# Compare before/after
# Should see improved p95/p99 times
```

---

## Common Commands

```bash
# Quick health check
curl http://localhost:8000/health

# Run specific endpoint benchmark
python -c "
import requests
import time
times = []
for _ in range(100):
    start = time.time()
    requests.post('http://localhost:8000/api/v1/analysis/basic-stats',
                  json={'region_filter': '강남구'})
    times.append((time.time() - start) * 1000)
print(f'p95: {sorted(times)[95]:.2f}ms')
"

# Check cache stats
python -c "
from fastapi_backend.cache.cache_warming import CacheWarmer
warmer = CacheWarmer('redis://localhost:6379/0')
stats = warmer.get_cache_stats()
print(f'Hit rate: {stats[\"hit_rate\"]:.1f}%')
"

# Check slow queries
python fastapi-backend/db/query_optimizer.py
```

---

## Performance Targets

| Metric | Target | How to Check |
|--------|--------|-------------|
| p50 | < 50ms | `performance_check.py` |
| p95 | < 200ms | `benchmark.py` |
| p99 | < 500ms | `benchmark.py` |
| Error Rate | < 1% | Load test |
| Cache Hit Rate | > 80% | Cache stats |

---

## Troubleshooting

### API Too Slow

```bash
# 1. Check database indexes
python fastapi-backend/db/query_optimizer.py

# 2. Warm cache
python fastapi-backend/cache/cache_warming.py

# 3. Check slow queries
# Review optimization_report_*.json
```

### High Error Rate

```bash
# 1. Check API logs
tail -f fastapi-backend/logs/app.log

# 2. Test endpoint manually
curl -X POST http://localhost:8000/api/v1/analysis/basic-stats \
  -H "Content-Type: application/json" \
  -d '{"region_filter": "강남구"}'

# 3. Check database connection
psql $DATABASE_URL -c "SELECT 1"
```

### Load Test Failures

```bash
# 1. Reduce concurrent users
# Start with 10 users, increase gradually

# 2. Check system resources
top  # or htop

# 3. Check database connections
# Increase pool size in settings
```

---

## Next Steps

1. **Read full guide**: PERFORMANCE_OPTIMIZATION.md
2. **Setup monitoring**: Configure Prometheus/Grafana
3. **Schedule optimization**: Add to cron for weekly runs
4. **CI/CD integration**: Add performance gates to pipeline

---

## Getting Help

- **Performance issues**: Review PERFORMANCE_OPTIMIZATION.md
- **Load testing**: Read tests/load/README.md
- **Scripts**: See scripts/README.md
- **API docs**: fastapi-backend/API_ENDPOINTS.md

---

**Estimated time to complete**: 30 minutes
**Difficulty**: Beginner
**Last updated**: 2026-02-08
