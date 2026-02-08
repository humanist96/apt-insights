# Performance Testing & Optimization Scripts

Collection of scripts for performance testing, benchmarking, and optimization.

## Scripts Overview

| Script | Purpose | Usage |
|--------|---------|-------|
| `benchmark.py` | Comprehensive API benchmarking | `python benchmark.py` |
| `performance_check.py` | Quick performance validation | `python performance_check.py` |
| `optimize_all.sh` | Run all optimization tasks | `./optimize_all.sh` |

---

## benchmark.py

Comprehensive benchmarking of all 24 API endpoints with detailed statistics.

### Usage

```bash
# Basic benchmark (100 iterations per endpoint)
python scripts/benchmark.py

# Custom configuration
python scripts/benchmark.py \
  --host http://localhost:8000 \
  --iterations 200 \
  --output benchmark_report.json \
  --warmup 10

# Quick benchmark (fewer iterations)
python scripts/benchmark.py --iterations 50
```

### Parameters

- `--host`: API base URL (default: http://localhost:8000)
- `--iterations`: Number of requests per endpoint (default: 100)
- `--output`: Output JSON file path (default: benchmark_report_TIMESTAMP.json)
- `--warmup`: Number of warmup requests (default: 5)

### Output

**Console Report**:
```
BENCHMARK REPORT
================================================================================

Total Endpoints: 24
Total Requests: 2400
Successful: 2398 (99.9%)
Failed: 2 (0.1%)

Average Response Time: 45.23ms
Average p95: 127.56ms
Average p99: 234.12ms

TOP 10 SLOWEST ENDPOINTS (by p95)
--------------------------------------------------------------------------------

1. /api/v1/market/compare-periods
   Mean: 156.34ms | Median: 142.21ms
   p95: 298.45ms | p99: 412.67ms
   ...
```

**JSON Report**:
```json
{
  "timestamp": "2026-02-08T10:30:00",
  "base_url": "http://localhost:8000",
  "total_endpoints": 24,
  "summary": {
    "total_requests": 2400,
    "successful_requests": 2398,
    "failed_requests": 2,
    "avg_response_time_ms": 45.23,
    "avg_p95_ms": 127.56,
    "avg_p99_ms": 234.12
  },
  "slowest_endpoints": [...],
  "fastest_endpoints": [...],
  "endpoints": [...]
}
```

### Use Cases

1. **Performance regression testing**: Compare before/after optimization
2. **Capacity planning**: Determine system limits
3. **SLA validation**: Verify response time targets
4. **Bottleneck identification**: Find slow endpoints

---

## performance_check.py

Quick performance validation against defined targets.

### Usage

```bash
# Run performance check
python scripts/performance_check.py
```

### Performance Targets

| Metric | Target |
|--------|--------|
| p50 | < 50ms |
| p95 | < 200ms |
| p99 | < 500ms |
| Error Rate | < 1% |
| Success Rate | > 99% |

### Output

```
PERFORMANCE CHECK REPORT
============================================================

Total Requests: 50
Successful: 50
Failed: 0
Success Rate: 100.0%
Error Rate: 0.0%

------------------------------------------------------------
RESPONSE TIMES
------------------------------------------------------------
Min:    23.45ms
Mean:   42.18ms
Median: 39.67ms
p50:    39.67ms
p95:    127.34ms
p99:    189.23ms
Max:    234.56ms

------------------------------------------------------------
TARGET VALIDATION
------------------------------------------------------------
✓ PASS | p50_ms: 39.67ms (target: < 50ms)
✓ PASS | p95_ms: 127.34ms (target: < 200ms)
✓ PASS | p99_ms: 189.23ms (target: < 500ms)
✓ PASS | error_rate: 0.00% (target: < 1.0%)
✓ PASS | success_rate: 100.00% (target: > 99.0%)

============================================================
✓ ALL CHECKS PASSED
============================================================
```

### Exit Codes

- `0`: All checks passed
- `1`: Some checks failed or API unavailable

### Use Cases

1. **Pre-deployment checks**: Validate before release
2. **CI/CD integration**: Automated performance gates
3. **Health monitoring**: Quick system validation
4. **Smoke testing**: Verify after deployment

---

## optimize_all.sh

Comprehensive optimization script that runs all optimization tasks.

### Usage

```bash
# Run all optimizations
./scripts/optimize_all.sh
```

### Tasks Performed

1. **Database Optimization**
   - Analyze slow queries
   - Apply recommended indexes
   - Update table statistics

2. **Redis Cache Warming**
   - Pre-populate cache with popular queries
   - Verify cache health

3. **Performance Benchmark**
   - Run full benchmark suite
   - Generate detailed report

4. **Performance Validation**
   - Verify all targets met
   - Provide actionable recommendations

### Prerequisites

- API server running at http://localhost:8000
- `DATABASE_URL` environment variable set
- `REDIS_URL` environment variable set
- Virtual environment activated (recommended)

### Output

```
=========================================
APARTMENT ANALYSIS API - OPTIMIZATION
=========================================

Project root: /Users/koscom/Downloads/apt_test

=========================================
1. DATABASE OPTIMIZATION
=========================================
Analyzing slow queries...
Applying recommended indexes...
✓ Database optimization complete

=========================================
2. REDIS CACHE WARMING
=========================================
Warming cache with popular queries...
✓ Cache warming complete

=========================================
3. PERFORMANCE BENCHMARK
=========================================
Running performance benchmark...
✓ Benchmark complete

=========================================
4. PERFORMANCE VALIDATION
=========================================
Validating performance targets...
✓ All performance targets met

=========================================
OPTIMIZATION COMPLETE
=========================================

Next steps:
  1. Review benchmark report (benchmark_*.json)
  2. Run load test: cd tests/load && locust -f locustfile.py
  3. Monitor cache hit rate in production
  4. Schedule regular optimization (cron job)
```

### Scheduling

Add to crontab for regular optimization:

```bash
# Run every Sunday at 2 AM
0 2 * * 0 /path/to/apt_test/scripts/optimize_all.sh >> /var/log/optimization.log 2>&1
```

---

## Workflow Examples

### Before Deployment

```bash
# 1. Run performance check
python scripts/performance_check.py

# 2. If passed, run full benchmark
python scripts/benchmark.py --output pre_deploy.json

# 3. Compare with baseline
python -c "
import json
with open('baseline.json') as f:
    baseline = json.load(f)
with open('pre_deploy.json') as f:
    current = json.load(f)

p95_baseline = baseline['summary']['avg_p95_ms']
p95_current = current['summary']['avg_p95_ms']
change = ((p95_current - p95_baseline) / p95_baseline) * 100

print(f'p95 change: {change:+.1f}%')
assert change < 10, 'Performance regression detected'
"
```

### After Optimization

```bash
# 1. Run comprehensive optimization
./scripts/optimize_all.sh

# 2. Run load test
cd tests/load
locust -f locustfile.py --host=http://localhost:8000 \
  --headless --users 100 --spawn-rate 10 --run-time 5m \
  --csv results/after_optimization

# 3. Compare results
python -c "
import csv
with open('results/before_optimization_stats.csv') as f:
    before = list(csv.DictReader(f))[-1]
with open('results/after_optimization_stats.csv') as f:
    after = list(csv.DictReader(f))[-1]

print(f'Before: {before[\"Average Response Time\"]}ms')
print(f'After: {after[\"Average Response Time\"]}ms')
print(f'Improvement: {((float(before[\"Average Response Time\"]) - float(after[\"Average Response Time\"])) / float(before[\"Average Response Time\"]) * 100):.1f}%')
"
```

### CI/CD Integration

```yaml
# .github/workflows/performance.yml
- name: Performance check
  run: python scripts/performance_check.py

- name: Benchmark
  run: |
    python scripts/benchmark.py \
      --iterations 50 \
      --output benchmark.json

- name: Validate
  run: |
    python -c "
    import json
    with open('benchmark.json') as f:
        data = json.load(f)
    assert data['summary']['avg_p95_ms'] < 200
    "
```

---

## Troubleshooting

### API Not Running

**Error**: `ERROR: API is not healthy or not accessible`

**Solution**:
```bash
cd fastapi-backend
uvicorn main:app --reload --port 8000
```

### Database Connection Failed

**Error**: `ERROR: DATABASE_URL not set`

**Solution**:
```bash
export DATABASE_URL="postgresql://user:pass@localhost:5432/apt_test"
```

### Redis Connection Failed

**Error**: `WARNING: REDIS_URL not set`

**Solution**:
```bash
export REDIS_URL="redis://localhost:6379/0"

# Or start Redis
redis-server
```

### High Error Rate

**Symptoms**: Error rate > 1%, failed requests

**Solutions**:
1. Check API logs for errors
2. Verify database connection pool
3. Check Redis connectivity
4. Review rate limiting settings

### Slow Benchmarks

**Symptoms**: Benchmarks taking > 10 minutes

**Solutions**:
1. Reduce iterations: `--iterations 50`
2. Check system resources (CPU, memory)
3. Optimize database queries first
4. Warm cache before benchmarking

---

## Best Practices

1. **Always warm up**: First few requests are slower (cache, JIT)
2. **Use realistic data**: Production-like dataset sizes
3. **Run multiple times**: Average results across runs
4. **Monitor system resources**: CPU, memory, disk during tests
5. **Baseline comparisons**: Keep historical benchmark data
6. **Isolate testing**: Dedicated test environment
7. **Document changes**: Record optimization changes made

---

## Performance Budget

Set performance budgets for your API:

```python
# performance_budget.py
PERFORMANCE_BUDGET = {
    "p50_ms": 50,
    "p95_ms": 200,
    "p99_ms": 500,
    "error_rate": 0.01,
    "throughput_rps": 100,
}

def check_budget(metrics):
    violations = []
    for key, target in PERFORMANCE_BUDGET.items():
        if metrics[key] > target:
            violations.append(f"{key}: {metrics[key]} exceeds {target}")
    return violations
```

---

## Resources

- **Performance Optimization Guide**: ../PERFORMANCE_OPTIMIZATION.md
- **Load Testing Guide**: ../tests/load/README.md
- **API Documentation**: ../fastapi-backend/API_ENDPOINTS.md

---

**Last Updated**: 2026-02-08
