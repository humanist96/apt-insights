# Quick Start Guide - Premium Features

## Prerequisites

1. **Redis** - Required for usage tracking
2. **Python 3.9+** - Backend
3. **Node.js 18+** - Frontend

## Step 1: Start Redis

```bash
# macOS (using Homebrew)
brew services start redis

# Or using Docker
docker run -d -p 6379:6379 redis:latest

# Verify Redis is running
redis-cli ping
# Should return: PONG
```

## Step 2: Start Backend

```bash
cd /Users/koscom/Downloads/apt_test/fastapi-backend

# Set environment variables
export USE_REDIS=true
export REDIS_URL=redis://localhost:6379/0

# Start server
python3 -m uvicorn main:app --reload --port 8000

# Should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

## Step 3: Start Frontend

```bash
cd /Users/koscom/Downloads/apt_test/nextjs-frontend

# Install dependencies (if not done)
npm install

# Start dev server
npm run dev

# Should see:
# ▲ Next.js 14.x.x
# - Local:        http://localhost:3000
```

## Step 4: Test Premium Features

### 1. View Subscription Plans

Visit: http://localhost:3000/subscription

You should see:
- Free plan (current plan)
- Premium plan with "프리미엄 시작하기" button
- Usage statistics showing "0/10 API calls"

### 2. Check Usage Indicator

Look at the header - you should see:
- Green badge: "API: 0/10"

### 3. Make API Calls

Visit any analysis page (e.g., http://localhost:3000/regional)
- Each page load counts as 1 API call
- Watch the header counter increase
- After 10 calls, you'll see rate limit error

### 4. Upgrade to Premium (Mock)

1. Go to http://localhost:3000/subscription
2. Click "프리미엄 시작하기" button
3. Should see success message
4. Header now shows "무제한" badge
5. No more rate limiting

### 5. Test CSV Export

1. Go to http://localhost:3000/detail-data
2. As free user: CSV button shows "Premium" badge and is locked
3. Click it to see upgrade modal
4. Upgrade to premium
5. CSV button now works - click to download

### 6. Test PDF Export (Mock)

1. Click "PDF 내보내기" button
2. Should see alert: "PDF 생성 중입니다..."
3. Real implementation coming soon

### 7. Cancel Subscription

1. Go to http://localhost:3000/subscription
2. Click "구독 취소" button
3. Confirm cancellation
4. Tier reverts to "무료"
5. Rate limiting reactivates

## API Testing with cURL

### Get Subscription Plans

```bash
curl http://localhost:8000/api/v1/subscriptions/plans | jq
```

### Get Current Subscription

```bash
curl http://localhost:8000/api/v1/subscriptions/current \
  -H "X-User-Id: demo_user" | jq
```

### Make API Calls (Test Rate Limit)

```bash
# Make 11 requests quickly
for i in {1..11}; do
  echo "Request $i:"
  curl -X POST http://localhost:8000/api/v1/analysis/basic-stats \
    -H "Content-Type: application/json" \
    -H "X-User-Id: demo_user" \
    -d '{}' \
    -w "\nHTTP Status: %{http_code}\n" \
    -s | grep -E "(HTTP Status|rate_limit|remaining)"
  echo "---"
  sleep 0.5
done

# Request 11 should return 429 Too Many Requests
```

### Upgrade to Premium

```bash
curl -X POST http://localhost:8000/api/v1/subscriptions/upgrade \
  -H "Content-Type: application/json" \
  -H "X-User-Id: demo_user" \
  -d '{"plan_id": "premium"}' | jq
```

### Export CSV

```bash
# As free user (should fail)
curl -X POST http://localhost:8000/api/v1/export/csv \
  -H "Content-Type: application/json" \
  -H "X-User-Id: free_user" \
  -d '{"export_type": "csv"}' \
  --output test.csv

# As premium user (should succeed)
curl -X POST http://localhost:8000/api/v1/export/csv \
  -H "Content-Type: application/json" \
  -H "X-User-Id: demo_user" \
  -d '{"export_type": "csv"}' \
  --output test.csv
