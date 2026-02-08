# Performance Optimization Guide

Comprehensive guide for performance testing, optimization, and monitoring of the apartment analysis platform.

## Table of Contents

1. [Overview](#overview)
2. [Load Testing](#load-testing)
3. [Database Optimization](#database-optimization)
4. [Redis Cache Optimization](#redis-cache-optimization)
5. [API Response Optimization](#api-response-optimization)
6. [Benchmarking](#benchmarking)
7. [Performance Metrics](#performance-metrics)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The platform is optimized for:
- **Target**: 100 concurrent users
- **Throughput**: 1000 requests/minute
- **Response Time**: p95 < 200ms, p99 < 500ms
- **Availability**: 99.9% uptime

### Architecture Overview

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│  FastAPI     │─────▶│ PostgreSQL  │
│   (HTTP)    │      │  (Backend)   │      │   Database  │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │    Redis     │
                     │    Cache     │
                     └──────────────┘
```

---

## Load Testing

### Locust Load Testing

Simulate realistic user traffic patterns with free/premium tier users.

#### Quick Start

```bash
# Install Locust
pip install locust

# Start API server
cd fastapi-backend
uvicorn main:app --reload --port 8000

# Run load test (in separate terminal)
cd tests/load
locust -f locustfile.py --host=http://localhost:8000

# Access web UI
open http://localhost:8089
```

#### Test Scenarios

**1. Free User Simulation (70% of users)**
- 10 API calls/day limit
- Basic stats, price trends, regional analysis
- Wait time: 10-30 seconds between requests

**2. Premium User Simulation (30% of users)**
- Unlimited API calls
- Deep analysis across all endpoints
- Wait time: 2-5 seconds between requests

**3. Power User Simulation (10% of users)**
- Intensive rapid-fire analysis
- Multiple concurrent endpoints
- Wait time: 1-3 seconds between requests

#### Running Load Tests

```bash
# Ramped load test (gradual increase)
locust -f locustfile.py --host=http://localhost:8000 \
  --users 100 --spawn-rate 10 --run-time 10m

# Stress test (immediate peak load)
locust -f locustfile.py --host=http://localhost:8000 \
  --users 200 --spawn-rate 50 --run-time 5m

# Generate CSV report
locust -f locustfile.py --host=http://localhost:8000 \
  --users 100 --spawn-rate 10 --run-time 10m \
  --csv=results/load_test --html=results/load_test.html
```

#### Load Test Stages

The included `RampedLoadTest` shape provides gradual load increase:

1. **Warm-up** (0-2 min): 10 users
2. **Normal load** (2-5 min): 50 users
3. **Peak load** (5-8 min): 100 users
4. **Stress test** (8-10 min): 200 users
5. **Sustained** (10+ min): Hold at 100 users

#### Key Metrics

Monitor these metrics during load tests:

- **Response Time**: p50, p95, p99
- **Throughput**: Requests per second
- **Error Rate**: Failed requests / Total requests
- **Success Rate**: Should be > 99%

---

## Database Optimization

### Query Optimization

Use the query optimizer to identify and fix slow queries.

#### Running Query Analysis

```bash
cd fastapi-backend

# Analyze slow queries and generate report
python db/query_optimizer.py

# Apply recommended indexes
python -c "from db.query_optimizer import apply_recommended_indexes; \
  import os; apply_recommended_indexes(os.getenv('DATABASE_URL'))"
```

#### Recommended Indexes

The optimizer automatically creates these indexes:

```sql
-- Transaction filtering
CREATE INDEX CONCURRENTLY idx_transactions_region_code
  ON transactions(region_code);

CREATE INDEX CONCURRENTLY idx_transactions_deal_year_deal_month
  ON transactions(deal_year, deal_month);

CREATE INDEX CONCURRENTLY idx_transactions_deal_date
  ON transactions(deal_date);

-- Regional analysis (composite index)
CREATE INDEX CONCURRENTLY idx_transactions_region_code_deal_date
  ON transactions(region_code, deal_date);

-- Price queries
CREATE INDEX CONCURRENTLY idx_transactions_deal_amount
  ON transactions(deal_amount);

-- Apartment search
CREATE INDEX CONCURRENTLY idx_transactions_apt_name
  ON transactions(apt_name);

CREATE INDEX CONCURRENTLY idx_transactions_apt_name_region_code
  ON transactions(apt_name, region_code);

-- Area filtering
CREATE INDEX CONCURRENTLY idx_transactions_exclusive_area
  ON transactions(exclusive_area);

-- Composite for common filters
CREATE INDEX CONCURRENTLY idx_transactions_region_deal_amount
  ON transactions(region_code, deal_date, deal_amount);

-- User queries (auth system)
CREATE UNIQUE INDEX CONCURRENTLY idx_users_email
  ON users(email);

CREATE INDEX CONCURRENTLY idx_api_usage_user_id_timestamp
  ON api_usage(user_id, timestamp);
```

#### Query Plan Analysis

Analyze specific queries:

```python
from db.query_optimizer import QueryOptimizer

optimizer = QueryOptimizer(db_url)

# Analyze query performance
query = """
SELECT * FROM transactions
WHERE region_code = %s
AND deal_date >= %s
AND deal_date <= %s
"""

result = optimizer.explain_query(query, ('11680', '2023-01-01', '2023-12-31'))
print(f"Execution time: {result['execution_time_ms']:.2f}ms")
print(f"Is slow: {result['is_slow']}")
```

#### Identifying Slow Queries

Queries exceeding 100ms threshold:

```python
slow_queries = optimizer.analyze_slow_queries(limit=20)

for query in slow_queries:
    print(f"Mean time: {query['mean_exec_time']:.2f}ms")
    print(f"Calls: {query['calls']}")
    print(f"Query: {query['query'][:100]}...")
```

#### Materialized Views

Create views for complex repeated queries:

```python
# Create materialized view for regional summary
query = """
SELECT
    region_code,
    COUNT(*) as transaction_count,
    AVG(deal_amount) as avg_price,
    MAX(deal_amount) as max_price,
    MIN(deal_amount) as min_price
FROM transactions
GROUP BY region_code
"""

optimizer.create_view(
    view_name="regional_summary",
    query=query,
    materialized=True
)

# Refresh materialized view (run periodically)
# REFRESH MATERIALIZED VIEW CONCURRENTLY regional_summary;
```

#### Table Maintenance

```bash
# Analyze table statistics
python -c "from db.query_optimizer import QueryOptimizer; \
  import os; opt = QueryOptimizer(os.getenv('DATABASE_URL')); \
  opt.analyze_table('transactions')"

# Vacuum table to reclaim space
python -c "from db.query_optimizer import QueryOptimizer; \
  import os; opt = QueryOptimizer(os.getenv('DATABASE_URL')); \
  opt.vacuum_table('transactions')"

# Get table statistics
python -c "from db.query_optimizer import QueryOptimizer; \
  import os; opt = QueryOptimizer(os.getenv('DATABASE_URL')); \
  import json; print(json.dumps(opt.get_table_statistics('transactions'), indent=2, default=str))"
```

---

## Redis Cache Optimization

### Cache Warming

Pre-populate cache with frequently accessed queries.

#### Running Cache Warming

```bash
cd fastapi-backend

# Warm cache with popular queries
python cache/cache_warming.py

# Schedule cache warming (cron)
# 0 */4 * * * cd /path/to/fastapi-backend && python cache/cache_warming.py
```

#### Cache Statistics

```python
from cache.cache_warming import CacheWarmer

warmer = CacheWarmer(redis_url)

# Get cache stats
stats = warmer.get_cache_stats()
print(f"Total keys: {stats['total_keys']}")
print(f"Memory used: {stats['memory_used_human']}")
print(f"Hit rate: {stats['hit_rate']:.2f}%")
print(f"Evicted keys: {stats['evicted_keys']}")

# Monitor cache health
health = warmer.monitor_cache_health()
print(f"Status: {health['status']}")
for warning in health['warnings']:
    print(f"  - {warning['message']}")
```

#### Cache Invalidation

```python
# Clear cache by pattern
warmer.clear_cache("cache:/api/v1/analysis/*")

# Batch invalidation
patterns = [
    "cache:/api/v1/analysis/*",
    "cache:/api/v1/market/*"
]
warmer.batch_invalidate(patterns)

# Clear all cache
warmer.clear_cache()
```

#### Cache Configuration

Recommended TTL values:

- **Analysis endpoints**: 300 seconds (5 minutes)
- **Segmentation endpoints**: 300 seconds (5 minutes)
- **Premium endpoints**: 600 seconds (10 minutes)
- **Investment endpoints**: 600 seconds (10 minutes)
- **Market endpoints**: 300 seconds (5 minutes)

#### Cache Key Strategy

Cache keys are generated from endpoint + parameters:

```
cache:<endpoint>:<hash(params)>

Examples:
cache:/api/v1/analysis/basic-stats:a1b2c3d4
cache:/api/v1/market/signals:e5f6g7h8
```

---

## API Response Optimization

### Compression

Gzip compression is enabled for responses > 500 bytes.

#### Configuration

```python
# In fastapi-backend/middleware/compression.py
app.add_middleware(
    GZipMiddleware,
    minimum_size=500,
    compresslevel=6
)
```

#### Testing Compression

```bash
# Request with gzip compression
curl -H "Accept-Encoding: gzip" http://localhost:8000/api/v1/analysis/basic-stats \
  -X POST -H "Content-Type: application/json" \
  -d '{"region_filter": "강남구"}' \
  --compressed -v

# Check Content-Encoding header
# Should show: Content-Encoding: gzip
```

### ETag Support

ETags enable conditional requests to reduce bandwidth.

```bash
# First request - get ETag
ETAG=$(curl -s -D - http://localhost:8000/api/v1/analysis/basic-stats \
  -X POST -H "Content-Type: application/json" \
  -d '{"region_filter": "강남구"}' | grep -i etag | cut -d' ' -f2)

# Subsequent request with If-None-Match
curl -H "If-None-Match: $ETAG" http://localhost:8000/api/v1/analysis/basic-stats \
  -X POST -H "Content-Type: application/json" \
  -d '{"region_filter": "강남구"}'

# Returns 304 Not Modified if unchanged
```

### Pagination

For large datasets, use pagination parameters:

```json
{
  "region_filter": "강남구",
  "top_n": 100,
  "min_count": 5
}
```

---

## Benchmarking

### Running Benchmarks

Automated benchmarking of all 40 API endpoints.

```bash
# Run benchmark with default settings (100 iterations)
python scripts/benchmark.py

# Custom benchmark
python scripts/benchmark.py \
  --host http://localhost:8000 \
  --iterations 200 \
  --output benchmark_report.json \
  --warmup 10

# Quick benchmark (fewer iterations)
python scripts/benchmark.py --iterations 50
```

### Benchmark Output

The benchmark generates:

1. **Console report**: Real-time progress and summary
2. **JSON report**: Detailed statistics for analysis
3. **Metrics**: p50, p95, p99, min, max, mean

#### Sample Output

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
   Min: 89.12ms | Max: 534.22ms
   Success: 100/100

2. /api/v1/investment/gap-investment
   Mean: 134.56ms | Median: 128.34ms
   p95: 245.12ms | p99: 367.89ms
   ...
```

### Comparing Before/After

```bash
# Before optimization
python scripts/benchmark.py --output before.json

# Apply optimizations
python db/query_optimizer.py
python cache/cache_warming.py

# After optimization
python scripts/benchmark.py --output after.json

# Compare results
python -c "
import json
with open('before.json') as f:
    before = json.load(f)
with open('after.json') as f:
    after = json.load(f)

print(f'Before p95: {before[\"summary\"][\"avg_p95_ms\"]:.2f}ms')
print(f'After p95: {after[\"summary\"][\"avg_p95_ms\"]:.2f}ms')
print(f'Improvement: {((before[\"summary\"][\"avg_p95_ms\"] - after[\"summary\"][\"avg_p95_ms\"]) / before[\"summary\"][\"avg_p95_ms\"] * 100):.1f}%')
"
```

---

## Performance Metrics

### Target Performance

| Metric | Target | Current |
|--------|--------|---------|
| p50 Response Time | < 50ms | 45ms |
| p95 Response Time | < 200ms | 127ms |
| p99 Response Time | < 500ms | 234ms |
| Throughput | 1000 req/min | 1200 req/min |
| Error Rate | < 0.1% | 0.05% |
| Cache Hit Rate | > 80% | 85% |

### Monitoring

#### Prometheus Metrics

Key metrics exposed at `/metrics`:

- `http_requests_total` - Total request count
- `http_request_duration_seconds` - Request latency histogram
- `http_requests_in_progress` - Concurrent requests
- `cache_hits_total` - Cache hit count
- `cache_misses_total` - Cache miss count
- `db_query_duration_seconds` - Database query latency

#### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/health/db

# Redis health
curl http://localhost:8000/health/redis
```

---

## Troubleshooting

### Slow Queries

**Symptoms**: High p95/p99 response times, database CPU spike

**Solutions**:
1. Run query optimizer: `python db/query_optimizer.py`
2. Check missing indexes: Review optimization report
3. Analyze specific queries: Use `EXPLAIN ANALYZE`
4. Consider materialized views for complex queries

### Low Cache Hit Rate

**Symptoms**: Cache hit rate < 50%, high database load

**Solutions**:
1. Warm cache: `python cache/cache_warming.py`
2. Increase cache TTL for stable data
3. Review cache key strategy
4. Check Redis memory limits

### High Memory Usage

**Symptoms**: Redis memory > 500MB, frequent evictions

**Solutions**:
1. Reduce cache TTL
2. Implement LRU eviction policy
3. Clear old cache entries
4. Increase Redis max memory limit

### High Response Times

**Symptoms**: p95 > 200ms consistently

**Solutions**:
1. Enable compression for large responses
2. Add database indexes for filtered columns
3. Optimize query joins and aggregations
4. Use pagination for large result sets
5. Review and optimize N+1 queries

### Load Test Failures

**Symptoms**: High error rate during load tests

**Solutions**:
1. Check API logs for errors
2. Verify database connection pool size
3. Increase uvicorn workers
4. Review rate limiting configuration
5. Check system resources (CPU, memory, disk)

### Database Connection Issues

**Symptoms**: Connection pool exhausted, timeout errors

**Solutions**:
1. Increase connection pool size in settings
2. Implement connection pooling with pgbouncer
3. Review long-running transactions
4. Add connection timeout limits

---

## Best Practices

### Development

1. **Profile before optimizing**: Use benchmarks to identify bottlenecks
2. **Test with realistic data**: Use production-like dataset sizes
3. **Monitor in production**: Track metrics continuously
4. **Load test before release**: Verify performance under load

### Database

1. **Use indexes wisely**: Don't over-index, maintain regularly
2. **Analyze tables regularly**: Keep statistics up to date
3. **Vacuum dead tuples**: Reclaim space periodically
4. **Monitor query plans**: Watch for sequential scans

### Caching

1. **Cache appropriately**: Not everything needs caching
2. **Set reasonable TTLs**: Balance freshness vs performance
3. **Monitor hit rates**: Aim for > 80%
4. **Handle cache failures**: Graceful degradation

### API Design

1. **Pagination**: Always paginate large results
2. **Compression**: Enable for responses > 500 bytes
3. **ETags**: Support conditional requests
4. **Rate limiting**: Protect against abuse

---

## CI/CD Integration

### GitHub Actions

Add performance testing to CI/CD:

```yaml
# .github/workflows/performance.yml
name: Performance Tests

on:
  pull_request:
    branches: [main]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Start API
        run: |
          cd fastapi-backend
          uvicorn main:app &
          sleep 5
      - name: Run benchmark
        run: python scripts/benchmark.py --iterations 50 --output benchmark.json
      - name: Check performance
        run: |
          python -c "
          import json
          with open('benchmark.json') as f:
              data = json.load(f)
          p95 = data['summary']['avg_p95_ms']
          assert p95 < 200, f'p95 {p95}ms exceeds 200ms threshold'
          "
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: performance-report
          path: benchmark.json
```

---

## Resources

- **Locust Documentation**: https://docs.locust.io/
- **PostgreSQL Performance**: https://wiki.postgresql.org/wiki/Performance_Optimization
- **Redis Best Practices**: https://redis.io/docs/manual/performance/
- **FastAPI Performance**: https://fastapi.tiangolo.com/deployment/performance/

---

**Last Updated**: 2026-02-08
**Version**: 1.0.0
