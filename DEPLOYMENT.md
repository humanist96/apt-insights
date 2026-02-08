# Production Deployment Guide

This guide covers deploying the Korean Apartment Transaction Analysis Platform to production.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [CI/CD Pipeline Overview](#cicd-pipeline-overview)
- [Prerequisites](#prerequisites)
- [GitHub Actions Setup](#github-actions-setup)
- [Option 1: Vercel + Railway (Recommended)](#option-1-vercel--railway-recommended)
- [Option 2: Self-Hosted with Docker](#option-2-self-hosted-with-docker)
- [Environment Variables](#environment-variables)
- [Database Migration](#database-migration)
- [SSL Certificate Setup](#ssl-certificate-setup)
- [Monitoring Setup](#monitoring-setup)
- [Rollback Procedures](#rollback-procedures)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

```
┌──────────────────┐
│   Vercel CDN     │ <- Next.js Frontend (Static + SSR)
│   (Global)       │
└────────┬─────────┘
         │ HTTPS
         ▼
┌──────────────────┐
│   Railway        │ <- FastAPI Backend
│   (Cloud)        │
├──────────────────┤
│   PostgreSQL     │ <- Database
├──────────────────┤
│   Redis          │ <- Cache
└──────────────────┘
```

## CI/CD Pipeline Overview

The platform uses GitHub Actions for continuous integration and deployment.

### Pipeline Architecture

```
Push/PR to main
      |
      v
+-----------------+     +-----------------+
| PR Checks       |     | CodeQL Analysis |
| - Lint          |     | - Python scan   |
| - Type check    |     | - JS/TS scan    |
| - Tests         |     | - Secret scan   |
| - Security      |     +-----------------+
+-----------------+
      |
      v (merge to main)
+------------------------------------------+
| Deploy Production                        |
|                                          |
|  +--------+   +----------+   +--------+  |
|  | Backend|-->| Database |-->|Frontend|  |
|  | Tests  |   |Migration |   | Tests  |  |
|  +--------+   +----------+   +--------+  |
|       |                          |        |
|       v                          v        |
|  +--------+                 +---------+   |
|  |Railway |                 | Vercel  |   |
|  |Deploy  |                 | Deploy  |   |
|  +--------+                 +---------+   |
|       |                          |        |
|       v                          v        |
|  +---------------------------------+      |
|  |        Smoke Tests              |      |
|  +---------------------------------+      |
+------------------------------------------+
```

### Workflow Files

| File | Purpose | Trigger |
|------|---------|---------|
| `backend-ci.yml` | Backend lint, test, security, Docker build, Railway deploy | Push/PR to `fastapi-backend/` |
| `frontend-ci.yml` | Frontend lint, test, build, security audit, Vercel deploy | Push/PR to `nextjs-frontend/` |
| `deploy-production.yml` | Full-stack production deployment with migrations | Merge to main / Manual |
| `pr-checks.yml` | Consolidated PR quality gates | All PRs to main |
| `codeql-analysis.yml` | CodeQL security scanning | Push to main / Weekly |
| `dependabot.yml` | Automated dependency updates | Weekly schedule |

### Required GitHub Secrets

Configure these in **Settings > Secrets and variables > Actions**:

| Secret | Description | Required For |
|--------|-------------|--------------|
| `RAILWAY_TOKEN` | Railway API token | Backend deployment |
| `RAILWAY_DATABASE_URL` | Railway PostgreSQL URL | Database migrations |
| `VERCEL_TOKEN` | Vercel API token | Frontend deployment |
| `VERCEL_ORG_ID` | Vercel organization ID | Frontend deployment |
| `VERCEL_PROJECT_ID` | Vercel project ID | Frontend deployment |

See [ENVIRONMENT_VARIABLES.md](./ENVIRONMENT_VARIABLES.md) for the complete list.

### Setting Up GitHub Secrets

```bash
# Using GitHub CLI
gh secret set RAILWAY_TOKEN --body "your-railway-token"
gh secret set RAILWAY_DATABASE_URL --body "postgresql://user:pass@host:port/db"
gh secret set VERCEL_TOKEN --body "your-vercel-token"
gh secret set VERCEL_ORG_ID --body "your-vercel-org-id"
gh secret set VERCEL_PROJECT_ID --body "your-vercel-project-id"
```

### Manual Deployment Trigger

The `deploy-production.yml` workflow supports manual dispatch:

```bash
# Deploy everything
gh workflow run deploy-production.yml

# Deploy only backend
gh workflow run deploy-production.yml \
  -f deploy_backend=true \
  -f deploy_frontend=false \
  -f run_migrations=false

# Emergency deploy (skip tests)
gh workflow run deploy-production.yml \
  -f skip_tests=true
```

---

## Prerequisites

### Required Accounts

- [ ] Vercel account (https://vercel.com)
- [ ] Railway account (https://railway.app)
- [ ] GitHub account (for deployments)
- [ ] Domain name (optional, for custom domain)

### Required Credentials

- [ ] Korean Ministry of Land API key (`SERVICE_KEY`)
- [ ] Google Gemini API key (`GEMINI_API_KEY`, optional)
- [ ] PostgreSQL credentials
- [ ] Redis credentials

### Required Tools

```bash
# Install Vercel CLI
npm install -g vercel

# Install Railway CLI
npm install -g @railway/cli

# Install Docker (for local testing)
brew install docker docker-compose
```

---

## Option 1: Vercel + Railway (Recommended)

This is the easiest and most cost-effective deployment method for production.

### Step 1: Deploy FastAPI Backend to Railway

#### 1.1 Create Railway Project

```bash
# Login to Railway
railway login

# Navigate to backend directory
cd fastapi-backend

# Initialize Railway project
railway init
```

#### 1.2 Add PostgreSQL Database

```bash
# Add PostgreSQL plugin
railway add postgresql

# Railway automatically sets DATABASE_URL
```

#### 1.3 Add Redis Cache

```bash
# Add Redis plugin
railway add redis

# Railway automatically sets REDIS_URL
```

#### 1.4 Configure Environment Variables

In Railway dashboard (https://railway.app/dashboard):

1. Go to your project → Variables
2. Add the following variables:

```env
# Required
SERVICE_KEY=your_ministry_of_land_api_key
USE_DATABASE=true
USE_REDIS=true

# Optional
GEMINI_API_KEY=your_gemini_api_key
LOG_LEVEL=info
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-app.vercel.app

# Auto-generated by Railway (verify these exist)
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
PORT=8000
```

#### 1.5 Deploy Backend

```bash
# Deploy to Railway
railway up

# Get the deployment URL
railway open
# Copy the URL (e.g., https://your-backend.railway.app)
```

#### 1.6 Run Database Migrations

```bash
# SSH into Railway container
railway run bash

# Run migrations (if you have migration scripts)
# python migrate.py

# Or manually load initial data
# python load_data.py
```

### Step 2: Deploy Next.js Frontend to Vercel

#### 2.1 Push Code to GitHub

```bash
# Ensure code is committed
cd nextjs-frontend
git add .
git commit -m "feat: production deployment configuration"
git push origin main
```

#### 2.2 Import Project to Vercel

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Select `nextjs-frontend` as root directory
4. Configure project settings:
   - Framework Preset: **Next.js**
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

#### 2.3 Configure Environment Variables

In Vercel dashboard → Settings → Environment Variables:

```env
# Required
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_APP_NAME=Korean Apartment Transaction Analysis
NEXT_PUBLIC_APP_VERSION=1.0.0

# Optional
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_API_TIMEOUT=30000
```

#### 2.4 Deploy Frontend

```bash
# Deploy using Vercel CLI
cd nextjs-frontend
vercel --prod

# Or deploy via Git push (auto-deploys)
git push origin main
```

#### 2.5 Update CORS in Backend

Update Railway backend environment variables:

```env
ALLOWED_ORIGINS=https://your-app.vercel.app,https://your-custom-domain.com
```

Redeploy backend:

```bash
railway up --detach
```

### Step 3: Configure Custom Domain (Optional)

#### 3.1 Add Domain to Vercel

1. Go to Vercel project → Settings → Domains
2. Add your domain (e.g., `apt-insights.com`)
3. Follow DNS configuration instructions

#### 3.2 Update Backend CORS

```env
ALLOWED_ORIGINS=https://apt-insights.com,https://www.apt-insights.com
```

---

## Option 2: Self-Hosted with Docker

For organizations that prefer self-hosting or need more control.

### Step 1: Prepare Server

```bash
# Provision Ubuntu 22.04 server (AWS EC2, DigitalOcean, etc.)
# Minimum requirements:
# - 2 vCPUs
# - 4 GB RAM
# - 20 GB SSD
# - Ubuntu 22.04 LTS

# SSH into server
ssh ubuntu@your-server-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Step 2: Clone Repository

```bash
# Clone repository
git clone https://github.com/your-username/apt_test.git
cd apt_test

# Create production environment file
cp .env.example .env.production

# Edit environment variables
nano .env.production
```

### Step 3: Configure Environment Variables

Edit `.env.production`:

```env
# PostgreSQL
POSTGRES_PASSWORD=your_secure_postgres_password

# Redis
REDIS_PASSWORD=your_secure_redis_password

# API Keys
SERVICE_KEY=your_ministry_of_land_api_key
GEMINI_API_KEY=your_gemini_api_key

# Security
SECRET_KEY=your_secret_key_at_least_32_characters_long

# CORS (use your domain)
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### Step 4: Start Services

```bash
# Start all services
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Step 5: Run Database Migrations

```bash
# Execute migrations in backend container
docker-compose -f docker-compose.prod.yml exec backend python migrate.py

# Or load initial data
docker-compose -f docker-compose.prod.yml exec backend python load_data.py
```

### Step 6: Configure Nginx & SSL

See [SSL Certificate Setup](#ssl-certificate-setup) section below.

---

## Environment Variables

### Next.js Frontend (.env.production.local)

```env
# Required
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
NEXT_PUBLIC_APP_NAME=Korean Apartment Transaction Analysis
NEXT_PUBLIC_APP_VERSION=1.0.0

# Optional
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DEBUG=false
NEXT_PUBLIC_API_TIMEOUT=30000
NEXT_PUBLIC_API_RETRY_COUNT=3
```

### FastAPI Backend (.env.production)

```env
# Database
USE_DATABASE=true
DATABASE_URL=postgresql://user:password@host:port/database

# Cache
USE_REDIS=true
REDIS_URL=redis://:password@host:port/0

# API Keys
SERVICE_KEY=your_ministry_api_key
GEMINI_API_KEY=your_gemini_api_key

# Security
SECRET_KEY=your_secret_key
ALLOWED_ORIGINS=https://your-frontend.vercel.app

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Logging
LOG_LEVEL=info
ENVIRONMENT=production
```

---

## Database Migration

### Automated Migration (Recommended)

If you have migration scripts:

```bash
# Railway
railway run python migrate.py

# Docker
docker-compose -f docker-compose.prod.yml exec backend python migrate.py
```

### Manual Data Loading

Load data from JSON files:

```bash
# Navigate to project root
cd /path/to/apt_test

# Run data loader script
python -c "
from backend.data_loader import DataLoader
loader = DataLoader()
data = loader.get_all_data()
print(f'Loaded {len(data)} transactions')
"
```

### Database Backup

```bash
# PostgreSQL backup
pg_dump -h localhost -U postgres -d apt_insights -F c -f backup_$(date +%Y%m%d).dump

# Restore from backup
pg_restore -h localhost -U postgres -d apt_insights -F c backup_20260207.dump
```

---

## SSL Certificate Setup

### Using Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal (already configured by certbot)
sudo certbot renew --dry-run
```

### Manual SSL Configuration

1. Obtain SSL certificate from your provider
2. Copy certificate files to `/etc/nginx/ssl/`
3. Update `nginx/nginx.conf` with correct paths
4. Restart Nginx: `docker-compose restart nginx`

---

## Monitoring Setup

### Health Check Endpoints

- **Frontend**: `https://your-app.vercel.app/api/health`
- **Backend**: `https://your-backend.railway.app/health`

### Uptime Monitoring (Free Options)

1. **UptimeRobot** (https://uptimerobot.com)
   - Add both frontend and backend health checks
   - Set check interval to 5 minutes
   - Configure email/SMS alerts

2. **Better Uptime** (https://betteruptime.com)
   - Monitor HTTP endpoints
   - Status page included

### Application Monitoring (Optional)

#### Sentry for Error Tracking

```bash
# Install Sentry SDK
pip install sentry-sdk

# Add to backend/.env.production
SENTRY_DSN=your_sentry_dsn
```

#### Vercel Analytics (Built-in)

Enable in Vercel dashboard → Analytics → Enable

### Log Management

#### Railway Logs

```bash
# View backend logs
railway logs --service backend

# Follow logs in real-time
railway logs --follow
```

#### Docker Logs

```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Export logs
docker-compose -f docker-compose.prod.yml logs backend > backend.log
```

### Database Monitoring

```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('apt_insights'));

-- Check active connections
SELECT count(*) FROM pg_stat_activity WHERE datname = 'apt_insights';

-- Check slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

## Rollback Procedures

### Automated Rollback Notification

When a deployment fails, the CI/CD pipeline automatically:
1. Creates a GitHub issue labeled `deployment-failure` and `urgent`
2. Includes links to the failed workflow run
3. Provides rollback instructions

### Backend Rollback (Railway)

```bash
# Option 1: Railway Dashboard
# Go to https://railway.app/dashboard -> Deployments -> Click previous deployment -> Rollback

# Option 2: Railway CLI
railway rollback --service fastapi-backend

# Option 3: Redeploy known good commit
git checkout <known-good-commit-sha>
cd fastapi-backend
railway up --service fastapi-backend
```

### Frontend Rollback (Vercel)

```bash
# Option 1: Vercel Dashboard
# Go to Vercel -> Deployments -> Click previous deployment -> Promote to Production

# Option 2: Vercel CLI
vercel rollback
```

### Database Rollback

```bash
# Restore from backup
pg_restore -h <host> -U postgres -d apt_insights -F c backup_YYYYMMDD.dump

# Or reverse a specific migration
railway run psql $DATABASE_URL -f fastapi-backend/migrations/rollback_001.sql
```

### Full Stack Rollback

1. Rollback backend first (Railway dashboard or CLI)
2. Verify backend health: `curl https://your-backend.railway.app/health`
3. Rollback frontend (Vercel dashboard or CLI)
4. Verify frontend: `curl -s -o /dev/null -w "%{http_code}" https://your-app.vercel.app`
5. If database migration caused the issue, restore from latest backup
6. Create a post-mortem issue on GitHub

---

## Troubleshooting

### Frontend Issues

#### Build Failures

```bash
# Clear Next.js cache
rm -rf .next
rm -rf node_modules
npm install
npm run build
```

#### API Connection Errors

- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check CORS configuration in backend
- Test backend health: `curl https://your-backend.railway.app/health`

### Backend Issues

#### Database Connection Errors

```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Test PostgreSQL connection
psql $DATABASE_URL -c "SELECT version();"
```

#### Memory Issues

```bash
# Railway: Increase memory allocation in dashboard
# Docker: Adjust memory limits in docker-compose.prod.yml
```

#### Slow API Responses

- Enable Redis caching: `USE_REDIS=true`
- Increase workers: `WORKERS=8`
- Check database query performance

### Database Issues

#### Disk Space

```bash
# Check disk usage
df -h

# Clear old backups
rm -f /backups/*.dump.old
```

#### Connection Pool Exhausted

Increase pool size in backend environment:

```env
DB_POOL_SIZE=30
DB_MAX_OVERFLOW=20
```

### SSL Issues

```bash
# Test SSL certificate
openssl s_client -connect your-domain.com:443

# Renew Let's Encrypt certificate
sudo certbot renew --force-renewal
```

---

## Post-Deployment Checklist

- [ ] Frontend health check returns 200 OK
- [ ] Backend health check returns 200 OK
- [ ] Database migrations completed
- [ ] Sample API requests work correctly
- [ ] SSL certificate installed and valid
- [ ] CORS configured correctly
- [ ] Environment variables set in production
- [ ] Monitoring and alerts configured
- [ ] Backup strategy implemented
- [ ] Documentation updated with production URLs
- [ ] Performance testing completed
- [ ] Security review completed

---

## Next Steps

1. Review [PRODUCTION_CHECKLIST.md](./PRODUCTION_CHECKLIST.md) for comprehensive checklist
2. Set up monitoring and alerting
3. Configure automated backups
4. Plan capacity scaling strategy
5. Document operational procedures

---

## Support

For deployment assistance:

- Railway: https://railway.app/help
- Vercel: https://vercel.com/support
- Project Issues: https://github.com/your-username/apt_test/issues

---

**Last Updated**: 2026-02-08
