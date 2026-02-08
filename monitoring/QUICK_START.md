# Monitoring Quick Start Guide

Get monitoring up and running in 5 minutes.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.9+ installed
- Node.js 18+ installed (for frontend)

## 1. Run Setup Script

```bash
# From project root
./scripts/setup-monitoring.sh
```

This script will:
- Check dependencies
- Install Python/Node packages
- Create environment files
- Start monitoring stack

## 2. Configure Sentry

### Create Sentry Account

1. Go to https://sentry.io/signup/
2. Create a free account

### Create Projects

**Backend Project:**
1. Click "Create Project"
2. Select "Python" → "FastAPI"
3. Name: "apartment-analysis-backend"
4. Copy the DSN

**Frontend Project:**
1. Click "Create Project"
2. Select "JavaScript" → "Next.js"
3. Name: "apartment-analysis-frontend"
4. Copy the DSN

### Add DSNs to Environment Files

**Backend (.env):**
```bash
cd fastapi-backend
nano .env

# Add your DSN
SENTRY_DSN=https://your-backend-dsn@sentry.io/your-project-id
```

**Frontend (.env.local):**
```bash
cd nextjs-frontend
nano .env.local

# Add your DSN
NEXT_PUBLIC_SENTRY_DSN=https://your-frontend-dsn@sentry.io/your-project-id
```

## 3. Start Application

**Terminal 1 - Backend:**
```bash
cd fastapi-backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd nextjs-frontend
npm run dev
```

## 4. Verify Monitoring

### Health Checks

```bash
# Basic health
curl http://localhost:8000/api/health

# Detailed health (includes all dependencies)
curl http://localhost:8000/api/health/detailed
```

### Metrics

```bash
# View Prometheus metrics
curl http://localhost:8000/api/metrics

# Or open in browser
open http://localhost:8000/api/metrics
```

### Dashboards

```bash
# Open Prometheus
open http://localhost:9090

# Open Grafana (login: admin/admin)
open http://localhost:3001

# Open Alertmanager
open http://localhost:9093
```

### Test Error Tracking

**Backend:**
```python
# Add to any endpoint temporarily
from config.sentry import capture_message
capture_message("Test message from backend", level="info")
```

**Frontend:**
```typescript
// Add to any component temporarily
import { captureMessage } from '@/config/sentry.config';
captureMessage('Test message from frontend', 'info');
```

Check Sentry dashboard for the messages.

## 5. Import Grafana Dashboard

1. Open Grafana at http://localhost:3001
2. Login with `admin` / `admin`
3. Change password when prompted
4. Go to Dashboards → Import
5. Click "Upload JSON file"
6. Select `monitoring/grafana-dashboard.json`
7. Select "Prometheus" as data source
8. Click "Import"

## 6. Configure Alerts (Optional)

Edit `monitoring/alertmanager.yml` to add your notification channels:

**Slack:**
```yaml
slack_configs:
  - api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
    channel: '#alerts'
```

**Email:**
```yaml
email_configs:
  - to: 'you@example.com'
    from: 'alerts@example.com'
    smarthost: 'smtp.gmail.com:587'
    auth_username: 'alerts@example.com'
    auth_password: 'YOUR_APP_PASSWORD'
```

Restart Alertmanager:
```bash
cd monitoring
docker-compose -f docker-compose.monitoring.yml restart alertmanager
```

## Troubleshooting

### Monitoring stack not starting

```bash
# Check Docker is running
docker ps

# Check logs
cd monitoring
docker-compose -f docker-compose.monitoring.yml logs

# Restart services
docker-compose -f docker-compose.monitoring.yml restart
```

### Metrics endpoint returns 404

```bash
# Make sure you're using the correct endpoint
curl http://localhost:8000/api/metrics

# NOT /metrics (without /api prefix)
```

### Grafana shows "No data"

1. Check Prometheus targets are UP:
   - Go to http://localhost:9090/targets
   - All targets should be green/UP

2. Check backend is running:
   ```bash
   curl http://localhost:8000/api/health
   ```

3. Check data source in Grafana:
   - Go to Configuration → Data Sources
   - Verify Prometheus is configured with URL: http://prometheus:9090

### Sentry not capturing errors

1. Check DSN is set:
   ```bash
   grep SENTRY_DSN fastapi-backend/.env
   ```

2. Check logs for Sentry initialization:
   ```bash
   tail -f fastapi-backend/logs/app.log | grep sentry
   ```

3. Trigger a test error:
   ```bash
   curl http://localhost:8000/api/nonexistent-endpoint
   ```

## Next Steps

- Read [MONITORING_OBSERVABILITY.md](../MONITORING_OBSERVABILITY.md) for comprehensive guide
- Configure alerts in `monitoring/alerts.yml`
- Set up notification channels in `monitoring/alertmanager.yml`
- Create custom Grafana dashboards
- Set up log aggregation for production

## Support

For issues:
1. Check logs: `docker-compose -f docker-compose.monitoring.yml logs`
2. Check application logs: `tail -f fastapi-backend/logs/app.log`
3. Review [MONITORING_OBSERVABILITY.md](../MONITORING_OBSERVABILITY.md) troubleshooting section