```

### Check Usage Stats

```bash
curl http://localhost:8000/api/v1/subscriptions/usage \
  -H "X-User-Id: demo_user" | jq
```

## Troubleshooting

### Redis Not Running

**Error:** `usage_tracking_connection_failed`

**Solution:**
```bash
brew services start redis
# or
docker run -d -p 6379:6379 redis:latest
```

### Rate Limiting Not Working

**Check:**
1. Is Redis running? `redis-cli ping`
2. Is `USE_REDIS=true` set? `echo $USE_REDIS`
3. Check backend logs for connection errors

**Solution:**
```bash
export USE_REDIS=true
export REDIS_URL=redis://localhost:6379/0
# Restart backend
```

### Frontend Can't Connect to Backend

**Error:** `Network Error` or `CORS Error`

**Check:**
1. Is backend running? Visit http://localhost:8000/docs
2. Is `NEXT_PUBLIC_API_URL` set correctly?

**Solution:**
```bash
# In nextjs-frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
# Restart frontend
```

### Usage Counter Not Updating

**Check:**
1. Open browser DevTools → Network tab
2. Look for `X-RateLimit-*` headers in responses
3. Check if API calls are actually being made

**Solution:**
- Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
- Clear browser cache
- Check subscription context is loaded

### Upgrade Button Not Working

**Check:**
1. Open browser console for errors
2. Check Network tab for API call
3. Verify response shows success

**Solution:**
- Check backend logs for errors
- Try direct API call with cURL
- Verify subscription context is available

## Development Tips

### Reset Usage Counter

```bash
# Connect to Redis
redis-cli

# List all keys
KEYS apt_insights:usage:*

# Delete specific user's usage
DEL apt_insights:usage:demo_user:2026-02-08

# Delete all usage data
KEYS apt_insights:usage:* | xargs redis-cli DEL
```

### Monitor Redis in Real-Time

```bash
# Terminal 1: Monitor all Redis commands
redis-cli MONITOR

# Terminal 2: Make API calls and watch Redis activity
```

### Check Backend Logs

```bash
# Backend shows structured logs
# Look for:
# - "rate_limit_exceeded" - User hit limit
# - "usage_incremented" - API call counted
# - "subscription_upgraded" - User upgraded
# - "csv_export_requested" - Export requested
```

### Test Different Users

```bash
# Create multiple test users by changing X-User-Id header
curl http://localhost:8000/api/v1/subscriptions/current \
  -H "X-User-Id: user1" | jq

curl http://localhost:8000/api/v1/subscriptions/current \
  -H "X-User-Id: user2" | jq

# Each user has separate usage counter
```

## What's Working

✅ **Backend:**
- Subscription management endpoints
- Rate limiting with Redis
- Usage tracking with daily reset
- CSV export (real)
- PDF export (mock)
- Premium feature checks

✅ **Frontend:**
- Subscription page with plan comparison
- Usage indicator in header
- Premium badges and gates
- Upgrade modal
- Export buttons
- Subscription context

✅ **Integration:**
- Rate limit headers in responses
- 429 error handling
- Premium access checks
- Subscription state management

## What's Mock

⚠️ **Not Real Yet:**
- Payment processing (instant upgrade)
- User database (in-memory)
- PDF generation (shows message only)
- CSV data (uses sample data)
- Authentication (header-based only)

## Next Steps

1. **Try the demo** - Follow steps 1-7 above
2. **Test rate limiting** - Make 11 API calls
3. **Test premium features** - Upgrade and export
4. **Review the code** - See implementation details
5. **Extend as needed** - Add real payment, PDF, etc.

## Support

If you encounter issues:
1. Check backend logs
2. Check browser console
3. Verify Redis is running
4. Review troubleshooting section above
5. Check `/PREMIUM_FEATURES_IMPLEMENTATION.md` for details

## Success Criteria

✅ You're ready when:
- Subscription page loads with plan comparison
- Usage indicator appears in header
- Rate limiting kicks in after 10 calls
- Upgrade changes tier to premium
- Export buttons show premium gates
- CSV export downloads file
- Everything works smoothly!

Enjoy the premium features! 🎉
