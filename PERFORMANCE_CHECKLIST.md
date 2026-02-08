# Performance Optimization Checklist

Quick reference checklist for performance verification and monitoring.

## Pre-Deployment Checklist

### Frontend (Next.js)

- [ ] **Build and verify bundle sizes**
  ```bash
  cd nextjs-frontend
  npm run build
  ```
  - [ ] Base bundle < 102KB ✅
  - [ ] Each page < 260KB ✅
  - [ ] No build errors

- [ ] **Analyze bundle composition**
  ```bash
  npm run analyze
  ```
  - [ ] No packages > 100KB
  - [ ] No duplicate dependencies
  - [ ] No unused code detected

- [ ] **Verify font optimization**
  - [ ] Using next/font for Google fonts ✅
  - [ ] Only loading required weights (400, 500, 700) ✅
  - [ ] Font display set to 'swap' ✅

- [ ] **Check image optimization**
  - [ ] All images use next/image component
  - [ ] Blur placeholders configured (if using images)
  - [ ] Image domains configured in next.config.ts

- [ ] **Review caching strategy**
  - [ ] TanStack Query staleTime appropriate (5min) ✅
  - [ ] gcTime configured (10min) ✅
  - [ ] Structural sharing enabled ✅

### Backend (FastAPI)

- [ ] **Run API benchmarks**
  ```bash
  cd fastapi-backend
  python benchmark_api.py
  ```
  - [ ] All endpoints P50 < 200ms
  - [ ] All endpoints P95 < 500ms
  - [ ] No errors in test suite

- [ ] **Verify Redis connection**
  ```bash
  python -m backend.cache.cache_manager ping
  ```
  - [ ] Connection successful
  - [ ] Read/write test passes

- [ ] **Check cache statistics**
  ```bash
  python -m backend.cache.cache_manager stats
  ```
  - [ ] Hit rate > 80%
  - [ ] Error count < 1%
  - [ ] Redis server responsive

- [ ] **Warm cache**
  ```bash
  python cache_warming.py --full
  ```
  - [ ] All endpoints warmed successfully
  - [ ] No errors reported

- [ ] **Verify compression**
  - [ ] GZipMiddleware added to main.py ✅
  - [ ] Middleware order correct (compression first) ✅
  - [ ] Test response headers include Content-Encoding: gzip

- [ ] **Database optimization**
  - [ ] Required indexes created (see DATABASE_OPTIMIZATION.md)
  - [ ] Connection pool configured (20+10)
  - [ ] Query profiling enabled in development

### Environment Variables

- [ ] **Frontend (.env.local)**
  ```bash
  NEXT_PUBLIC_API_URL=http://localhost:8000
  # No ANALYZE variable (only set during npm run analyze)
  ```

- [ ] **Backend (.env)**
  ```bash
  USE_DATABASE=false  # or true for PostgreSQL
  USE_REDIS=true      # Enable Redis caching
  REDIS_URL=redis://localhost:6379/0
  WARM_CACHE_ON_STARTUP=true  # Pre-populate cache
  LOG_LEVEL=info
  ```

## Post-Deployment Monitoring

### Daily Checks

- [ ] **Monitor API performance**
  ```bash
  python benchmark_api.py --output daily_benchmark.json
  ```
  - [ ] Compare with baseline
  - [ ] Identify regression

- [ ] **Check cache health**
  ```bash
  python -m backend.cache.cache_manager stats
  ```
  - [ ] Hit rate stable
  - [ ] No error spike

### Weekly Checks

- [ ] **Bundle analysis**
  ```bash
  npm run analyze
  ```
  - [ ] Review new dependencies
  - [ ] Check for bundle bloat

- [ ] **Full API benchmark**
  ```bash
  python benchmark_api.py --requests 100 --output weekly_benchmark.json
  ```
  - [ ] All endpoints within budget
  - [ ] No performance degradation

- [ ] **Database query review**
  - [ ] Check slow query logs
  - [ ] Review missing indexes
  - [ ] Verify connection pool usage

