# Production Ready Guide

Complete production deployment reference for the Korean Apartment Transaction Analysis Platform.

## Quick Links

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) | Pre-deployment checklist | Before every deployment |
| [RUNBOOK.md](RUNBOOK.md) | Operational procedures | Daily operations & incidents |
| [DISASTER_RECOVERY.md](DISASTER_RECOVERY.md) | Backup & recovery | Disaster scenarios |
| [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) | Security audit | Pre-production & quarterly |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Deployment guide | Detailed deployment steps |
| [MONITORING.md](MONITORING.md) | Observability setup | Setting up monitoring |

---

## Pre-Deployment Quick Check

Run this checklist 24 hours before deployment:

```bash
# 1. All tests passing
cd fastapi-backend && pytest -v
cd nextjs-frontend && npm test

# 2. No security vulnerabilities
safety check -r fastapi-backend/requirements.txt
cd nextjs-frontend && npm audit

# 3. No secrets in code
git grep -E 'api[_-]?key|secret|password|token' --ignore-case

# 4. Environment variables configured
railway variables list
vercel env ls

# 5. Database backup exists
ls -lh backups/ | tail -5

# 6. Health endpoints working
curl https://api.your-domain.com/health
curl https://your-domain.com/api/health

# 7. Monitoring configured
curl https://api.your-domain.com/api/metrics | grep http_request

# All checks passed? ✅ Ready to deploy!
```

---

## Deployment Workflow

### Standard Deployment (Non-Emergency)

```bash
# 1. Complete pre-deployment checklist
# See PRODUCTION_CHECKLIST.md

# 2. Create deployment branch
git checkout -b deployment/v1.1.0

# 3. Run automated deployment
./scripts/deploy.sh all production

# 4. Monitor deployment
railway logs -f

# 5. Verify deployment
./scripts/smoke-test.sh production

# 6. Update documentation
git tag v1.1.0
git push origin v1.1.0
```

### Emergency Hotfix Deployment

```bash
# 1. Create hotfix branch
git checkout -b hotfix/critical-bug

# 2. Fix and test
# ... make changes ...
pytest -v

# 3. Deploy directly
git commit -m "fix: critical security issue"
git push origin hotfix/critical-bug
./scripts/deploy.sh backend production

# 4. Verify fix
./scripts/smoke-test.sh production

# 5. Merge to main
git checkout main
git merge hotfix/critical-bug
git push origin main
```

### Rollback Procedure

```bash
# When to rollback:
# - Error rate > 5% for 5 minutes
# - Critical functionality broken
# - Security incident detected

# Execute rollback
./scripts/rollback.sh v1.0.0

# Monitor recovery
railway logs -f | grep ERROR

# Verify system
./scripts/smoke-test.sh production

# Document incident
# See RUNBOOK.md - Incident Response
```

---

## Common Operations

### View Logs

```bash
# Backend logs (Railway)
railway logs -f

# Filter errors only
railway logs | grep ERROR

# Last 100 lines
railway logs --lines 100

# Specific time range
railway logs --since 1h
```

### Check Health

```bash
# All services
./scripts/check-all-health.sh production

# Individual services
curl https://api.your-domain.com/health | jq
curl https://your-domain.com/api/health | jq
```

### Database Operations

```bash
# Connect to database
railway run psql $DATABASE_URL

# Backup database
./scripts/backup-database.sh production

# Restore database (CAREFUL!)
./scripts/restore-database.sh backups/production-YYYYMMDD.sql.gz

# Run migrations
cd fastapi-backend && railway run alembic upgrade head

# Check migration status
railway run alembic current
```

### Cache Operations

```bash
# Clear Redis cache
redis-cli -h <host> -a <password> FLUSHDB

# Warm cache
python fastapi-backend/cache/cache_warming.py

# Check cache stats
redis-cli INFO stats | grep keyspace
```

### Performance Monitoring

```bash
# Check metrics
curl https://api.your-domain.com/api/metrics | grep http_request_duration

# Run performance test
python scripts/performance_check.py

# Run full benchmark
python scripts/benchmark.py

# Load testing
cd tests/load && locust -f locustfile.py
```

---

## Incident Response

### Severity Levels

