# Disaster Recovery Plan

Comprehensive disaster recovery procedures for the Korean Apartment Transaction Analysis Platform.

## Table of Contents

- [Overview](#overview)
- [Backup Strategy](#backup-strategy)
- [Recovery Procedures](#recovery-procedures)
- [Testing & Validation](#testing--validation)
- [Recovery Scenarios](#recovery-scenarios)
- [Failover Procedures](#failover-procedures)
- [Data Loss Prevention](#data-loss-prevention)

---

## Overview

### Recovery Objectives

| Metric | Target | Maximum Acceptable |
|--------|--------|-------------------|
| **RTO** (Recovery Time Objective) | 1 hour | 4 hours |
| **RPO** (Recovery Point Objective) | 15 minutes | 1 hour |
| **Data Loss Tolerance** | 0 records | < 100 records |
| **Downtime per Month** | < 44 minutes | < 4 hours |
| **Availability** | 99.9% | 99.5% |

### Disaster Categories

| Category | Examples | Impact | Priority |
|----------|----------|--------|----------|
| **Critical** | Data loss, complete outage | Business停止 | P0 |
| **High** | Database corruption, major data center failure | Service degraded | P1 |
| **Medium** | Partial service failure, single component down | Some features unavailable | P2 |
| **Low** | Performance degradation, minor data inconsistency | User experience affected | P3 |

### Disaster Recovery Team

| Role | Name | Phone | Email | Responsibility |
|------|------|-------|-------|----------------|
| **DR Lead** | _______ | _______ | _______ | Overall coordination |
| **Database Admin** | _______ | _______ | _______ | Data recovery |
| **DevOps Engineer** | _______ | _______ | _______ | Infrastructure recovery |
| **Application Developer** | _______ | _______ | _______ | Application recovery |
| **Communication Lead** | _______ | _______ | _______ | Stakeholder updates |

---

## Backup Strategy

### Backup Types

#### 1. Database Backups

**Automated Daily Backups** (Railway Plugin)

```bash
# Verify Railway backup plugin enabled
railway plugins list

# Manual backup
./scripts/backup-database.sh production

# Backup script details:
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
BACKUP_FILE="$BACKUP_DIR/production-$TIMESTAMP.sql"

# Create backup
pg_dump "$DATABASE_URL" --format=plain --no-owner --no-acl > "$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_FILE"

# Upload to S3 (optional)
aws s3 cp "$BACKUP_FILE.gz" "s3://your-backup-bucket/database/"

# Verify backup integrity
gunzip -t "$BACKUP_FILE.gz"

echo "Backup completed: $BACKUP_FILE.gz"
```

**Backup Schedule**:
- **Full backup**: Daily at 2:00 AM UTC
- **Point-in-time**: Continuous (WAL archiving via Railway)
- **Retention**: 30 days rolling
- **Location**: Railway managed storage + S3 (optional)

#### 2. Application Code Backups

**Git Repository** (Primary source of truth)

```bash
# Verify all code committed
git status

# Create release tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Clone to backup location (optional)
git clone --mirror https://github.com/your-org/apt-insights.git \
  /backups/git/apt-insights-mirror.git
```

#### 3. Configuration Backups

**Environment Variables**

```bash
# Export Railway environment variables
railway variables > backups/env-vars-$(date +%Y%m%d).txt

# Export Vercel environment variables
vercel env ls > backups/vercel-env-$(date +%Y%m%d).txt

# Store securely (encrypted)
gpg --encrypt --recipient your-email@domain.com backups/env-vars-*.txt
```

#### 4. Redis Backups

**Redis Persistence** (Enabled by default)

```bash
# Verify RDB persistence enabled
redis-cli CONFIG GET save

# Manual snapshot
redis-cli BGSAVE

# Check last save time
redis-cli LASTSAVE

# Backup RDB file (if self-hosted)
cp /var/lib/redis/dump.rdb /backups/redis/dump-$(date +%Y%m%d).rdb
```

#### 5. File Storage Backups

**User Uploads / Generated Files**

```bash
# Backup output directories
tar -czf backups/outputs-$(date +%Y%m%d).tar.gz \
  api_01/output/ \
  api_02/output/ \
  api_03/output/ \
  api_04/output/

# Upload to S3
aws s3 cp backups/outputs-*.tar.gz s3://your-backup-bucket/files/
```

### Backup Verification

**Daily Automated Verification**

```bash
#!/bin/bash
# verify-backups.sh

echo "=== Backup Verification Report ==="
echo "Date: $(date)"
echo ""

# Check database backup
LATEST_DB_BACKUP=$(ls -t /backups/production-*.sql.gz | head -1)
if [ -f "$LATEST_DB_BACKUP" ]; then
    echo "✅ Database backup found: $LATEST_DB_BACKUP"
    echo "   Size: $(du -h $LATEST_DB_BACKUP | cut -f1)"
    echo "   Age: $(find $LATEST_DB_BACKUP -mtime -1 -print)"

    # Test backup integrity
    gunzip -t "$LATEST_DB_BACKUP" && echo "   ✅ Integrity OK" || echo "   ❌ Integrity FAILED"
else
    echo "❌ No database backup found!"
fi

# Check backup age
BACKUP_AGE=$(find /backups -name "production-*.sql.gz" -mtime -1 | wc -l)
if [ $BACKUP_AGE -eq 0 ]; then
    echo "⚠️  WARNING: No backup in last 24 hours!"
fi

# Check backup count
BACKUP_COUNT=$(ls -1 /backups/production-*.sql.gz 2>/dev/null | wc -l)
echo ""
echo "Total backups: $BACKUP_COUNT"

# Check disk space
echo ""
echo "Backup storage:"
df -h /backups

echo ""
echo "=== End of Report ==="
```

Run daily via cron:
```bash
# Add to crontab
0 3 * * * /path/to/verify-backups.sh | mail -s "Daily Backup Verification" team@company.com
```

### Backup Retention Policy

| Backup Type | Retention | Location | Frequency |
|-------------|-----------|----------|-----------|
| Database Full | 30 days | Railway + S3 | Daily |
| Database WAL | 7 days | Railway | Continuous |
| Application Code | Indefinite | GitHub | On commit |
| Configuration | 90 days | Encrypted file | Weekly |
| Redis Snapshots | 7 days | Railway | Daily |
| File Storage | 30 days | S3 | Daily |

---

## Recovery Procedures

### Full System Recovery

**Scenario**: Complete data center failure, all services down

**Estimated Recovery Time**: 2-4 hours

#### Step 1: Assess Damage (15 minutes)

```bash
# Check service status
./scripts/check-all-health.sh production

# Review recent changes
git log --oneline -10

# Check Railway status
curl https://status.railway.app/api/v2/status.json | jq

# Check Vercel status
curl https://www.vercel-status.com/api/v2/status.json | jq

# Document findings
cat > recovery-log-$(date +%Y%m%d-%H%M%S).md <<EOF
# Recovery Log

**Incident Start**: $(date)
**Detected By**: _______
**Initial Assessment**: _______

## Impact
- Frontend: _______
- Backend: _______
- Database: _______
- Redis: _______

## Next Steps
1. _______
2. _______
EOF
```

#### Step 2: Restore Database (30-60 minutes)

```bash
# 1. Identify latest backup
LATEST_BACKUP=$(ls -t /backups/production-*.sql.gz | head -1)
echo "Using backup: $LATEST_BACKUP"

# 2. Verify backup integrity
gunzip -t "$LATEST_BACKUP"

# 3. Create new database instance (if needed)
railway up postgresql

# 4. Restore database
gunzip -c "$LATEST_BACKUP" | railway run psql $DATABASE_URL

# 5. Verify restoration
railway run psql $DATABASE_URL -c "
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;"

# 6. Run migrations (if needed)
cd fastapi-backend
alembic upgrade head

# 7. Verify data integrity
railway run psql $DATABASE_URL -c "SELECT COUNT(*) FROM apartments;"
```

#### Step 3: Restore Redis (10 minutes)

```bash
# 1. Create new Redis instance (if needed)
railway up redis

# 2. Configure Redis password
railway variables set REDIS_PASSWORD=<secure-password>

# 3. Warm cache
python fastapi-backend/cache/cache_warming.py

# 4. Verify cache
redis-cli -h <host> -a <password> INFO keyspace
```

#### Step 4: Restore Application (30 minutes)

```bash
# 1. Deploy backend
cd fastapi-backend
railway up

# 2. Deploy frontend
cd nextjs-frontend
vercel --prod

# 3. Wait for deployments
sleep 120

# 4. Verify health
curl https://api.your-domain.com/health
curl https://your-domain.com/api/health

# 5. Run smoke tests
./scripts/smoke-test.sh production
```

#### Step 5: Verify Recovery (15 minutes)

```bash
# 1. Test critical user flows
./scripts/test-critical-flows.sh

# 2. Check error rates
curl https://api.your-domain.com/api/metrics | grep error

# 3. Monitor logs
railway logs -f | grep -E 'ERROR|WARN'

# 4. Verify database queries
railway run psql $DATABASE_URL -c "
SELECT query, calls, mean_time
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 5;"

# 5. Check cache hit rate
redis-cli INFO stats | grep keyspace_hits
```

#### Step 6: Post-Recovery (30 minutes)

```bash
# 1. Notify stakeholders
echo "System recovered at $(date)" | \
  mail -s "RESOLVED: System Recovery Complete" team@company.com

# 2. Document incident
# Complete recovery-log file

# 3. Schedule post-mortem
# Within 48 hours

# 4. Monitor closely
# Next 24 hours - increased vigilance
```

### Database-Only Recovery

**Scenario**: Database corruption, accidental data deletion

**Estimated Recovery Time**: 30-60 minutes

```bash
#!/bin/bash
# restore-database.sh

set -e

BACKUP_FILE=$1
TARGET_ENV=${2:-production}

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup-file> [environment]"
    echo "Example: $0 /backups/production-20260208.sql.gz production"
    exit 1
fi

echo "=== Database Recovery ==="
echo "Backup file: $BACKUP_FILE"
echo "Target environment: $TARGET_ENV"
echo ""

# 1. Verify backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found!"
    exit 1
fi

# 2. Test backup integrity
echo "Testing backup integrity..."
gunzip -t "$BACKUP_FILE"
echo "✅ Backup integrity OK"
echo ""

# 3. Confirm action
read -p "⚠️  This will OVERWRITE the $TARGET_ENV database. Continue? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# 4. Create pre-restore backup
echo "Creating pre-restore backup..."
./scripts/backup-database.sh "$TARGET_ENV"
echo ""

# 5. Drop existing connections
echo "Terminating existing connections..."
railway run psql $DATABASE_URL -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = current_database()
AND pid != pg_backend_pid();"
echo ""

# 6. Restore database
echo "Restoring database..."
gunzip -c "$BACKUP_FILE" | railway run psql $DATABASE_URL
echo "✅ Database restored"
echo ""

# 7. Run migrations
echo "Running migrations..."
cd fastapi-backend
alembic upgrade head
cd ..
echo "✅ Migrations complete"
echo ""

# 8. Verify restoration
echo "Verifying restoration..."
RECORD_COUNT=$(railway run psql $DATABASE_URL -t -c "SELECT COUNT(*) FROM apartments;")
echo "Record count: $RECORD_COUNT"

if [ "$RECORD_COUNT" -gt 0 ]; then
    echo "✅ Data verified"
else
    echo "⚠️  Warning: No records found!"
fi
echo ""

# 9. Rebuild indexes
echo "Rebuilding indexes..."
railway run psql $DATABASE_URL -c "REINDEX DATABASE apt_insights;"
echo "✅ Indexes rebuilt"
echo ""

# 10. Update statistics
echo "Updating statistics..."
railway run psql $DATABASE_URL -c "VACUUM ANALYZE;"
echo "✅ Statistics updated"
echo ""

echo "=== Recovery Complete ==="
echo "Next steps:"
echo "1. Test application functionality"
echo "2. Monitor error logs"
echo "3. Verify data integrity"
echo "4. Document incident"
```

### Partial Data Recovery

**Scenario**: Specific table or records corrupted/deleted

```bash
#!/bin/bash
# restore-partial-data.sh

BACKUP_FILE=$1
TABLE_NAME=$2

# 1. Extract specific table from backup
pg_restore -t "$TABLE_NAME" --data-only "$BACKUP_FILE" > "temp-$TABLE_NAME.sql"

# 2. Review data before restore
head -20 "temp-$TABLE_NAME.sql"

# 3. Restore to staging first
railway run psql $STAGING_DATABASE_URL < "temp-$TABLE_NAME.sql"

# 4. Verify in staging
railway run psql $STAGING_DATABASE_URL -c "SELECT COUNT(*) FROM $TABLE_NAME;"

# 5. If OK, restore to production
read -p "Restore to production? (yes/no): " confirm
if [ "$confirm" == "yes" ]; then
    railway run psql $DATABASE_URL < "temp-$TABLE_NAME.sql"
fi

# 6. Cleanup
rm "temp-$TABLE_NAME.sql"
```

### Point-in-Time Recovery (PITR)

**Scenario**: Need to restore to specific timestamp

```bash
#!/bin/bash
# point-in-time-restore.sh

TARGET_TIME=$1  # Format: "2026-02-08 12:00:00"

# 1. Create new database instance
railway up postgresql --name recovery-db

# 2. Restore from base backup
gunzip -c /backups/production-base.sql.gz | railway run psql $RECOVERY_DB_URL

# 3. Apply WAL logs up to target time
# (Railway handles this automatically via WAL archiving)

# 4. Verify recovered data
railway run psql $RECOVERY_DB_URL -c "
SELECT * FROM apartments
WHERE updated_at <= '$TARGET_TIME'
ORDER BY updated_at DESC
LIMIT 10;"

# 5. Switch to recovered database (if verified)
# Update DATABASE_URL in Railway
```

---

## Testing & Validation

### Disaster Recovery Drill

**Frequency**: Quarterly

**Procedure**:

```bash
#!/bin/bash
# disaster-recovery-drill.sh

echo "=== Disaster Recovery Drill ==="
echo "Date: $(date)"
echo ""

# 1. Create staging environment
echo "Step 1: Creating staging environment..."
railway up --environment staging

# 2. Restore latest backup to staging
echo "Step 2: Restoring backup to staging..."
LATEST_BACKUP=$(ls -t /backups/production-*.sql.gz | head -1)
./scripts/restore-database.sh "$LATEST_BACKUP" staging

# 3. Deploy application to staging
echo "Step 3: Deploying application..."
railway up --environment staging

# 4. Run tests
echo "Step 4: Running tests..."
./scripts/smoke-test.sh staging

# 5. Measure recovery time
echo "Step 5: Measuring recovery time..."
DRILL_END=$(date +%s)
DRILL_START=$(cat /tmp/drill-start-time)
RECOVERY_TIME=$((DRILL_END - DRILL_START))
echo "Recovery time: $((RECOVERY_TIME / 60)) minutes"

# 6. Generate report
cat > drill-report-$(date +%Y%m%d).md <<EOF
# Disaster Recovery Drill Report

**Date**: $(date)
**Recovery Time**: $((RECOVERY_TIME / 60)) minutes
**RTO Target**: 60 minutes
**Status**: $([ $RECOVERY_TIME -lt 3600 ] && echo "PASSED" || echo "FAILED")

## Steps Completed
- [x] Environment creation
- [x] Database restoration
- [x] Application deployment
- [x] Testing
- [x] Verification

## Issues Encountered
- _______

## Action Items
- _______

## Next Drill
**Scheduled**: $(date -d "+3 months" +%Y-%m-%d)
EOF

# 7. Cleanup staging environment
echo "Step 7: Cleaning up..."
railway down --environment staging

echo "Drill complete. Report: drill-report-$(date +%Y%m%d).md"
```

### Backup Restoration Test

**Frequency**: Monthly

```bash
#!/bin/bash
# test-backup-restoration.sh

echo "=== Backup Restoration Test ==="

# Test last 3 backups
for BACKUP in $(ls -t /backups/production-*.sql.gz | head -3); do
    echo ""
    echo "Testing: $BACKUP"

    # 1. Check integrity
    gunzip -t "$BACKUP" && echo "✅ Integrity OK" || echo "❌ FAILED"

    # 2. Test restoration to temp database
    createdb temp_restore_test
    gunzip -c "$BACKUP" | psql temp_restore_test > /dev/null 2>&1

    # 3. Verify data
    RECORD_COUNT=$(psql temp_restore_test -t -c "SELECT COUNT(*) FROM apartments;")
    echo "   Records: $RECORD_COUNT"

    # 4. Cleanup
    dropdb temp_restore_test

    if [ "$RECORD_COUNT" -gt 0 ]; then
        echo "✅ Test PASSED"
    else
        echo "❌ Test FAILED"
    fi
done

echo ""
echo "Test complete."
```

---

## Recovery Scenarios

### Scenario 1: Accidental Table Drop

**Detection**: Error logs show "table does not exist"

**Recovery**:
```bash
# 1. Identify affected table
TABLE_NAME="apartments"

# 2. Stop application (prevent further damage)
railway restart --stop

# 3. Restore table from latest backup
LATEST_BACKUP=$(ls -t /backups/production-*.sql.gz | head -1)
pg_restore -t "$TABLE_NAME" "$LATEST_BACKUP" | railway run psql $DATABASE_URL

# 4. Verify restoration
railway run psql $DATABASE_URL -c "SELECT COUNT(*) FROM $TABLE_NAME;"

# 5. Restart application
railway restart

# 6. Monitor
railway logs -f
```

### Scenario 2: Ransomware Attack

**Detection**: Files encrypted, ransom note

**Recovery**:
```bash
# 1. IMMEDIATELY disconnect all systems
# Isolate affected servers

# 2. Notify security team
# DO NOT pay ransom

# 3. Assess damage
# Identify encrypted files

# 4. Restore from clean backups
# Use backup from before infection

# 5. Scan for vulnerabilities
# Patch all systems

# 6. Rebuild from clean images
# Do not restore any infected files

# 7. Restore data
./scripts/restore-database.sh /backups/clean/production.sql.gz

# 8. Change all passwords
./scripts/rotate-all-secrets.sh

# 9. Enable enhanced monitoring
# Watch for reinfection
```

### Scenario 3: Data Center Outage

**Detection**: Railway status page shows outage

**Recovery**:
```bash
# 1. Monitor Railway status
curl https://status.railway.app/api/v2/status.json

# 2. If prolonged (> 30 minutes), failover to backup region
# (Requires multi-region setup)

# 3. If using single region, wait for Railway recovery
# Railway has 99.9% SLA

# 4. Once restored, verify all services
./scripts/check-all-health.sh production

# 5. Check for data loss
./scripts/verify-data-integrity.sh

# 6. Document incident
```

### Scenario 4: Database Corruption

**Detection**: PostgreSQL crashes, "corrupt page" errors

**Recovery**:
```bash
# 1. Attempt to start in recovery mode
railway run psql $DATABASE_URL -c "SET zero_damaged_pages = on;"

# 2. If that fails, restore from backup
./scripts/restore-database.sh /backups/production-latest.sql.gz

# 3. Identify cause
# Check hardware, PostgreSQL logs

# 4. Run integrity checks
railway run psql $DATABASE_URL -c "
SELECT * FROM pg_catalog.pg_database WHERE datname = 'apt_insights';"

# 5. Rebuild indexes
railway run psql $DATABASE_URL -c "REINDEX DATABASE apt_insights;"

# 6. Monitor for recurrence
```

### Scenario 5: Bad Deployment

**Detection**: High error rate after deployment

**Recovery**:
```bash
# 1. Immediately rollback
./scripts/rollback.sh <previous-version>

# 2. Verify rollback successful
curl https://api.your-domain.com/health

# 3. Check for database migration issues
cd fastapi-backend
alembic current
alembic downgrade -1  # If needed

# 4. Monitor error rates
curl https://api.your-domain.com/api/metrics | grep error

# 5. Investigate failure
# Fix in development, test thoroughly

# 6. Document incident and prevention steps
```

---

## Failover Procedures

### Automatic Failover

Railway provides automatic failover for:
- **Database**: Automatic replica promotion
- **Application**: Health check failures trigger restart
- **Load Balancing**: Automatic request routing

### Manual Failover

**When to use**: Automatic failover failed, need immediate control

```bash
# 1. Assess primary region
railway status --region us-west

# 2. Promote standby (if configured)
railway promote-standby --database

# 3. Update DNS (if using custom domain)
# Point to new endpoint

# 4. Verify new primary
./scripts/check-all-health.sh production

# 5. Monitor traffic
railway logs -f
```

---

## Data Loss Prevention

### 1. Continuous Backup

```bash
# Enable WAL archiving (Railway default)
# Provides point-in-time recovery

# Verify WAL archiving
railway run psql $DATABASE_URL -c "SHOW archive_mode;"
```

### 2. Replication

```bash
# Enable read replicas (Railway enterprise)
railway replicas create --count 2

# Verify replication lag
railway run psql $DATABASE_URL -c "SELECT * FROM pg_stat_replication;"
```

### 3. Multi-Region Backup

```bash
# Copy backups to multiple regions
aws s3 sync /backups/ s3://backup-us-west/ --region us-west-2
aws s3 sync /backups/ s3://backup-eu-central/ --region eu-central-1

# Verify replication
aws s3 ls s3://backup-us-west/
aws s3 ls s3://backup-eu-central/
```

### 4. Versioning

```bash
# Enable S3 versioning for backups
aws s3api put-bucket-versioning \
  --bucket your-backup-bucket \
  --versioning-configuration Status=Enabled

# List versions
aws s3api list-object-versions --bucket your-backup-bucket
```

### 5. Immutable Backups

```bash
# Enable S3 Object Lock (requires vault)
aws s3api put-object-lock-configuration \
  --bucket your-backup-bucket \
  --object-lock-configuration 'ObjectLockEnabled=Enabled'
```

---

## Appendix

### Recovery Checklists

#### Database Recovery Checklist

- [ ] Backup file identified and verified
- [ ] Backup integrity tested
- [ ] Pre-recovery backup created
- [ ] Existing connections terminated
- [ ] Database restored
- [ ] Migrations applied
- [ ] Data integrity verified
- [ ] Indexes rebuilt
- [ ] Statistics updated
- [ ] Application restarted
- [ ] Smoke tests passed
- [ ] Monitoring resumed
- [ ] Incident documented

#### Application Recovery Checklist

- [ ] Root cause identified
- [ ] Fix deployed to staging
- [ ] Staging tests passed
- [ ] Production backup created
- [ ] Deployment executed
- [ ] Health checks passed
- [ ] Error rates normal
- [ ] Performance verified
- [ ] Rollback plan ready
- [ ] Team notified
- [ ] Monitoring active
- [ ] Documentation updated

### Contact Directory

**Emergency Contacts**: See RUNBOOK.md

**External Support**:
- Railway Support: support@railway.app
- Vercel Support: support@vercel.com
- Database Expert: _______
- Security Consultant: _______

### Recovery Time Estimates

| Scenario | RTO Estimate | Complexity |
|----------|-------------|------------|
| Service restart | 5 minutes | Low |
| Application rollback | 15 minutes | Low |
| Database restore (small) | 30 minutes | Medium |
| Database restore (large) | 2 hours | Medium |
| Full system recovery | 4 hours | High |
| Multi-region failover | 1 hour | High |
| Data center migration | 8 hours | Very High |

---

**Last Updated**: 2026-02-08
**Document Version**: 1.0.0
**Next Review**: 2026-03-08
**Next Drill**: 2026-05-08
