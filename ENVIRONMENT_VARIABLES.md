# Environment Variables Reference

Complete reference for all environment variables used in the Korean Apartment Transaction Analysis Platform.

---

## Table of Contents

- [GitHub Actions Secrets](#github-actions-secrets)
- [FastAPI Backend Variables](#fastapi-backend-variables)
- [Next.js Frontend Variables](#nextjs-frontend-variables)
- [Docker Compose Variables](#docker-compose-variables)
- [Railway Auto-Injected Variables](#railway-auto-injected-variables)
- [Vercel Auto-Injected Variables](#vercel-auto-injected-variables)

---

## GitHub Actions Secrets

These must be configured in **GitHub > Settings > Secrets and variables > Actions**.

### Deployment Secrets

| Secret | Required | Description | How to Obtain |
|--------|----------|-------------|---------------|
| `RAILWAY_TOKEN` | Yes | Railway API authentication token | Railway Dashboard > Account Settings > Tokens > Create Token |
| `RAILWAY_DATABASE_URL` | Yes | PostgreSQL connection URL on Railway | Railway Dashboard > PostgreSQL Service > Connect > Connection URL |
| `VERCEL_TOKEN` | Yes | Vercel API authentication token | Vercel Dashboard > Settings > Tokens > Create Token |
| `VERCEL_ORG_ID` | Yes | Vercel organization/team ID | Run `vercel whoami` or check `.vercel/project.json` after `vercel link` |
| `VERCEL_PROJECT_ID` | Yes | Vercel project identifier | Run `vercel link` and check `.vercel/project.json` |

### Setting Up via GitHub CLI

```bash
# Railway
gh secret set RAILWAY_TOKEN
gh secret set RAILWAY_DATABASE_URL

# Vercel
gh secret set VERCEL_TOKEN
gh secret set VERCEL_ORG_ID
gh secret set VERCEL_PROJECT_ID
```

---

## FastAPI Backend Variables

File: `fastapi-backend/.env` (local) or Railway Dashboard (production)

### API Keys (Required)

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVICE_KEY` | - | Korean Ministry of Land public data API service key. Obtain from [data.go.kr](https://www.data.go.kr/) |
| `GEMINI_API_KEY` | - | Google Gemini API key for AI-powered insights. Optional. Obtain from [Google AI Studio](https://aistudio.google.com/) |

### Database Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_DATABASE` | `false` | Enable PostgreSQL database. Set to `true` in production |
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/apt_insights` | PostgreSQL connection string. Format: `postgresql://user:password@host:port/database` |
| `DB_POOL_SIZE` | `20` | SQLAlchemy connection pool size |
| `DB_MAX_OVERFLOW` | `10` | Maximum overflow connections beyond pool size |
| `DB_POOL_TIMEOUT` | `30` | Seconds to wait for a connection from the pool |
| `DB_POOL_RECYCLE` | `3600` | Seconds before a connection is recycled |
| `SQL_ECHO` | `false` | Log all SQL queries. Set to `false` in production |

### Redis Cache Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_REDIS` | `false` | Enable Redis caching. Set to `true` in production |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection URL. Format: `redis://:password@host:port/db` |
| `CACHE_TTL_SHORT` | `300` | Short cache TTL in seconds (5 minutes) |
| `CACHE_TTL_MEDIUM` | `1800` | Medium cache TTL in seconds (30 minutes) |
| `CACHE_TTL_LONG` | `3600` | Long cache TTL in seconds (1 hour) |

### Server Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port. Railway overrides this automatically |
| `WORKERS` | `4` | Number of Uvicorn worker processes |
| `ENVIRONMENT` | `development` | Environment name: `development`, `staging`, `production`, `test` |

### Security Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | - | JWT signing key. Minimum 32 characters. Generate with: `openssl rand -hex 32` |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | CORS allowed origins. Comma-separated list of frontend URLs |
| `API_KEY_HEADER` | `X-API-Key` | Header name for API key authentication |
| `RATE_LIMIT_ENABLED` | `true` | Enable request rate limiting |
| `RATE_LIMIT_REQUESTS` | `100` | Maximum requests per window |
| `RATE_LIMIT_WINDOW` | `60` | Rate limit window in seconds |

### Logging Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `info` | Logging level: `debug`, `info`, `warning`, `error`, `critical` |
| `LOG_FORMAT` | `json` | Log output format: `json` (production) or `console` (development) |
| `DEBUG` | `false` | Enable debug mode. Never enable in production |

### Feature Flags

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_DOCS` | `true` | Enable Swagger/ReDoc API documentation endpoints |
| `ENABLE_METRICS` | `true` | Enable application metrics collection |
| `ENABLE_PROFILING` | `false` | Enable performance profiling |
| `WARM_CACHE_ON_STARTUP` | `false` | Pre-warm Redis cache on application startup |

### External API Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `API_REQUEST_TIMEOUT` | `30` | External API request timeout in seconds |
| `API_MAX_RETRIES` | `3` | Maximum retry attempts for failed API requests |
| `API_RETRY_DELAY` | `1` | Delay between retries in seconds |

### Monitoring (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `SENTRY_DSN` | - | Sentry error tracking DSN. Obtain from [sentry.io](https://sentry.io/) |
| `APP_INSIGHTS_KEY` | - | Application Insights instrumentation key |

### Payment Configuration (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `PORTONE_API_KEY` | - | PortOne payment gateway API key |
| `PORTONE_API_SECRET` | - | PortOne payment gateway API secret |
| `PORTONE_MERCHANT_ID` | - | PortOne merchant identifier |

---

## Next.js Frontend Variables

File: `nextjs-frontend/.env.local` (local) or Vercel Dashboard (production)

**Note:** Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. Never put secrets in `NEXT_PUBLIC_` variables.

### API Configuration (Required)

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | FastAPI backend URL. Must be the full URL including protocol |

### Application Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_APP_NAME` | `Korean Apartment Transaction Analysis Platform` | Application display name |
| `NEXT_PUBLIC_APP_VERSION` | `1.0.0` | Application version string |
| `NEXT_PUBLIC_APP_DESCRIPTION` | `Real-time apartment transaction data analysis and insights` | Application description for meta tags |

### Feature Flags

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_ENABLE_ANALYTICS` | `false` | Enable frontend analytics tracking |
| `NEXT_PUBLIC_ENABLE_DEBUG` | `false` | Enable debug panel in UI |

### API Client Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_TIMEOUT` | `30000` | API request timeout in milliseconds |
| `NEXT_PUBLIC_API_RETRY_COUNT` | `3` | Number of retry attempts for failed API calls |

### Build Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `NODE_ENV` | `development` | Node environment: `development`, `production`, `test` |
| `NEXT_TELEMETRY_DISABLED` | `1` | Disable Next.js telemetry data collection |
| `ANALYZE` | `false` | Enable webpack bundle analyzer output |

---

## Docker Compose Variables

File: `.env.production` (project root)

These variables are used by `docker-compose.prod.yml` for self-hosted deployments.

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_DB` | `apt_insights` | PostgreSQL database name |
| `POSTGRES_USER` | `postgres` | PostgreSQL username |
| `POSTGRES_PASSWORD` | - | PostgreSQL password. Use a strong password |
| `REDIS_PASSWORD` | - | Redis authentication password |

---

## Railway Auto-Injected Variables

These are automatically provided by Railway and should not be set manually.

| Variable | Description |
|----------|-------------|
| `PORT` | Application port assigned by Railway |
| `DATABASE_URL` | PostgreSQL connection string (from Railway PostgreSQL plugin) |
| `REDIS_URL` | Redis connection string (from Railway Redis plugin) |
| `RAILWAY_ENVIRONMENT` | Railway environment name |
| `RAILWAY_PROJECT_NAME` | Railway project name |
| `RAILWAY_SERVICE_NAME` | Railway service name |
| `RAILWAY_STATIC_URL` | Static URL for the service |

---

## Vercel Auto-Injected Variables

These are automatically provided by Vercel at build/runtime.

| Variable | Description |
|----------|-------------|
| `VERCEL` | Set to `1` when running on Vercel |
| `VERCEL_ENV` | Environment: `production`, `preview`, `development` |
| `VERCEL_URL` | Deployment URL (without protocol) |
| `VERCEL_REGION` | Deployment region (e.g., `icn1` for Seoul) |
| `VERCEL_GIT_COMMIT_SHA` | Git commit SHA that triggered the build |
| `VERCEL_GIT_COMMIT_MESSAGE` | Git commit message |
| `VERCEL_GIT_REPO_SLUG` | Repository slug |

---

## Environment Setup Quick Reference

### Local Development

```bash
# 1. Copy example files
cp .env.example .env
cp fastapi-backend/.env.example fastapi-backend/.env
cp nextjs-frontend/.env.production.example nextjs-frontend/.env.local

# 2. Edit with your actual values
# - Set SERVICE_KEY (required for API calls)
# - Set DATABASE_URL if using PostgreSQL locally
# - Set NEXT_PUBLIC_API_URL to http://localhost:8000
```

### CI/CD Pipeline (GitHub Actions)

```bash
# Set required secrets via GitHub CLI
gh secret set RAILWAY_TOKEN --body "<your-token>"
gh secret set RAILWAY_DATABASE_URL --body "<your-db-url>"
gh secret set VERCEL_TOKEN --body "<your-token>"
gh secret set VERCEL_ORG_ID --body "<your-org-id>"
gh secret set VERCEL_PROJECT_ID --body "<your-project-id>"
```

### Production (Railway + Vercel)

1. **Railway Dashboard** - Set all FastAPI Backend Variables
2. **Vercel Dashboard** - Set all Next.js Frontend Variables
3. **GitHub Secrets** - Set all deployment tokens

### Generating Secure Values

```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Generate POSTGRES_PASSWORD
openssl rand -base64 24

# Generate REDIS_PASSWORD
openssl rand -base64 24
```

---

**Last Updated**: 2026-02-08