| Level | Response Time | Example |
|-------|--------------|---------|
| **P0 - Critical** | Immediate | Complete outage |
| **P1 - High** | < 15 min | API errors > 10% |
| **P2 - Medium** | < 1 hour | Slow response times |
| **P3 - Low** | < 4 hours | UI glitches |

### Response Process

1. **Detect**: Monitoring alerts, user reports
2. **Assess**: Determine severity and impact
3. **Communicate**: Notify team and stakeholders
4. **Mitigate**: Apply immediate fix or rollback
5. **Resolve**: Implement permanent fix
6. **Document**: Create incident report

### Quick Diagnostic

```bash
#!/bin/bash
# Quick diagnostic for incidents

echo "=== Quick Diagnostic ==="
echo "Time: $(date)"
echo ""

echo "Backend Health:"
curl -s https://api.your-domain.com/health | jq .
echo ""

echo "Frontend Health:"
curl -s https://your-domain.com/api/health | jq .
echo ""

echo "Recent Errors:"
railway logs --lines 50 | grep ERROR
echo ""

echo "Resource Usage:"
railway status
echo ""

echo "Error Rate:"
curl -s https://api.your-domain.com/api/metrics | \
  grep 'http_requests_total.*5[0-9][0-9]'
```

### Escalation Path

1. On-Call Engineer (immediate)
2. Technical Lead (if not resolved in 15 min)
3. DevOps Lead (if infrastructure issue)
4. Engineering Manager (if critical, > 1 hour)

---

## Monitoring & Alerts

### Key Metrics to Monitor

| Metric | Target | Critical |
|--------|--------|----------|
| Response Time (p95) | < 200ms | > 500ms |
| Error Rate | < 0.1% | > 1% |
| Uptime | > 99.9% | < 99% |
| CPU Usage | < 70% | > 90% |
| Memory Usage | < 80% | > 90% |
| Database Connections | < 80% max | > 95% max |
| Cache Hit Rate | > 80% | < 50% |

### Alert Configuration

Configure alerts for:
- ❗ Response time > 500ms (p95)
- ❗ Error rate > 1%
- ❗ Service down (health check fails)
- ❗ CPU usage > 90%
- ❗ Memory usage > 90%
- ⚠️  Response time > 200ms (p95)
- ⚠️  Error rate > 0.5%
- ⚠️  Cache hit rate < 70%

### Monitoring Dashboards

1. **Application Dashboard**
   - Request rate
   - Response times
   - Error rates
   - Active users

2. **Infrastructure Dashboard**
   - CPU/Memory usage
   - Disk usage
   - Network I/O
   - Database metrics

3. **Business Metrics**
   - User registrations
   - API usage by endpoint
   - Premium conversions
   - Feature adoption

---

## Security Operations

### Regular Security Tasks

#### Daily
```bash
# Check for suspicious activity
railway logs | grep -i "unauthorized\|forbidden\|failed.*login"

# Verify SSL certificate
echo | openssl s_client -connect your-domain.com:443 2>/dev/null | \
  openssl x509 -noout -dates
```

#### Weekly
```bash
# Scan dependencies
safety check -r fastapi-backend/requirements.txt
cd nextjs-frontend && npm audit

# Review access logs
railway logs --since 7d | grep -E "POST|PUT|DELETE" | head -50
```

#### Monthly
```bash
# Full security scan
bandit -r fastapi-backend/ -ll
trivy image apt-insights-backend:latest

# Update dependencies
pip install -U -r requirements.txt
cd nextjs-frontend && npm update
```

### Security Incident Response

If security incident detected:

1. **Isolate** affected systems
2. **Notify** security lead immediately
3. **Preserve** logs and evidence
4. **Investigate** scope and impact
5. **Remediate** vulnerability
6. **Rotate** all credentials
7. **Document** incident
8. **Post-mortem** within 48 hours

---

## Maintenance Windows

### Scheduled Maintenance

```bash
# 1. Announce maintenance (24 hours notice)
# Email/status page notification

# 2. Create backup
./scripts/backup-database.sh production

# 3. Enable maintenance mode (if available)
# vercel --prod --env MAINTENANCE_MODE=true

# 4. Perform maintenance
# Database upgrades, migrations, etc.

# 5. Verify functionality
./scripts/smoke-test.sh production

# 6. Disable maintenance mode
# vercel --prod --env MAINTENANCE_MODE=false

# 7. Monitor for issues
railway logs -f
```

