# Monitoring and Observability Guide

Comprehensive monitoring setup for the Apartment Analysis Platform using Sentry, Prometheus, Grafana, and structured logging.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Sentry Integration](#sentry-integration)
- [Logging Configuration](#logging-configuration)
- [Prometheus Metrics](#prometheus-metrics)
- [Grafana Dashboards](#grafana-dashboards)
- [Health Checks](#health-checks)
- [Alerts](#alerts)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

### Monitoring Stack

```
┌─────────────────┐
│   Next.js App   │──► Sentry (Frontend Errors)
│  (Port 3000)    │──► Browser Console
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Backend│──► Sentry (Backend Errors)
│  (Port 8000)    │──► Structured Logs (JSON)
│                 │──► Prometheus Metrics
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Monitoring Stack (Docker Compose)      │
│                                         │
│  ┌─────────────┐  ┌──────────────┐    │
│  │ Prometheus  │──│  Alertmanager│    │
│  │ (Port 9090) │  │  (Port 9093) │    │
│  └──────┬──────┘  └──────────────┘    │
│         │                               │
│         ▼                               │
│  ┌─────────────┐                       │
│  │   Grafana   │                       │
│  │ (Port 3001) │                       │
│  └─────────────┘                       │
│                                         │
│  Exporters:                             │
│  - PostgreSQL (9187)                    │
│  - Redis (9121)                         │
│  - Node (9100)                          │
└─────────────────────────────────────────┘
```

### Components

| Component | Purpose | Port |
|-----------|---------|------|
| Sentry | Error tracking & performance monitoring | N/A (SaaS) |
| Prometheus | Metrics collection | 9090 |
| Grafana | Metrics visualization | 3001 |
| Alertmanager | Alert routing & notification | 9093 |
| PostgreSQL Exporter | Database metrics | 9187 |
| Redis Exporter | Cache metrics | 9121 |
| Node Exporter | System metrics | 9100 |

## Quick Start

### 1. Install Dependencies

**Backend:**
```bash
cd fastapi-backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd nextjs-frontend
npm install
```

### 2. Get Sentry DSN

1. Create account at https://sentry.io
2. Create new project:
   - **Backend**: Python / FastAPI
   - **Frontend**: JavaScript / Next.js
3. Copy DSN from project settings

### 3. Configure Environment

**Backend (.env):**
```bash
# Copy example file
cp fastapi-backend/.env.monitoring.example fastapi-backend/.env

# Add your Sentry DSN
SENTRY_DSN=https://your-sentry-dsn@sentry.io/your-project-id
SENTRY_ENVIRONMENT=development
SENTRY_TRACES_SAMPLE_RATE=0.1
APP_VERSION=1.0.0
LOG_LEVEL=INFO
ENABLE_METRICS=true
```

**Frontend (.env.local):**
```bash
# Copy example file
cp nextjs-frontend/.env.monitoring.example nextjs-frontend/.env.local

# Add your Sentry DSN
NEXT_PUBLIC_SENTRY_DSN=https://your-sentry-dsn@sentry.io/your-project-id
NEXT_PUBLIC_SENTRY_ENVIRONMENT=development
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### 4. Start Monitoring Stack

```bash
cd monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

### 5. Verify Setup

```bash
# Check health endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/health/detailed

# Check metrics
curl http://localhost:8000/api/metrics

# Access dashboards
open http://localhost:9090    # Prometheus
open http://localhost:3001    # Grafana (admin/admin)
open http://localhost:9093    # Alertmanager
```

## Sentry Integration

### Backend (FastAPI)

Sentry is automatically initialized in `main.py`. Configuration in `/Users/koscom/Downloads/apt_test/fastapi-backend/config/sentry.py`.

**Features:**
- Error tracking with stack traces
- Performance monitoring (traces)
- Release tracking
- Privacy-first (no PII sent)
- Automatic FastAPI, SQLAlchemy, Redis integration

**Manual Error Capture:**
```python
from config.sentry import capture_exception, capture_message, set_user_context

# Capture exception with context
try:
    result = process_data(user_id)
except Exception as e:
    capture_exception(e, context={
        "user_id": user_id,
        "operation": "process_data"
    })
    raise

# Capture message
capture_message(
    "High memory usage detected",
    level="warning",
    context={"memory_mb": 1024}
)

# Set user context for error tracking
set_user_context(
    user_id="123",
    email="user@example.com",  # Optional
    username="john_doe"
)
```

### Frontend (Next.js)

Initialize Sentry in your app. Configuration in `/Users/koscom/Downloads/apt_test/nextjs-frontend/src/config/sentry.config.ts`.

**Integration:**
```typescript
// _app.tsx or layout.tsx
import { initSentry } from '@/config/sentry.config';

initSentry();
```

**Error Capture:**
```typescript
import {
  captureException,
  captureMessage,
  setUserContext,
  addBreadcrumb
} from '@/config/sentry.config';

// Capture errors
try {
  await fetchData();
} catch (error) {
  captureException(error as Error, {
    component: 'DataTable',
    action: 'fetch'
  });
}

// Add debugging breadcrumbs
addBreadcrumb(
  'User clicked export',
  'user-action',
  'info',
  { format: 'csv', rows: 100 }
);

// Set user context
setUserContext('user-123', 'user@example.com', 'john_doe');
```

### Sentry Dashboard

Access your Sentry dashboard to:
- View errors with stack traces
- Monitor performance (transaction traces)
- Track releases and deployments
- Set up alerts for new errors
- View user feedback

## Logging Configuration

### Structured Logging

Logs are written in JSON format for easy parsing and analysis.

**Configuration:** `/Users/koscom/Downloads/apt_test/fastapi-backend/config/logging.py`

**Usage:**
```python
import structlog

logger = structlog.get_logger(__name__)

# Info logging
logger.info(
    "api_request_completed",
    path="/api/v1/analysis/stats",
    method="GET",
    status_code=200,
    duration_ms=123.45,
    user_id="user-123"
)

# Error logging
logger.error(
    "database_query_failed",
    query_type="select_transactions",
    error=str(e),
    retry_count=3
)

# Warning logging
logger.warning(
    "cache_miss",
    cache_key="stats:11680:202312",
    fallback="database"
)
```

**JSON Output:**
```json
{
  "event": "api_request_completed",
  "path": "/api/v1/analysis/stats",
  "method": "GET",
  "status_code": 200,
  "duration_ms": 123.45,
  "user_id": "user-123",
  "timestamp": "2026-02-08T10:30:45.123456Z",
  "level": "info",
  "logger": "routers.analysis",
  "filename": "analysis.py",
  "func_name": "get_basic_stats",
  "lineno": 45
}
```

### Log Files

Location: `/Users/koscom/Downloads/apt_test/fastapi-backend/logs/`

| File | Content | Rotation | Retention |
|------|---------|----------|-----------|
| `app.log` | All logs (INFO+) | 100MB | 10 backups |
| `error.log` | Errors only (ERROR+) | 100MB | 10 backups |
| `access.log` | HTTP access logs | Daily | 30 days |

### Log Privacy

Sensitive data is automatically sanitized:
```python
from config.logging import sanitize_log_data

user_data = {
    "email": "user@example.com",
    "password": "secret123",
    "api_key": "sk-abc123"
}

logger.info("user_created", **sanitize_log_data(user_data))
# Output: {"email": "user@example.com", "password": "[REDACTED]", "api_key": "[REDACTED]"}
```

### Viewing Logs

```bash
# Tail all logs
tail -f fastapi-backend/logs/app.log

# View errors only
tail -f fastapi-backend/logs/error.log

# Parse JSON logs
cat fastapi-backend/logs/app.log | jq 'select(.level=="error")'

# Count errors by type
cat fastapi-backend/logs/app.log | jq -r '.event' | sort | uniq -c | sort -rn
```

## Prometheus Metrics

### Endpoints

- **Metrics**: http://localhost:8000/api/metrics
- **Prometheus UI**: http://localhost:9090

### Available Metrics

**HTTP Metrics (auto-instrumented):**
```
http_requests_total{method,endpoint,status}
http_request_duration_seconds{method,endpoint}
http_requests_inprogress
```

**Business Metrics:**
```
analysis_requests_total{analysis_type}
analysis_duration_seconds{analysis_type}
cache_hits_total{cache_type}
cache_misses_total{cache_type}
database_queries_total{query_type}
database_query_duration_seconds{query_type}
external_api_requests_total{api_name,status}
external_api_duration_seconds{api_name}
```

**System Metrics:**
```
active_connections
active_database_connections
authenticated_users
subscription_users_total{plan_type}
total_transactions_in_database
errors_total{error_type,severity}
```

### Recording Custom Metrics

**File:** `/Users/koscom/Downloads/apt_test/fastapi-backend/routers/metrics.py`

```python
from routers.metrics import (
    record_analysis_request,
    record_analysis_duration,
    record_cache_hit,
    record_cache_miss,
    record_database_query,
    record_error,
)

# Record analysis
record_analysis_request("basic-stats")

# Record duration
import time
start = time.time()
# ... process ...
record_analysis_duration("basic-stats", time.time() - start)

# Record cache
if cache_hit:
    record_cache_hit("redis")
else:
    record_cache_miss("redis")

# Record database query
start = time.time()
# ... query ...
record_database_query("select_transactions", time.time() - start)

# Record error
record_error("validation_error", severity="warning")
```

### Querying Metrics

```promql
# Request rate (requests/sec)
rate(api_requests_total[5m])

# 95th percentile response time
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Cache hit rate
rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))

# Error rate
rate(errors_total[5m])

# Slow queries
histogram_quantile(0.95, rate(database_query_duration_seconds_bucket[5m])) > 1
```

## Grafana Dashboards

### Access

http://localhost:3001
- Username: `admin`
- Password: `admin`

### Dashboard

Pre-configured dashboard: `/Users/koscom/Downloads/apt_test/monitoring/grafana-dashboard.json`

**Panels:**
1. API Health Status
2. Request Rate (by endpoint)
3. Error Rate (by type)
4. Response Time (p50, p95)
5. Analysis Requests (by type)
6. Database Health
7. Active DB Connections
8. Database Query Duration
9. Redis Health
10. Cache Hit Rate
11. Redis Memory Usage
12. External API Metrics
13. Active Users
14. Subscription Users (by plan)
15. Total Transactions
16. CPU Usage
17. Memory Usage
18. Disk Usage

### Importing Dashboard

1. Navigate to Grafana → Dashboards → Import
2. Upload `/Users/koscom/Downloads/apt_test/monitoring/grafana-dashboard.json`
3. Select Prometheus as data source
4. Click Import

## Health Checks

### Endpoints

**File:** `/Users/koscom/Downloads/apt_test/fastapi-backend/routers/health.py`

| Endpoint | Purpose | Use Case |
|----------|---------|----------|
| `/api/health` | Basic health | Load balancer |
| `/api/health/detailed` | All dependencies | Operations |
| `/api/health/ready` | Readiness probe | Kubernetes |
| `/api/health/live` | Liveness probe | Kubernetes |

### Basic Health

```bash
curl http://localhost:8000/api/health
```

Response:
```json
{
  "status": "healthy",
  "service": "apartment-transaction-analysis-api",
  "version": "1.0.0",
  "timestamp": "2026-02-08T10:30:45.123456Z"
}
```

### Detailed Health

```bash
curl http://localhost:8000/api/health/detailed
```

Response:
```json
{
  "status": "healthy",
  "service": "apartment-transaction-analysis-api",
  "version": "1.0.0",
  "timestamp": "2026-02-08T10:30:45.123456Z",
  "uptime_seconds": 12345.67,
  "dependencies": {
    "database": {
      "status": "healthy",
      "latency_ms": 12.34
    },
    "redis": {
      "status": "healthy",
      "latency_ms": 2.56,
      "details": {
        "connected_clients": 5,
        "used_memory_human": "1.2M",
        "uptime_in_seconds": 86400
      }
    },
    "external_api": {
      "status": "healthy",
      "latency_ms": 234.56
    }
  }
}
```

## Alerts

### Alert Rules

**File:** `/Users/koscom/Downloads/apt_test/monitoring/alerts.yml`

**Critical Alerts:**
- API Down (2+ minutes)
- Database Down (2+ minutes)
- Low Disk Space (<10%)

**Warning Alerts:**
- High Error Rate (>10 errors/sec)
- High Response Time (p95 > 2s)
- High DB Connections (>80)
- Slow Queries (p95 > 1s)
- Redis Down
- High Redis Memory (>90%)

**Info Alerts:**
- Low Cache Hit Rate (<50%)
- External API Issues
- No Activity (1+ hour)
- Traffic Spike (2x normal)

### Notification Setup

**File:** `/Users/koscom/Downloads/apt_test/monitoring/alertmanager.yml`

Configure notifications:

**Slack:**
```yaml
slack_configs:
  - api_url: 'YOUR_SLACK_WEBHOOK_URL'
    channel: '#alerts'
    title: 'Alert: {{ .GroupLabels.alertname }}'
    text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

**Email:**
```yaml
email_configs:
  - to: 'ops@example.com'
    from: 'alerts@example.com'
    smarthost: 'smtp.gmail.com:587'
    auth_username: 'alerts@example.com'
    auth_password: 'YOUR_PASSWORD'
```

## Troubleshooting

### Sentry Not Capturing Errors

```bash
# 1. Check DSN is set
echo $SENTRY_DSN

# 2. Check logs
grep "sentry" fastapi-backend/logs/app.log

# 3. Test error capture
curl -X POST http://localhost:8000/api/test-error
```

### Metrics Not Appearing

```bash
# 1. Check metrics endpoint
curl http://localhost:8000/api/metrics

# 2. Check Prometheus targets
open http://localhost:9090/targets

# 3. Check Prometheus logs
docker logs apt-prometheus
```

### Logs Not Rotating

```bash
# 1. Check configuration
cat fastapi-backend/.env | grep LOG

# 2. Check log directory
ls -lah fastapi-backend/logs/

# 3. Check disk space
df -h
```

### High Memory Usage

```bash
# 1. Check metrics
curl http://localhost:8000/api/metrics | grep memory

# 2. Check processes
docker stats

# 3. Check connections
curl http://localhost:8000/api/health/detailed
```

## Best Practices

### 1. Error Handling
Always capture errors with context:
```python
try:
    result = risky_operation()
except Exception as e:
    logger.error("operation_failed", error=str(e), context="important")
    capture_exception(e, context={"operation": "risky"})
    raise
```

### 2. Privacy
Never log sensitive data:
- Passwords
- API keys
- Credit cards
- Personal info

Use sanitization:
```python
logger.info("user_action", **sanitize_log_data(user_data))
```

### 3. Metric Naming
Follow conventions:
- Use underscores: `api_requests_total`
- Add units: `duration_seconds`
- Use labels: `{method="GET"}`

### 4. Alert Fatigue
- Set appropriate thresholds
- Use inhibition rules
- Group related alerts
- Critical = immediate action
- Warning = investigate soon
- Info = track trends

### 5. Log Levels
- DEBUG: Development only
- INFO: Normal operations
- WARNING: Recoverable issues
- ERROR: Handled exceptions
- CRITICAL: Service degradation

### 6. Retention
- Logs: 30 days
- Metrics: 15 days (Prometheus)
- Errors: 90 days (Sentry)

---

**Files Created:**
- `/Users/koscom/Downloads/apt_test/fastapi-backend/config/sentry.py`
- `/Users/koscom/Downloads/apt_test/fastapi-backend/config/logging.py`
- `/Users/koscom/Downloads/apt_test/fastapi-backend/routers/health.py`
- `/Users/koscom/Downloads/apt_test/fastapi-backend/routers/metrics.py`
- `/Users/koscom/Downloads/apt_test/nextjs-frontend/src/config/sentry.config.ts`
- `/Users/koscom/Downloads/apt_test/monitoring/prometheus.yml`
- `/Users/koscom/Downloads/apt_test/monitoring/alerts.yml`
- `/Users/koscom/Downloads/apt_test/monitoring/alertmanager.yml`
- `/Users/koscom/Downloads/apt_test/monitoring/grafana-dashboard.json`
- `/Users/koscom/Downloads/apt_test/monitoring/docker-compose.monitoring.yml`

**Last Updated**: 2026-02-08
**Version**: 1.0.0
