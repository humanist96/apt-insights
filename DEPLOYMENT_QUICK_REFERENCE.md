# Production Deployment - Quick Reference Card

One-page reference for production deployment.

## Files Overview

| File | Purpose | Location |
|------|---------|----------|
| `vercel.json` | Vercel config | `/nextjs-frontend/` |
| `railway.json` | Railway config | `/fastapi-backend/` |
| `Dockerfile` | Backend image | `/fastapi-backend/` |
| `docker-compose.prod.yml` | Self-hosted | Root |
| `nginx.conf` | Reverse proxy | `/nginx/` |

## Environment Variables

### Frontend (Vercel)

```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_APP_NAME=Korean Apartment Transaction Analysis
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### Backend (Railway)

```env
SERVICE_KEY=your_ministry_api_key
USE_DATABASE=true
USE_REDIS=true
ALLOWED_ORIGINS=https://your-app.vercel.app
```

## Quick Deploy Commands

### Vercel + Railway

```bash
# 1. Deploy Backend
cd fastapi-backend
railway login
railway init
railway add postgresql
railway add redis
railway up

# 2. Deploy Frontend
cd ../nextjs-frontend
vercel --prod

# 3. Update CORS
# Railway Dashboard → Variables → ALLOWED_ORIGINS
```

### Self-Hosted Docker

```bash
# 1. Setup environment
cp .env.production.example .env.production
./scripts/generate-secret-key.sh
nano .env.production

# 2. Deploy
./scripts/docker-deploy.sh

# 3. Verify
curl http://localhost:8000/health
```

## Health Checks

```bash
# Frontend
curl https://your-app.vercel.app/api/health

# Backend
curl https://your-backend.railway.app/health
```

## Common Issues

### CORS Error
```bash
# Update Railway ALLOWED_ORIGINS
ALLOWED_ORIGINS=https://your-app.vercel.app
railway up --detach
```

### 500 Error
```bash
# Check logs
railway logs --service backend

# Common fixes
- Verify DATABASE_URL is set
- Check SERVICE_KEY is present
- Ensure USE_DATABASE=true
```

### Build Failed
```bash
# Vercel
vercel --prod --force

# Railway
railway up --detach
```

## Monitoring

### UptimeRobot Setup

1. Create account: https://uptimerobot.com
2. Add monitor: `https://your-backend.railway.app/health`
3. Set interval: 5 minutes
4. Add alerts: Email/SMS

### View Logs

```bash
# Railway
railway logs --follow

# Vercel
vercel logs --follow --production

# Docker
docker-compose -f docker-compose.prod.yml logs -f backend
```

## Backup & Restore

```bash
# Backup
./scripts/backup-database.sh

# Restore
./scripts/restore-database.sh
```

## Security Checklist

- [ ] Generate SECRET_KEY: `./scripts/generate-secret-key.sh`
- [ ] Update POSTGRES_PASSWORD
- [ ] Update REDIS_PASSWORD
- [ ] Configure ALLOWED_ORIGINS
- [ ] Enable 2FA on accounts
- [ ] Review SECURITY_REVIEW.md

## Cost Estimate

### Free Tier
- Vercel: 100 GB bandwidth
- Railway: $5 credit/month
- **Total**: $0-5/month

### Production
- Vercel Pro: $20/month
- Railway: $5-20/month
- **Total**: $25-40/month

## Documentation

| Document | Purpose | Time |
|----------|---------|------|
| [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) | Fast deployment | 30 min |
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Full guide | 2 hours |
| [PRODUCTION_CHECKLIST.md](./PRODUCTION_CHECKLIST.md) | Checklist | 1 hour |
| [MONITORING.md](./MONITORING.md) | Monitoring | 1 hour |
| [SECURITY_REVIEW.md](./SECURITY_REVIEW.md) | Security | 2 hours |

## Support

- Vercel: https://vercel.com/support
- Railway: https://railway.app/help
- GitHub Issues: Project repository

---

**Print this page** for quick reference during deployment.

**Last Updated**: 2026-02-07
