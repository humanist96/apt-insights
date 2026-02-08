# Production Runbook

Operational procedures for the Korean Apartment Transaction Analysis Platform.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Common Operations](#common-operations)
- [Incident Response](#incident-response)
- [Troubleshooting](#troubleshooting)
- [Maintenance Tasks](#maintenance-tasks)
- [Scaling Procedures](#scaling-procedures)
- [Emergency Procedures](#emergency-procedures)
- [Contact Information](#contact-information)

---

## Quick Reference

### Service URLs

| Service | URL | Health Check |
|---------|-----|--------------|
| Frontend | https://your-domain.com | https://your-domain.com/api/health |
| Backend API | https://api.your-domain.com | https://api.your-domain.com/health |
| API Docs | https://api.your-domain.com/docs | N/A |
| Metrics | https://api.your-domain.com/api/metrics | N/A |

### Quick Health Check

```bash
# Check all services
./scripts/check-all-health.sh production

# Individual checks
curl https://your-domain.com/api/health
curl https://api.your-domain.com/health
```

### Emergency Commands

```bash
# View logs
railway logs -f

# Restart backend
railway restart

# Rollback deployment
./scripts/rollback.sh v1.0.0

# Database backup
./scripts/backup-database.sh production

# Clear Redis cache
redis-cli -h <host> -p <port> -a <password> FLUSHDB
```

---

## Common Operations

### 1. Viewing Logs

#### Backend Logs (Railway)

```bash
# Stream live logs
railway logs -f

# Last 100 lines
railway logs --lines 100

# Filter by keyword
railway logs | grep ERROR

# View specific time range
railway logs --since 1h
```

#### Frontend Logs (Vercel)

```bash
# Via CLI
vercel logs <deployment-url>

# Via Dashboard
# Visit: https://vercel.com/<org>/<project>/deployments
```

#### Application Logs

```bash
# Backend structured logs (JSON format)
railway logs -f | jq '.level, .message, .error'

# Filter by severity
railway logs | grep '"level":"error"'
```

### 2. Checking Service Status

#### All Services

```bash
#!/bin/bash
# check-all-health.sh

echo "Checking Frontend..."
curl -sf https://your-domain.com/api/health || echo "FAILED"

echo "Checking Backend..."
curl -sf https://api.your-domain.com/health || echo "FAILED"

echo "Checking Database..."
railway run psql $DATABASE_URL -c "SELECT 1;" || echo "FAILED"

echo "Checking Redis..."
redis-cli -h <host> -a <password> PING || echo "FAILED"
```

#### Individual Service Status

```bash
# Backend health
curl https://api.your-domain.com/health | jq

# Expected response:
{
  "status": "healthy",
  "service": "apartment-transaction-analysis-api",
  "version": "1.0.0",
  "timestamp": "2026-02-08T12:00:00.000Z"
}

# Frontend health
curl https://your-domain.com/api/health | jq

# Database connection test
railway run psql $DATABASE_URL -c "SELECT version();"

# Redis ping
redis-cli -h <host> -a <password> PING
# Expected: PONG
```

### 3. Restarting Services

#### Backend (Railway)

```bash
# Restart via Railway CLI
railway restart

# Or via dashboard
# Visit: https://railway.app/project/<project-id>
# Click "Restart" button
```

#### Frontend (Vercel)

```bash
# Redeploy latest version
vercel --prod

# Or via dashboard
# Visit: https://vercel.com/<org>/<project>
# Click "Redeploy"
```

### 4. Database Operations

#### Connecting to Database

```bash
# Via Railway CLI
railway run psql $DATABASE_URL

# Direct connection
psql "postgresql://user:password@host:port/database?sslmode=require"
```

#### Common Queries

```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('apt_insights'));

-- Check table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check active connections
SELECT count(*) FROM pg_stat_activity;

-- Check slow queries
SELECT pid, age(clock_timestamp(), query_start), usename, query
FROM pg_stat_activity
WHERE query != '<IDLE>' AND query NOT ILIKE '%pg_stat_activity%'
ORDER BY query_start ASC;

-- Check index usage
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

#### Database Maintenance

```bash
# Vacuum analyze (regular maintenance)
railway run psql $DATABASE_URL -c "VACUUM ANALYZE;"

# Reindex (if needed)
railway run psql $DATABASE_URL -c "REINDEX DATABASE apt_insights;"

# Check for bloat
railway run psql $DATABASE_URL -f scripts/check-bloat.sql
```

### 5. Cache Operations

#### Connecting to Redis

```bash
# Via Railway (if Redis plugin)
railway run redis-cli -h <host> -p <port> -a <password>

# Direct connection
redis-cli -h <host> -p <port> -a <password>
```

#### Common Redis Commands

```bash
# Check Redis info
redis-cli INFO

# Check memory usage
redis-cli INFO memory

# Check cache stats
redis-cli INFO stats

# View all keys (careful in production!)
redis-cli KEYS "*" | head -20

# Get cache hit rate
redis-cli INFO stats | grep keyspace

# Clear specific pattern
redis-cli KEYS "apartment:*" | xargs redis-cli DEL

# Clear all cache (DANGEROUS!)
redis-cli FLUSHDB

# Warm cache
python fastapi-backend/cache/cache_warming.py
```

### 6. Monitoring Metrics

#### Prometheus Metrics

```bash
# Get all metrics
curl https://api.your-domain.com/api/metrics

# Filter specific metrics
curl https://api.your-domain.com/api/metrics | grep http_request_duration

# Response time percentiles
curl https://api.your-domain.com/api/metrics | grep -E 'quantile="0\.(5|95|99)"'
```

#### Application Metrics

```bash
# Request rate
curl https://api.your-domain.com/api/metrics | grep http_requests_total

# Error rate
curl https://api.your-domain.com/api/metrics | grep http_requests_total | grep 'code="5'

# Cache hit rate
redis-cli INFO stats | grep keyspace_hits
redis-cli INFO stats | grep keyspace_misses
```

### 7. Deployment Operations

#### Deploy New Version

```bash
# Tag release
git tag v1.1.0
git push origin v1.1.0

# GitHub Actions will automatically deploy

# Or manual deployment
./scripts/deploy.sh all production
```

#### Check Deployment Status

```bash
# Backend (Railway)
railway status

# Frontend (Vercel)
vercel ls
```

---

## Incident Response

### Severity Levels

| Level | Description | Response Time | Examples |
|-------|-------------|---------------|----------|
| **P0 - Critical** | Service completely down | Immediate | Complete outage, data loss |
| **P1 - High** | Major functionality broken | < 15 min | Login broken, API errors > 10% |
| **P2 - Medium** | Degraded performance | < 1 hour | Slow response times, some features down |
| **P3 - Low** | Minor issues | < 4 hours | UI glitches, non-critical bugs |

### Incident Response Process

#### 1. Detection

Monitor for:
- Health check failures
- High error rates (> 1%)
- Slow response times (> 500ms p95)
- High resource usage (> 90%)
- Failed deployments
- User reports

#### 2. Assessment

```bash
# Quick diagnostic script
#!/bin/bash
echo "=== INCIDENT DIAGNOSTIC ==="
echo "Time: $(date)"
echo ""

echo "Frontend Health:"
curl -s https://your-domain.com/api/health | jq . || echo "FAILED"
echo ""

echo "Backend Health:"
curl -s https://api.your-domain.com/health | jq . || echo "FAILED"
echo ""

echo "Recent Errors:"
railway logs --lines 50 | grep ERROR
echo ""

echo "Resource Usage:"
railway status
echo ""

echo "Database Connections:"
railway run psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"
```

#### 3. Communication

```bash
# Post status update
# Use status page or:
echo "Investigating service disruption at $(date)" > status.txt

# Notify team
# Send message to Slack/Discord/Teams
```

#### 4. Mitigation

See **Troubleshooting** section below for specific scenarios.

#### 5. Resolution

```bash
# Document incident
cat > incidents/incident-$(date +%Y%m%d-%H%M%S).md <<EOF
# Incident Report

**Date**: $(date)
**Severity**: P0/P1/P2/P3
**Duration**: X minutes
**Impact**: Description

## Timeline
- HH:MM - Incident detected
- HH:MM - Investigation started
- HH:MM - Root cause identified
- HH:MM - Fix deployed
- HH:MM - Service restored

## Root Cause
Description

## Resolution
Steps taken

## Prevention
Action items

## Lessons Learned
Key takeaways
EOF
```

### Escalation Path

1. **On-Call Engineer** (immediate)
2. **Technical Lead** (if not resolved in 15 min)
3. **DevOps Lead** (if infrastructure related)
4. **CTO/Engineering Manager** (if critical, ongoing > 1 hour)

---

## Troubleshooting

### Scenario 1: High Error Rate

**Symptoms**: Error rate > 1%, many 5xx responses

**Diagnosis**:
```bash
# Check recent errors
railway logs | grep ERROR | tail -50

# Check error rate
curl https://api.your-domain.com/api/metrics | grep 'http_requests_total.*5'

# Check resource usage
railway status
```

**Common Causes**:
- Database connection pool exhausted
- External API timeout (Ministry of Land API)
- Memory leak
- Unhandled exception in code

**Resolution**:
```bash
# Quick fix: Restart service
railway restart

# Check database connections
railway run psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"

# If too many connections:
railway run psql $DATABASE_URL -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle' AND state_change < NOW() - INTERVAL '5 minutes';"

# Monitor recovery
watch -n 5 'curl -s https://api.your-domain.com/health | jq .status'
```

### Scenario 2: Slow Response Times

**Symptoms**: Response time > 500ms (p95)

**Diagnosis**:
```bash
# Check response times
curl https://api.your-domain.com/api/metrics | grep http_request_duration

# Check database performance
railway run psql $DATABASE_URL -c "
SELECT query, calls, total_time, mean_time, max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;"

# Check cache hit rate
redis-cli INFO stats | grep keyspace
```

**Common Causes**:
- Slow database queries
- Missing database indexes
- Low cache hit rate
- High CPU/memory usage

**Resolution**:
```bash
# Optimize slow queries
python fastapi-backend/db/query_optimizer.py analyze

# Warm cache
python fastapi-backend/cache/cache_warming.py

# Add missing indexes (after analysis)
railway run psql $DATABASE_URL -c "CREATE INDEX CONCURRENTLY idx_name ON table(column);"

# Scale up resources (if needed)
# Via Railway dashboard: Settings > Resources
```

### Scenario 3: Database Connection Issues

**Symptoms**: "Too many connections", "Connection refused"

**Diagnosis**:
```bash
# Check connection count
railway run psql $DATABASE_URL -c "
SELECT count(*) as connections,
       state,
       application_name
FROM pg_stat_activity
GROUP BY state, application_name
ORDER BY count(*) DESC;"

# Check connection limits
railway run psql $DATABASE_URL -c "SHOW max_connections;"
```

**Resolution**:
```bash
# Kill idle connections
railway run psql $DATABASE_URL -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND state_change < NOW() - INTERVAL '10 minutes'
AND pid != pg_backend_pid();"

# Adjust connection pool in application
# Edit: fastapi-backend/.env
# DATABASE_URL=...?pool_size=10&max_overflow=5

# Restart application
railway restart
```

### Scenario 4: Redis Connection Issues

**Symptoms**: "Connection refused", "Timeout", cache misses

**Diagnosis**:
```bash
# Test connection
redis-cli -h <host> -a <password> PING

# Check memory usage
redis-cli INFO memory | grep used_memory

# Check eviction stats
redis-cli INFO stats | grep evicted_keys
```

**Resolution**:
```bash
# Restart Redis (if plugin)
railway restart redis

# Clear cache if corrupted
redis-cli FLUSHDB

# Warm cache again
python fastapi-backend/cache/cache_warming.py

# Increase memory limit (if needed)
# Via Railway dashboard: Redis plugin > Settings
```

### Scenario 5: Deployment Failure

**Symptoms**: Build fails, deployment doesn't start, health checks fail

**Diagnosis**:
```bash
# Check GitHub Actions
gh run list --limit 5
gh run view <run-id> --log-failed

# Check Railway build logs
railway logs --deployment <deployment-id>

# Check health after deployment
curl https://api.your-domain.com/health
```

**Common Causes**:
- Build errors (dependency issues)
- Environment variables missing
- Database migration failure
- Health check timeout

**Resolution**:
```bash
# Rollback to previous version
./scripts/rollback.sh <previous-version>

# Fix issues locally
# Test build:
docker build -t test ./fastapi-backend

# Fix and redeploy
git commit -m "fix: deployment issue"
git push origin main
```

### Scenario 6: Memory Leak

**Symptoms**: Memory usage increasing over time, OOM errors

**Diagnosis**:
```bash
# Check memory usage over time
railway logs | grep "memory"

# Monitor current usage
railway status

# Check for memory leaks in code
# Use memory profiler locally
```

**Resolution**:
```bash
# Immediate: Restart service
railway restart

# Long-term: Profile and fix code
# Use memory_profiler locally:
# pip install memory_profiler
# python -m memory_profiler fastapi-backend/main.py

# Increase memory limit (temporary)
# Via Railway dashboard: Settings > Resources
```

### Scenario 7: External API Failures

**Symptoms**: Timeouts, errors from Ministry of Land API

**Diagnosis**:
```bash
# Check logs for API errors
railway logs | grep "Ministry of Land API"

# Test API directly
curl "https://api.data.go.kr/..."

# Check API status
# Visit: https://www.data.go.kr/
```

**Resolution**:
```bash
# Implement fallback/retry logic (if not present)
# Increase timeout values
# Use cached data if available

# If API is down, consider:
# - Maintenance mode
# - Cached data only mode
# - Status message to users
```

---

## Maintenance Tasks

### Daily Tasks

```bash
# Check error logs
railway logs | grep ERROR | tail -50

# Verify backups completed
./scripts/verify-backups.sh

# Check disk usage
railway run df -h

# Monitor key metrics
curl https://api.your-domain.com/api/metrics | grep -E 'http_request_duration|http_requests_total'
```

### Weekly Tasks

```bash
# Database maintenance
railway run psql $DATABASE_URL -c "VACUUM ANALYZE;"

# Review slow queries
python fastapi-backend/db/query_optimizer.py analyze

# Check dependency updates
cd fastapi-backend && pip list --outdated
cd nextjs-frontend && npm outdated

# Review error patterns
railway logs --since 7d | grep ERROR | sort | uniq -c | sort -rn | head -20

# Security scan
safety check -r requirements.txt
npm audit
```

### Monthly Tasks

```bash
# Rotate secrets (if required)
./scripts/generate-secret-key.sh
# Update in Railway/Vercel dashboard

# Review and optimize indexes
python fastapi-backend/db/query_optimizer.py optimize

# Capacity planning review
./scripts/analyze-capacity.sh

# Update dependencies
pip install -U -r requirements.txt
npm update

# Test disaster recovery
./scripts/test-disaster-recovery.sh
```

### Quarterly Tasks

```bash
# Security audit
./scripts/security-audit.sh

# Performance review
./scripts/performance-review.sh

# Disaster recovery drill
./scripts/disaster-recovery-drill.sh

# Cost optimization review
./scripts/analyze-costs.sh

# Documentation update
# Review and update all operational docs
```

---

## Scaling Procedures

### Vertical Scaling (Scale Up)

#### Backend (Railway)

```bash
# Via Railway Dashboard:
# 1. Go to project > fastapi-backend service
# 2. Settings > Resources
# 3. Adjust CPU/Memory/Disk
# 4. Click "Save" (will trigger restart)

# Monitor after scaling
watch -n 5 'railway status'
```

#### Database (Railway)

```bash
# Via Railway Dashboard:
# 1. Go to PostgreSQL plugin
# 2. Settings > Plan
# 3. Select larger plan
# 4. Confirm change

# No downtime for most plan changes
```

### Horizontal Scaling (Scale Out)

#### Backend (Add Workers)

Edit `fastapi-backend/Dockerfile`:
```dockerfile
# Change from:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# To:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8"]
```

Redeploy:
```bash
git commit -m "scale: increase workers to 8"
git push origin main
```

#### Frontend (Automatic via Vercel)

Vercel automatically handles frontend scaling.

### Auto-Scaling

Railway supports auto-scaling via:
1. Resource limits with auto-restart
2. Horizontal pod autoscaling (enterprise plans)

Configure in Railway dashboard:
- Settings > Resources > Auto-scaling

---

## Emergency Procedures

### Emergency Rollback

**When to use**: Critical bug in production, service down, data corruption risk

**Process**:
```bash
# 1. Identify last known good version
git tag --sort=-v:refname | head -5

# 2. Execute rollback script
./scripts/rollback.sh v1.0.0

# 3. Verify health
curl https://api.your-domain.com/health

# 4. Monitor for errors
railway logs -f | grep ERROR

# 5. Notify stakeholders
echo "Emergency rollback to v1.0.0 completed at $(date)" | \
  mail -s "ALERT: Production Rollback" team@company.com
```

### Database Rollback

**When to use**: Failed migration, data corruption

**Process**:
```bash
# 1. Stop application
railway restart --stop

# 2. Restore from backup
./scripts/restore-database.sh backups/production-YYYYMMDD-HHMMSS.sql

# 3. Verify data integrity
railway run psql $DATABASE_URL -c "SELECT COUNT(*) FROM apartments;"

# 4. Restart application
railway restart

# 5. Monitor
railway logs -f
```

### Complete Service Restart

**When to use**: All troubleshooting failed, cascading failures

**Process**:
```bash
# 1. Notify users (maintenance mode)
# Update status page

# 2. Backup everything
./scripts/backup-all.sh

# 3. Restart all services
railway restart --all

# 4. Wait for services to be healthy
sleep 60
./scripts/check-all-health.sh production

# 5. Monitor recovery
railway logs -f

# 6. Verify functionality
./scripts/smoke-test.sh production
```

### Data Recovery

See **DISASTER_RECOVERY.md** for detailed procedures.

---

## Contact Information

### On-Call Rotation

| Week | Primary | Secondary | Manager |
|------|---------|-----------|---------|
| Current | _______ | _________ | _______ |

### Escalation Contacts

| Role | Name | Phone | Email | Availability |
|------|------|-------|-------|--------------|
| On-Call Engineer | _______ | _______ | _______ | 24/7 |
| Technical Lead | _______ | _______ | _______ | 9am-9pm |
| DevOps Lead | _______ | _______ | _______ | 9am-9pm |
| Engineering Manager | _______ | _______ | _______ | 9am-6pm |

### External Contacts

| Service | Support | Status Page |
|---------|---------|-------------|
| Railway | support@railway.app | https://status.railway.app |
| Vercel | support@vercel.com | https://www.vercel-status.com |
| Sentry | support@sentry.io | https://status.sentry.io |
| Ministry of Land API | _______ | https://www.data.go.kr/ |

### Emergency Hotlines

- **Technical Issues**: _____________
- **Security Incidents**: _____________
- **Data Loss**: _____________

---

## Appendix

### Useful Commands Reference

```bash
# Quick diagnostics
./scripts/quick-diag.sh

# Full health check
./scripts/check-all-health.sh production

# Deploy
./scripts/deploy.sh all production

# Rollback
./scripts/rollback.sh <version>

# Backup
./scripts/backup-database.sh production

# Restore
./scripts/restore-database.sh <backup-file>

# View metrics
curl https://api.your-domain.com/api/metrics | grep <metric>

# Clear cache
redis-cli FLUSHDB

# Warm cache
python fastapi-backend/cache/cache_warming.py

# Database maintenance
railway run psql $DATABASE_URL -c "VACUUM ANALYZE;"

# View slow queries
python fastapi-backend/db/query_optimizer.py analyze
```

### Performance Targets

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Response Time (p50) | < 50ms | > 100ms | > 200ms |
| Response Time (p95) | < 200ms | > 400ms | > 500ms |
| Response Time (p99) | < 500ms | > 1s | > 2s |
| Error Rate | < 0.1% | > 0.5% | > 1% |
| Uptime | > 99.9% | < 99.5% | < 99% |
| Cache Hit Rate | > 80% | < 70% | < 50% |
| Database Query Time (p95) | < 100ms | > 200ms | > 300ms |
| CPU Usage | < 70% | > 80% | > 90% |
| Memory Usage | < 80% | > 85% | > 90% |

---

**Last Updated**: 2026-02-08
**Document Version**: 1.0.0
**Next Review**: 2026-03-08