### Preferred Maintenance Windows

- **Primary**: Sunday 2:00 AM - 4:00 AM UTC
- **Secondary**: Tuesday 2:00 AM - 4:00 AM UTC
- **Emergency**: Anytime (with notification)

---

## Performance Optimization

### Optimization Checklist

```bash
# 1. Analyze slow queries
python fastapi-backend/db/query_optimizer.py analyze

# 2. Optimize indexes
python fastapi-backend/db/query_optimizer.py optimize

# 3. Warm cache
python fastapi-backend/cache/cache_warming.py

# 4. Run performance benchmark
python scripts/benchmark.py

# 5. Verify improvements
./scripts/performance_check.py
```

### Performance Targets

| Component | Metric | Target |
|-----------|--------|--------|
| API | p50 response time | < 50ms |
| API | p95 response time | < 200ms |
| API | p99 response time | < 500ms |
| Frontend | First Contentful Paint | < 1.5s |
| Frontend | Time to Interactive | < 3s |
| Database | Query time (p95) | < 100ms |
| Cache | Hit rate | > 80% |

---

## Backup & Recovery

### Backup Schedule

| Type | Frequency | Retention | Location |
|------|-----------|-----------|----------|
| Database Full | Daily | 30 days | Railway + S3 |
| Database WAL | Continuous | 7 days | Railway |
| Application Code | On commit | Indefinite | GitHub |
| Configuration | Weekly | 90 days | Encrypted file |
| Redis Snapshots | Daily | 7 days | Railway |

### Recovery Procedures

#### Database Recovery
```bash
# 1. Identify backup
ls -lh backups/ | tail -10

# 2. Restore database
./scripts/restore-database.sh backups/production-YYYYMMDD.sql.gz

# 3. Verify restoration
railway run psql $DATABASE_URL -c "SELECT COUNT(*) FROM apartments;"

# 4. Run migrations
cd fastapi-backend && railway run alembic upgrade head
```

#### Full System Recovery
See [DISASTER_RECOVERY.md](DISASTER_RECOVERY.md) for complete procedures.

---

## Cost Optimization

### Monthly Cost Targets

| Service | Estimated Cost | Optimization |
|---------|---------------|--------------|
| Railway (Backend) | $20-50/mo | Scale down unused environments |
| Railway (Database) | $10-30/mo | Optimize queries, add indexes |
| Railway (Redis) | $5-15/mo | Adjust memory limits |
| Vercel (Frontend) | $0-20/mo | Optimize build times |
| Sentry | $0-26/mo | Adjust error sampling rate |
| **Total** | **$35-141/mo** | |

### Optimization Tips

1. **Database**: Optimize slow queries, add proper indexes
2. **Redis**: Adjust TTL values, implement cache invalidation
3. **Frontend**: Optimize images, enable compression
4. **Backend**: Use connection pooling, async operations
5. **Monitoring**: Adjust log retention, error sampling rates

---

## Team Contacts

### Roles & Responsibilities

| Role | Name | Contact | Responsibility |
|------|------|---------|----------------|
| **Technical Lead** | _______ | _______ | Overall technical decisions |
| **DevOps Lead** | _______ | _______ | Infrastructure & deployments |
| **Backend Developer** | _______ | _______ | API & database |
| **Frontend Developer** | _______ | _______ | UI/UX & client-side |
| **Security Lead** | _______ | _______ | Security audits & incidents |
| **On-Call Engineer** | _______ | _______ | Emergency response (24/7) |

### Escalation Contacts

**Technical Issues**: _____________ (Primary)
**Infrastructure Issues**: _____________ (Primary)
**Security Incidents**: _____________ (Primary)
**Business Continuity**: _____________ (Manager)

### External Support

| Service | Support Contact | Status Page |
|---------|----------------|-------------|
| Railway | support@railway.app | https://status.railway.app |
| Vercel | support@vercel.com | https://www.vercel-status.com |
| Sentry | support@sentry.io | https://status.sentry.io |
| Ministry of Land API | _______ | https://www.data.go.kr/ |

---

## Useful Commands Reference

