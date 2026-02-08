# Load Testing with Locust

Comprehensive load testing suite for the apartment analysis platform.

## Quick Start

```bash
# Install Locust
pip install locust

# Start API server
cd ../../fastapi-backend
uvicorn main:app --reload --port 8000

# Run load test (in separate terminal)
locust -f locustfile.py --host=http://localhost:8000

# Access web UI
open http://localhost:8089
```

## Test Scenarios

### 1. Free User (70% of users)
- **Limit**: 10 API calls/day
- **Behavior**: Basic stats, price trends, regional analysis
- **Wait time**: 10-30 seconds between requests
- **Use case**: Casual users exploring data

### 2. Premium User (30% of users)
- **Limit**: Unlimited API calls
- **Behavior**: Deep analysis across all endpoints
- **Wait time**: 2-5 seconds between requests
- **Use case**: Regular users doing research

### 3. Power User (10% of users)
- **Limit**: Unlimited API calls
- **Behavior**: Intensive rapid-fire analysis
- **Wait time**: 1-3 seconds between requests
- **Use case**: Professional analysts, automated systems

## Running Tests

### Basic Test

```bash
# Run with 100 users, spawn rate 10 users/sec
locust -f locustfile.py --host=http://localhost:8000 \
  --users 100 --spawn-rate 10 --run-time 10m
```

### Ramped Load Test

Uses the built-in `RampedLoadTest` shape:

```bash
locust -f locustfile.py --host=http://localhost:8000
```

Load progression:
1. 0-2 min: 10 users (warm-up)
2. 2-5 min: 50 users (normal)
3. 5-8 min: 100 users (peak)
4. 8-10 min: 200 users (stress)
5. 10+ min: 100 users (sustained)

### Generate Reports

```bash
# CSV + HTML reports
locust -f locustfile.py --host=http://localhost:8000 \
  --users 100 --spawn-rate 10 --run-time 10m \
  --csv=results/load_test \
  --html=results/load_test.html
```

### Headless Mode

```bash
# Run without web UI (CI/CD)
locust -f locustfile.py --host=http://localhost:8000 \
  --headless --users 100 --spawn-rate 10 --run-time 10m \
  --csv=results/load_test
```

## Distributed Load Testing

For high load scenarios (1000+ users), use distributed mode:

```bash
# Start master
locust -f locustfile.py --master --host=http://localhost:8000

# Start workers (on same or different machines)
locust -f locustfile.py --worker --master-host=localhost
locust -f locustfile.py --worker --master-host=localhost
locust -f locustfile.py --worker --master-host=localhost
```

## Key Metrics

Monitor these during tests:

- **Response Time**: p50, p95, p99
- **Throughput**: Requests per second
- **Error Rate**: Failed requests / Total requests
- **Success Rate**: Target > 99%

## Performance Targets

| Metric | Target |
|--------|--------|
| p50 Response Time | < 50ms |
| p95 Response Time | < 200ms |
| p99 Response Time | < 500ms |
| Throughput | 1000 req/min |
| Error Rate | < 0.1% |

## Interpreting Results

### Good Results
- Success rate > 99%
- p95 < 200ms
- Error rate < 0.1%
- Stable throughput

### Warning Signs
- Success rate < 95%
- p95 > 500ms
- Error rate > 1%
- Declining throughput

### Critical Issues
- Success rate < 90%
- p95 > 1000ms
- Error rate > 5%
- System unresponsive

## Troubleshooting

### High Error Rate

**Possible causes**:
- Database connection pool exhausted
- Rate limiting triggered
- Backend service overloaded

**Solutions**:
- Increase connection pool size
- Add more API workers
- Optimize database queries
- Scale horizontally

### Slow Response Times

**Possible causes**:
- Slow database queries
- Low cache hit rate
- Insufficient resources

**Solutions**:
- Run query optimizer
- Warm cache before test
- Add indexes to database
- Increase server resources

### Inconsistent Performance

**Possible causes**:
- Cache warming effects
- Connection pool initialization
- JIT compilation warm-up

**Solutions**:
- Run warm-up phase (first 2 minutes)
- Ignore first 100 requests in analysis
- Use steady-state metrics (after 5 minutes)

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Load Test

on:
  pull_request:
    branches: [main]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install locust
      - name: Start API
        run: |
          cd fastapi-backend
          uvicorn main:app &
          sleep 5
      - name: Run load test
        run: |
          cd tests/load
          locust -f locustfile.py --host=http://localhost:8000 \
            --headless --users 50 --spawn-rate 10 --run-time 2m \
            --csv=results/load_test
      - name: Check results
        run: |
          python -c "
          import csv
          with open('tests/load/results/load_test_stats.csv') as f:
              reader = csv.DictReader(f)
              for row in reader:
                  if row['Name'] == 'Aggregated':
                      failure_rate = float(row['Failure Count']) / float(row['Request Count'])
                      assert failure_rate < 0.01, f'Failure rate {failure_rate:.2%} exceeds 1%'
          "
```

## Best Practices

1. **Always warm up**: Ignore first 2 minutes of data
2. **Test realistic scenarios**: Match production user behavior
3. **Monitor system resources**: CPU, memory, disk, network
4. **Compare baselines**: Track performance over time
5. **Test before deployment**: Catch issues early
6. **Use production-like data**: Realistic dataset sizes
7. **Gradual ramp-up**: Avoid shocking the system

## Advanced Usage

### Custom User Classes

Create specialized user behaviors:

```python
class AnalystUser(HttpUser):
    weight = 5
    wait_time = between(1, 3)

    @task
    def deep_analysis(self):
        # Custom analysis workflow
        pass
```

### Event Hooks

Add custom logging or monitoring:

```python
@events.request.add_listener
def on_request(request_type, name, response_time, **kwargs):
    if response_time > 1000:
        logger.warning(f"Slow request: {name} took {response_time}ms")
```

### Custom Shapes

Define complex load patterns:

```python
class SpikeLoadTest(LoadTestShape):
    def tick(self):
        # Implement spike pattern
        pass
```

## Resources

- **Locust Documentation**: https://docs.locust.io/
- **Best Practices**: https://docs.locust.io/en/stable/writing-a-locustfile.html
- **Distributed Testing**: https://docs.locust.io/en/stable/running-distributed.html
