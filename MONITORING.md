# Monitoring & Observability Guide

Complete guide for monitoring the Korean Apartment Transaction Analysis Platform in production.

## Table of Contents

- [Overview](#overview)
- [Health Checks](#health-checks)
- [Logging](#logging)
- [Metrics](#metrics)
- [Alerting](#alerting)
- [Dashboards](#dashboards)
- [Troubleshooting](#troubleshooting)

## Overview

### Monitoring Stack

```
┌─────────────────────────────────────────────────┐
│                   Frontend                       │
│  - Vercel Analytics (built-in)                  │
│  - Web Vitals (Core Web Vitals)                │
│  - Real User Monitoring (RUM)                   │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│                   Backend                        │
│  - Railway Logs                                 │
│  - Structured Logging (structlog)               │
│  - Health Endpoints                             │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│                  Database                        │
│  - PostgreSQL Metrics                           │
│  - Query Performance                            │
│  - Connection Pool Monitoring                   │
└─────────────────────────────────────────────────┘
```

### Key Metrics

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| API Response Time (p95) | < 200ms | > 500ms |
| API Error Rate | < 0.1% | > 1% |
| Database Query Time (p95) | < 100ms | > 300ms |
| Cache Hit Rate | > 80% | < 50% |
| Uptime | > 99.9% | < 99% |
| Memory Usage | < 80% | > 90% |
| CPU Usage | < 70% | > 85% |

---

## Health Checks

### Frontend Health Check

**Endpoint**: `GET /api/health`

```bash
# Test health endpoint
curl https://your-app.vercel.app/api/health

# Expected response
{
  "status": "healthy",
  "service": "nextjs-frontend",
  "version": "1.0.0",
  "timestamp": "2026-02-07T12:00:00.000Z",
  "environment": "production",
  "apiUrl": "https://your-backend.railway.app"
}
```

**Health Check Script** (save as `check-frontend.sh`):

```bash
#!/bin/bash
FRONTEND_URL="https://your-app.vercel.app"
RESPONSE=$(curl -s "$FRONTEND_URL/api/health")
STATUS=$(echo "$RESPONSE" | jq -r '.status')

if [ "$STATUS" == "healthy" ]; then
    echo "✅ Frontend is healthy"
    exit 0
else
    echo "❌ Frontend is unhealthy: $RESPONSE"
    exit 1
fi
```

### Backend Health Check

**Endpoint**: `GET /health`

```bash
# Test health endpoint
curl https://your-backend.railway.app/health

# Expected response
{
  "status": "healthy",
  "service": "apartment-transaction-analysis-api",
  "version": "1.0.0",
  "timestamp": "2026-02-07T12:00:00.000000"
}
```

**Health Check Script** (save as `check-backend.sh`):

```bash
#!/bin/bash
BACKEND_URL="https://your-backend.railway.app"
RESPONSE=$(curl -s "$BACKEND_URL/health")
STATUS=$(echo "$RESPONSE" | jq -r '.status')

if [ "$STATUS" == "healthy" ]; then
    echo "✅ Backend is healthy"
    exit 0
else
    echo "❌ Backend is unhealthy: $RESPONSE"
    exit 1
fi
```

### Database Health Check

```bash
# Docker deployment
docker-compose -f docker-compose.prod.yml exec postgres \
    pg_isready -U postgres

# Railway deployment
railway run psql $DATABASE_URL -c "SELECT 1;"
```

### Redis Health Check

```bash
# Docker deployment
docker-compose -f docker-compose.prod.yml exec redis \
    redis-cli -a $REDIS_PASSWORD ping

# Railway deployment
railway run redis-cli -u $REDIS_URL ping
```

---

## Logging

### Log Levels

```
DEBUG   → Development only, verbose information
INFO    → General information, normal operations
WARNING → Warning messages, potential issues
ERROR   → Error conditions, failed operations
CRITICAL→ Critical errors, service down
```

### Backend Logging Configuration

Structured JSON logging using `structlog`:

```python
# logger.py
import structlog

logger = structlog.get_logger(__name__)

# Log examples
logger.info("api_request", path="/api/v1/analysis/stats", method="GET")
logger.error("database_error", error=str(e), query="SELECT ...")
logger.warning("cache_miss", key="stats:11680:202312")
```

### Viewing Logs

#### Railway Logs

```bash
# View logs
railway logs

# Follow logs in real-time
railway logs --follow

# Filter by service
railway logs --service backend

# Export logs
railway logs > backend-logs.txt
```

#### Vercel Logs

```bash
# View logs
vercel logs

# Follow logs in real-time
vercel logs --follow

# Filter by production
vercel logs --production
```

#### Docker Logs

```bash
# View all service logs
docker-compose -f docker-compose.prod.yml logs

# Follow logs in real-time
docker-compose -f docker-compose.prod.yml logs -f

# View specific service
docker-compose -f docker-compose.prod.yml logs backend

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 backend
```

### Log Analysis

#### Search for Errors

```bash
# Railway
railway logs | grep ERROR

# Docker
docker-compose -f docker-compose.prod.yml logs | grep ERROR

# Count errors by type
railway logs | grep ERROR | cut -d' ' -f5- | sort | uniq -c
```

#### Analyze API Performance

```bash
# Extract response times from logs
railway logs | grep "api_request" | jq '.duration'

# Calculate average response time
railway logs | grep "api_request" | jq '.duration' | \
    awk '{sum+=$1; count++} END {print sum/count}'
```

---

## Metrics

### Application Metrics

#### API Endpoint Metrics

Track these metrics for each endpoint:

- **Request Count**: Total requests per endpoint
- **Response Time**: p50, p95, p99 percentiles
- **Error Rate**: 4xx and 5xx errors
- **Request Size**: Average request payload size
- **Response Size**: Average response payload size

#### Database Metrics

```sql
-- Active connections
SELECT count(*) FROM pg_stat_activity
WHERE datname = 'apt_insights';

-- Database size
SELECT pg_size_pretty(pg_database_size('apt_insights'));

-- Table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Slow queries (requires pg_stat_statements extension)
SELECT
    query,
    calls,
    mean_exec_time,
    max_exec_time,
    stddev_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Cache hit ratio
SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit) as heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) * 100 AS cache_hit_ratio
FROM pg_statio_user_tables;
```

#### Redis Metrics

```bash
# Get Redis info
redis-cli -u $REDIS_URL INFO

# Key metrics to monitor
redis-cli -u $REDIS_URL INFO stats | grep -E 'hit_rate|used_memory'

# Check memory usage
redis-cli -u $REDIS_URL INFO memory | grep used_memory_human

# Check connected clients
redis-cli -u $REDIS_URL INFO clients | grep connected_clients
```

### Custom Metrics Script

Create a metrics collection script (`scripts/collect-metrics.sh`):

```bash
#!/bin/bash
# Collect and display application metrics

echo "========================================"
echo "  Application Metrics"
echo "========================================"
echo "Timestamp: $(date)"
echo ""

# Frontend health
echo "Frontend Health:"
curl -s https://your-app.vercel.app/api/health | jq .

echo ""
echo "Backend Health:"
curl -s https://your-backend.railway.app/health | jq .

echo ""
echo "Backend Stats:"
curl -s https://your-backend.railway.app/api/v1/analysis/stats | jq '.meta'

echo ""
echo "Database Metrics:"
railway run psql $DATABASE_URL -c "SELECT count(*) as active_connections FROM pg_stat_activity WHERE datname = 'apt_insights';"

echo ""
echo "Database Size:"
railway run psql $DATABASE_URL -c "SELECT pg_size_pretty(pg_database_size('apt_insights'));"
```

---

## Alerting

### Uptime Monitoring with UptimeRobot

1. **Create Account**: https://uptimerobot.com
2. **Add Monitors**:

   **Frontend Monitor**:
   - Monitor Type: HTTP(s)
   - URL: `https://your-app.vercel.app/api/health`
   - Monitoring Interval: 5 minutes
   - Alert Contacts: Your email/SMS

   **Backend Monitor**:
   - Monitor Type: HTTP(s)
   - URL: `https://your-backend.railway.app/health`
   - Monitoring Interval: 5 minutes
   - Alert Contacts: Your email/SMS

3. **Configure Alerts**:
   - Email notifications
   - SMS notifications (optional)
   - Slack/Discord webhook (optional)

### Alert Rules

#### Critical Alerts (Immediate Response)

- [ ] Service completely down (all health checks failing)
- [ ] Database connection lost
- [ ] Error rate > 5%
- [ ] Response time > 2 seconds
- [ ] Disk space > 90%

#### Warning Alerts (Monitor Closely)

- [ ] Response time > 500ms
- [ ] Error rate > 1%
- [ ] Memory usage > 80%
- [ ] CPU usage > 80%
- [ ] Cache hit rate < 50%

#### Info Alerts (Track Trends)

- [ ] Traffic spike (2x normal)
- [ ] Slow query detected (> 1s)
- [ ] Backup completed
- [ ] Deployment completed

### Email Alert Template

```
Subject: [ALERT] {{SERVICE_NAME}} - {{ALERT_TYPE}}

Service: {{SERVICE_NAME}}
Alert: {{ALERT_TYPE}}
Severity: {{SEVERITY}}
Time: {{TIMESTAMP}}

Details:
{{ALERT_DETAILS}}

Action Required:
{{ACTION_ITEMS}}

Runbook:
{{RUNBOOK_LINK}}
```

---

## Dashboards

### Vercel Analytics Dashboard

Built-in analytics in Vercel dashboard:

- **Real User Monitoring**: Page views, unique visitors
- **Web Vitals**: LCP, FID, CLS, TTFB
- **Top Pages**: Most visited pages
- **Devices**: Desktop vs Mobile traffic
- **Locations**: Geographic distribution

Enable in: Vercel Dashboard → Project → Analytics

### Railway Dashboard

Built-in metrics in Railway dashboard:

- **CPU Usage**: Current and historical
- **Memory Usage**: Current and historical
- **Network Traffic**: Inbound/outbound
- **Logs**: Real-time log stream

Access: Railway Dashboard → Project → Metrics

### Custom Dashboard Script

Create a dashboard script (`scripts/dashboard.sh`):

```bash
#!/bin/bash
# Real-time monitoring dashboard

watch -n 5 '
    clear
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║         Apartment Insights - Live Dashboard               ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "⏰ $(date)"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🌐 Service Health"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Frontend
    if curl -s https://your-app.vercel.app/api/health > /dev/null; then
        echo "  Frontend:  ✅ HEALTHY"
    else
        echo "  Frontend:  ❌ DOWN"
    fi

    # Backend
    if curl -s https://your-backend.railway.app/health > /dev/null; then
        echo "  Backend:   ✅ HEALTHY"
    else
        echo "  Backend:   ❌ DOWN"
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 API Metrics"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    curl -s https://your-backend.railway.app/api/v1/analysis/stats | jq -r "
        \"  Transactions: \(.data.transaction_count // \"N/A\")
  Avg Price: \(.data.average_price // \"N/A\")
  Min Price: \(.data.min_price // \"N/A\")
  Max Price: \(.data.max_price // \"N/A\")\"
    "

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "💾 Database"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    docker-compose -f docker-compose.prod.yml exec -T postgres \
        psql -U postgres -d apt_insights -t -c "
        SELECT
            '\''  Connections: '\'' || count(*)
        FROM pg_stat_activity
        WHERE datname = '\''apt_insights'\'';" 2>/dev/null || echo "  Status: Unknown"

    echo ""
'
```

---

## Troubleshooting

### High Response Times

1. **Check backend logs**:
   ```bash
   railway logs | grep "duration" | sort -n -k3
   ```

2. **Identify slow queries**:
   ```sql
   SELECT query, mean_exec_time
   FROM pg_stat_statements
   ORDER BY mean_exec_time DESC
   LIMIT 5;
   ```

3. **Check cache hit rate**:
   ```bash
   redis-cli -u $REDIS_URL INFO stats | grep hit_rate
   ```

4. **Actions**:
   - Enable Redis caching if not already enabled
   - Add database indexes on slow queries
   - Increase worker processes
   - Optimize queries

### High Error Rates

1. **Check error logs**:
   ```bash
   railway logs | grep ERROR | tail -50
   ```

2. **Check error patterns**:
   ```bash
   railway logs | grep ERROR | cut -d' ' -f5- | sort | uniq -c | sort -rn
   ```

3. **Common causes**:
   - Database connection timeout
   - External API failures (Ministry of Land API)
   - Invalid input validation
   - Memory exhaustion

4. **Actions**:
   - Restart services
   - Check database connectivity
   - Verify API keys
   - Scale up resources

### Memory Issues

1. **Check memory usage**:
   ```bash
   # Railway
   railway run free -h

   # Docker
   docker stats
   ```

2. **Check memory leaks**:
   ```bash
   # Monitor over time
   watch -n 60 "railway run ps aux --sort=-%mem | head -10"
   ```

3. **Actions**:
   - Restart services
   - Increase memory allocation
   - Check for memory leaks in code
   - Reduce worker processes

### Database Connection Issues

1. **Check connection pool**:
   ```sql
   SELECT count(*), state
   FROM pg_stat_activity
   WHERE datname = 'apt_insights'
   GROUP BY state;
   ```

2. **Check max connections**:
   ```sql
   SHOW max_connections;
   SELECT count(*) FROM pg_stat_activity;
   ```

3. **Actions**:
   - Increase connection pool size
   - Check for connection leaks
   - Increase `max_connections` in PostgreSQL config
   - Add connection timeout configuration

---

## Monitoring Checklist

### Daily

- [ ] Check service health status
- [ ] Review error logs
- [ ] Monitor API response times
- [ ] Check disk space usage

### Weekly

- [ ] Review performance trends
- [ ] Analyze slow queries
- [ ] Check backup completion
- [ ] Review cache hit rates

### Monthly

- [ ] Capacity planning review
- [ ] Cost optimization analysis
- [ ] Security audit
- [ ] Performance optimization review

---

**Last Updated**: 2026-02-07