### Monthly Checks

- [ ] **Dependency updates**
  ```bash
  npm outdated
  pip list --outdated
  ```
  - [ ] Security updates applied
  - [ ] Performance improvements noted

- [ ] **Performance budget review**
  - [ ] Frontend: Bundle size trends
  - [ ] Backend: API response time trends
  - [ ] Cache: Hit rate trends

- [ ] **Lighthouse audit**
  - [ ] Performance > 90
  - [ ] Accessibility > 95
  - [ ] Best Practices > 95
  - [ ] SEO > 90

## Performance Targets

### Must Meet (P0)

- [ ] Frontend bundle size (gzipped) < 300KB per page
- [ ] API response time (P95) < 500ms
- [ ] Cache hit rate > 80%
- [ ] Zero critical errors in production

### Should Meet (P1)

- [ ] Frontend bundle size (gzipped) < 150KB per page
- [ ] API response time (P95) < 300ms
- [ ] Cache hit rate > 90%
- [ ] Page load time < 2s

### Nice to Have (P2)

- [ ] Frontend bundle size (gzipped) < 100KB per page
- [ ] API response time (P95) < 200ms
- [ ] Cache hit rate > 95%
- [ ] Page load time < 1s

## Tools Quick Reference

| Task | Command |
|------|---------|
| Build frontend | `npm run build` |
| Analyze bundle | `npm run analyze` |
| Benchmark API | `python benchmark_api.py` |
| Cache stats | `python -m backend.cache.cache_manager stats` |
| Warm cache | `python cache_warming.py --full` |
| Clear cache | `python -m backend.cache.cache_manager clear` |
| Test Redis | `python -m backend.cache.cache_manager ping` |

## Troubleshooting Quick Fixes

### Frontend Slow

1. Check bundle: `npm run analyze`
2. Verify API times in Network tab
3. Check TanStack Query cache in React DevTools
4. Review console for errors

### API Slow

1. Check cache: `python -m backend.cache.cache_manager stats`
2. Verify Redis: `python -m backend.cache.cache_manager ping`
3. Run benchmark: `python benchmark_api.py`
4. Check database indexes

### Low Cache Hit Rate

1. Increase TanStack Query staleTime
2. Verify Redis TTL settings
3. Enable cache warming: `WARM_CACHE_ON_STARTUP=true`
4. Check cache key consistency

### Large Bundle

1. Run `npm run analyze`
2. Check for duplicate dependencies
3. Use dynamic imports for heavy components
4. Consider package alternatives

## Documentation Reference

- [PERFORMANCE.md](/Users/koscom/Downloads/apt_test/PERFORMANCE.md) - Complete guide
- [PERFORMANCE_QUICKSTART.md](/Users/koscom/Downloads/apt_test/PERFORMANCE_QUICKSTART.md) - Quick start
- [DATABASE_OPTIMIZATION.md](/Users/koscom/Downloads/apt_test/fastapi-backend/DATABASE_OPTIMIZATION.md) - Database guide
- [PERFORMANCE_OPTIMIZATION_SUMMARY.md](/Users/koscom/Downloads/apt_test/PERFORMANCE_OPTIMIZATION_SUMMARY.md) - Implementation summary

## Sign-off Template

```
Performance Review: YYYY-MM-DD

Frontend:
- [ ] Bundle size: XXX KB (target: < 300KB)
- [ ] Build time: XXX s (target: < 10s)
- [ ] Lighthouse score: XXX/100 (target: > 90)

Backend:
- [ ] API P95: XXX ms (target: < 500ms)
- [ ] Cache hit rate: XX% (target: > 80%)
- [ ] Error rate: X% (target: < 1%)

Status: ✅ PASS / ❌ FAIL
Issues: None / [list issues]
Action items: None / [list actions]

Reviewer: [name]
Date: [date]
```

---

**Current Status**: ✅ All optimizations implemented and verified
**Last Updated**: 2026-02-07
