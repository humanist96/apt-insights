# Monitoring Stack

Docker Compose setup for Prometheus, Grafana, and Alertmanager.

## Quick Start

```bash
# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Check status
docker-compose -f docker-compose.monitoring.yml ps

# View logs
docker-compose -f docker-compose.monitoring.yml logs -f

# Stop monitoring stack
docker-compose -f docker-compose.monitoring.yml down
```

## Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Prometheus | http://localhost:9090 | N/A |
| Grafana | http://localhost:3001 | admin/admin |
| Alertmanager | http://localhost:9093 | N/A |
| PostgreSQL Exporter | http://localhost:9187/metrics | N/A |
| Redis Exporter | http://localhost:9121/metrics | N/A |
| Node Exporter | http://localhost:9100/metrics | N/A |

## Configuration Files

- `prometheus.yml` - Prometheus scrape configuration
- `alerts.yml` - Alert rules
- `alertmanager.yml` - Alert routing and notification
- `grafana-dashboard.json` - Pre-configured Grafana dashboard

## Setup

### 1. Configure Alertmanager

Edit `alertmanager.yml` to add your notification channels (Slack, email, PagerDuty).

### 2. Update Database Connection

Edit `docker-compose.monitoring.yml` and update PostgreSQL exporter connection:

```yaml
postgres-exporter:
  environment:
    - DATA_SOURCE_NAME=postgresql://user:password@host:5432/database?sslmode=disable
```

### 3. Update Redis Connection

Edit `docker-compose.monitoring.yml` and update Redis exporter connection:

```yaml
redis-exporter:
  environment:
    - REDIS_ADDR=redis:6379
    - REDIS_PASSWORD=your_password  # If using password
```

## Accessing Dashboards

### Prometheus

1. Navigate to http://localhost:9090
2. Go to Status → Targets to verify all exporters are UP
3. Query metrics using PromQL

### Grafana

1. Navigate to http://localhost:3001
2. Login with admin/admin (change password on first login)
3. Go to Dashboards → Import
4. Upload `grafana-dashboard.json`
5. Select Prometheus as data source

### Alertmanager

1. Navigate to http://localhost:9093
2. View active alerts
3. Silence alerts if needed

## Troubleshooting

### Targets Down in Prometheus

```bash
# Check if application is running
curl http://localhost:8000/api/metrics

# Check Prometheus logs
docker logs apt-prometheus

# Restart Prometheus
docker restart apt-prometheus
```

### Grafana Can't Connect to Prometheus

```bash
# Check if Prometheus is accessible from Grafana container
docker exec apt-grafana curl http://prometheus:9090/-/healthy

# Restart Grafana
docker restart apt-grafana
```

### Exporters Not Collecting Metrics

```bash
# Check PostgreSQL exporter
curl http://localhost:9187/metrics

# Check Redis exporter
curl http://localhost:9121/metrics

# Check exporter logs
docker logs apt-postgres-exporter
docker logs apt-redis-exporter
```

## Persistence

Data is persisted in Docker volumes:
- `prometheus-data` - Prometheus time-series data
- `grafana-data` - Grafana dashboards and settings
- `alertmanager-data` - Alertmanager silences and state

## Production Deployment

For production:

1. **Change Grafana password**:
   ```yaml
   environment:
     - GF_SECURITY_ADMIN_PASSWORD=strong_password
   ```

2. **Enable authentication for Prometheus**:
   Add basic auth or use reverse proxy

3. **Configure external storage**:
   Set up remote storage for long-term metrics retention

4. **Set up backups**:
   Backup Grafana dashboards and Prometheus data

5. **Configure alerts**:
   Set up proper notification channels in `alertmanager.yml`

6. **Resource limits**:
   Add resource limits to services in docker-compose

## See Also

- [MONITORING_OBSERVABILITY.md](../MONITORING_OBSERVABILITY.md) - Complete monitoring guide
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
