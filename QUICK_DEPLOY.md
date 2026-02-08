# Quick Deployment Guide

Fast-track guide to deploy the application to production in under 30 minutes.

## Prerequisites Checklist

- [ ] Vercel account created
- [ ] Railway account created
- [ ] GitHub repository ready
- [ ] API keys obtained (SERVICE_KEY, optional GEMINI_API_KEY)

---

## Deployment Steps

### Step 1: Deploy Backend to Railway (10 minutes)

```bash
# 1. Login to Railway
railway login

# 2. Navigate to backend
cd fastapi-backend

# 3. Initialize project
railway init

# 4. Add PostgreSQL
railway add postgresql

# 5. Add Redis
railway add redis

# 6. Set environment variables in Railway dashboard
# Go to: https://railway.app/dashboard → Variables
```

**Required Environment Variables**:
```env
SERVICE_KEY=your_ministry_api_key
USE_DATABASE=true
USE_REDIS=true
LOG_LEVEL=info
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-app.vercel.app
```

```bash
# 7. Deploy backend
railway up

# 8. Get deployment URL
railway open
# Copy URL: https://your-backend.railway.app
```

### Step 2: Deploy Frontend to Vercel (10 minutes)

```bash
# 1. Navigate to frontend
cd ../nextjs-frontend

# 2. Install Vercel CLI
npm install -g vercel

# 3. Login to Vercel
vercel login

# 4. Deploy to Vercel
vercel --prod
```

**During deployment, set these environment variables**:
```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_APP_NAME=Korean Apartment Transaction Analysis
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### Step 3: Update CORS (5 minutes)

```bash
# 1. Get your Vercel URL from deployment output
# Example: https://your-app.vercel.app

# 2. Update Railway environment variables
# Go to: Railway Dashboard → Variables
# Update ALLOWED_ORIGINS:
ALLOWED_ORIGINS=https://your-app.vercel.app

# 3. Redeploy backend
cd fastapi-backend
railway up --detach
```

### Step 4: Verify Deployment (5 minutes)

```bash
# 1. Test frontend health
curl https://your-app.vercel.app/api/health

# 2. Test backend health
curl https://your-backend.railway.app/health

# 3. Test API endpoint
curl https://your-backend.railway.app/api/v1/analysis/stats

# 4. Open in browser
open https://your-app.vercel.app
```

---

## Verification Checklist

- [ ] Frontend loads successfully
- [ ] Backend health check returns 200 OK
- [ ] API calls work from frontend
- [ ] No CORS errors in browser console
- [ ] Data displays correctly
- [ ] All tabs functional

---

## Troubleshooting

### CORS Errors

**Problem**: `Access to fetch at 'https://...' has been blocked by CORS policy`

**Solution**:
1. Check `ALLOWED_ORIGINS` in Railway includes your Vercel URL
2. Restart backend: `railway up --detach`
3. Clear browser cache

### 500 Server Errors

**Problem**: Backend returns 500 errors

**Solution**:
```bash
# Check backend logs
railway logs --service backend

# Common issues:
# - DATABASE_URL not set (Railway auto-sets this)
# - SERVICE_KEY missing
# - Database connection timeout
```

### Frontend Not Loading

**Problem**: Vercel deployment shows error

**Solution**:
```bash
# Check build logs
vercel logs --production

# Redeploy
vercel --prod --force
```

---

## Post-Deployment

### Set Up Monitoring (Optional, 10 minutes)

1. **UptimeRobot**:
   - Go to https://uptimerobot.com
   - Add monitor for: `https://your-app.vercel.app/api/health`
   - Add monitor for: `https://your-backend.railway.app/health`
   - Set interval: 5 minutes
   - Add email alerts

2. **Vercel Analytics** (Free):
   - Go to Vercel Dashboard → Project → Analytics
   - Enable Analytics
   - View real-time traffic

3. **Railway Logs**:
   ```bash
   # Monitor logs in real-time
   railway logs --follow
   ```

---

## Next Steps

1. **Custom Domain** (Optional):
   - Add domain in Vercel: Settings → Domains
   - Update `ALLOWED_ORIGINS` in Railway
   - Configure DNS

2. **Security Review**:
   - Review [SECURITY_REVIEW.md](./SECURITY_REVIEW.md)
   - Rotate default passwords
   - Enable 2FA on accounts

3. **Performance Optimization**:
   - Enable Redis caching
   - Add database indexes
   - Monitor response times

4. **Backup Strategy**:
   - Configure automated database backups
   - Test backup restoration

---

## Cost Estimate

### Free Tier (Getting Started)

- **Vercel**: Free tier includes:
  - Unlimited deployments
  - 100 GB bandwidth/month
  - Serverless functions

- **Railway**: Free tier includes:
  - $5 credit/month
  - 500 hours execution time
  - PostgreSQL and Redis included

**Total**: $0-5/month for low traffic

### Production Tier (Paid)

- **Vercel Pro**: $20/month
  - 1 TB bandwidth
  - Advanced analytics
  - Password protection

- **Railway**: Pay as you go
  - $5-20/month (typical)
  - Scales with usage
  - Includes database and cache

**Total**: $25-40/month for production

---

## Quick Commands Reference

```bash
# Railway Commands
railway login              # Login to Railway
railway init               # Initialize project
railway up                 # Deploy application
railway logs               # View logs
railway logs --follow      # Follow logs
railway run bash           # SSH into container
railway open               # Open project in browser

# Vercel Commands
vercel login               # Login to Vercel
vercel                     # Deploy (preview)
vercel --prod              # Deploy to production
vercel logs                # View logs
vercel logs --follow       # Follow logs
vercel env pull            # Pull environment variables

# Health Checks
curl https://your-app.vercel.app/api/health
curl https://your-backend.railway.app/health

# API Testing
curl https://your-backend.railway.app/api/v1/analysis/stats
curl https://your-backend.railway.app/api/v1/analysis/by-region
```

---

## Support

- **Railway**: https://railway.app/help
- **Vercel**: https://vercel.com/support
- **Project Issues**: GitHub Issues

---

**Deployment Time**: ~30 minutes

**Difficulty**: Beginner-friendly

**Last Updated**: 2026-02-07
