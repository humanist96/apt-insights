# Database Query Optimization

## Current Implementation Analysis

### Query Patterns in analyzer_service.py

The service currently uses:
- In-memory caching with 5-minute TTL
- Sequential filtering operations
- Statistics package for aggregations

### Optimization Recommendations

#### 1. Database Indexes (PostgreSQL)

When using PostgreSQL mode, ensure these indexes exist:

```sql
-- Transaction date range queries
CREATE INDEX idx_transactions_deal_date ON transactions(_deal_date);

-- Regional filtering
CREATE INDEX idx_transactions_region ON transactions(_region_name);

-- Price-based queries
CREATE INDEX idx_transactions_price ON transactions(_deal_amount_numeric);

-- Composite index for common query patterns
CREATE INDEX idx_transactions_region_date
ON transactions(_region_name, _deal_date);

-- Area-based queries
CREATE INDEX idx_transactions_area ON transactions(_area_numeric);

-- Full-text search (apartment names)
CREATE INDEX idx_transactions_apt_name_gin
ON transactions USING gin(to_tsvector('korean', apartment_name));
```

#### 2. Query Profiling Setup

Add query profiling to identify slow queries:

```python
import time
from functools import wraps

def profile_query(func):
    """Decorator to profile database query execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start

        if duration > 1.0:  # Log queries taking > 1 second
            logger.warning(
                "slow_query",
                function=func.__name__,
                duration_seconds=duration
            )

        return result
    return wrapper
```

#### 3. Batch Loading Optimization

Current implementation loads all data at once. For large datasets:

**Recommendation**: Implement pagination at the database level:

```python
def get_transactions_paginated(
    offset: int = 0,
    limit: int = 1000,
    filters: Optional[Dict] = None
) -> Tuple[List[Dict], int]:
    """
    Load transactions with pagination

    Returns:
        Tuple of (items, total_count)
    """
    # Apply filters and return paginated results
    pass
```

#### 4. Aggregation Optimization

For statistical calculations, use database aggregation functions instead of loading all data into memory:

```python
# Instead of loading all data and calculating in Python:
# prices = [item['price'] for item in items]
# avg_price = statistics.mean(prices)

# Use SQL aggregation:
# SELECT AVG(_deal_amount_numeric) as avg_price,
#        MAX(_deal_amount_numeric) as max_price,
#        MIN(_deal_amount_numeric) as min_price,
#        COUNT(*) as total_count
# FROM transactions
# WHERE ...
```

#### 5. Connection Pooling

Ensure SQLAlchemy is configured with proper connection pooling:

```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=20,          # Number of persistent connections
    max_overflow=10,       # Additional connections on high load
    pool_pre_ping=True,    # Verify connections before use
    pool_recycle=3600,     # Recycle connections after 1 hour
)
```

## Current Performance Baselines

### In-Memory Mode (JSON files)
- Data loading: ~100-200ms (first load)
- Data loading: ~1-5ms (cached)
- Filter operations: ~10-50ms depending on dataset size
- Aggregations: ~20-100ms depending on complexity

### PostgreSQL Mode (when USE_DATABASE=true)
- Query with indexes: Target < 100ms for simple queries
- Complex aggregations: Target < 500ms
- Full table scan: Should be avoided

## Monitoring Recommendations

1. **Add query logging in production**:
   - Log all queries taking > 500ms
   - Track query patterns and frequency
   - Monitor cache hit rates

2. **Add metrics endpoint**:
   ```python
   @app.get("/metrics/db")
   async def database_metrics():
       return {
           "cache_hit_rate": cache_hit_rate,
           "avg_query_time_ms": avg_query_time,
           "slow_queries_count": slow_queries_count,
       }
   ```

3. **Use database query analyzer**:
   ```sql
   EXPLAIN ANALYZE SELECT ...
   ```

## Action Items

- [ ] Create database indexes migration script
- [ ] Add query profiling decorator
- [ ] Implement pagination for large datasets
- [ ] Move aggregations to database layer
- [ ] Configure connection pooling
- [ ] Add performance monitoring endpoint
- [ ] Create query benchmarking suite