```bash
# ===== Deployment =====
./scripts/deploy.sh all production          # Full deployment
./scripts/deploy.sh backend production      # Backend only
./scripts/deploy.sh frontend production     # Frontend only
./scripts/rollback.sh v1.0.0               # Rollback to version

# ===== Health Checks =====
./scripts/check-all-health.sh production   # Check all services
curl https://api.your-domain.com/health    # Backend health
curl https://your-domain.com/api/health    # Frontend health

# ===== Logs =====
railway logs -f                            # Stream backend logs
railway logs | grep ERROR                  # Filter errors
vercel logs <deployment-url>              # Frontend logs

# ===== Database =====
railway run psql $DATABASE_URL             # Connect to DB
./scripts/backup-database.sh production    # Backup
./scripts/restore-database.sh <file>       # Restore
railway run alembic upgrade head           # Run migrations
railway run alembic current                # Check version

# ===== Cache =====
redis-cli -h <host> -a <pass> FLUSHDB     # Clear cache
python cache/cache_warming.py              # Warm cache
redis-cli INFO stats                       # Cache stats

# ===== Monitoring =====
curl https://api.your-domain.com/api/metrics | grep http_request  # Metrics
python scripts/performance_check.py        # Performance check
python scripts/benchmark.py                # Full benchmark

# ===== Security =====
safety check -r requirements.txt           # Check vulnerabilities
npm audit                                  # Node.js audit
bandit -r fastapi-backend/ -ll            # Security scan
git secrets --scan-history                # Scan for secrets
```

---

## Additional Resources

### Documentation
- [API Documentation](https://api.your-domain.com/docs) - OpenAPI/Swagger docs
- [CLAUDE.md](CLAUDE.md) - Development guide
- [README.md](README.md) - Project overview

### Monitoring
- [Railway Dashboard](https://railway.app) - Infrastructure monitoring
- [Vercel Dashboard](https://vercel.com) - Frontend deployment
- [Sentry Dashboard](https://sentry.io) - Error tracking
- [Uptime Monitor](https://uptimerobot.com) - Availability monitoring

### External Resources
- [Railway Documentation](https://docs.railway.app)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

### Training Materials
- [Incident Response Training](docs/training/incident-response.md)
- [Deployment Training](docs/training/deployment.md)
- [Security Training](docs/training/security.md)
- [On-Call Guide](docs/training/on-call.md)

---

## Changelog

### Version 1.0.0 (2026-02-08)

- Initial production-ready documentation
- Deployment and rollback scripts
- Comprehensive runbook
- Disaster recovery procedures
- Security checklist
- Monitoring and alerting setup

---

## Next Steps

### Before First Production Deployment

- [ ] Review all documentation
- [ ] Complete security audit
- [ ] Configure monitoring and alerts
- [ ] Test backup and restore procedures
- [ ] Conduct disaster recovery drill
- [ ] Train team on operational procedures
- [ ] Set up on-call rotation
- [ ] Establish communication channels

### After First Deployment

- [ ] Monitor closely for 48 hours
- [ ] Gather user feedback
- [ ] Optimize based on metrics
- [ ] Update documentation with learnings
- [ ] Schedule regular reviews

### Ongoing

- [ ] Weekly performance reviews
- [ ] Monthly security audits
- [ ] Quarterly disaster recovery drills
- [ ] Regular team training
- [ ] Continuous documentation updates

---

**Document Version**: 1.0.0
**Last Updated**: 2026-02-08
**Next Review**: 2026-03-08

**Maintained By**: DevOps Team
**Contact**: devops@company.com

---

## Quick Decision Tree

```
Is production down?
├─ Yes → See RUNBOOK.md "Emergency Procedures"
└─ No
    │
    Need to deploy?
    ├─ Yes
    │   ├─ Emergency? → See RUNBOOK.md "Emergency Hotfix"
    │   └─ Regular → See PRODUCTION_CHECKLIST.md
    │
    └─ No
        │
        Need to rollback?
        ├─ Yes → ./scripts/rollback.sh <version>
        └─ No
            │
            Security incident?
            ├─ Yes → See SECURITY_CHECKLIST.md "Incident Response"
            └─ No
                │
                Data loss?
                ├─ Yes → See DISASTER_RECOVERY.md
                └─ No → See RUNBOOK.md "Common Operations"
```

---

**Ready for Production? ✅**

You now have all the documentation and tools needed for production operations.

Good luck! 🚀
