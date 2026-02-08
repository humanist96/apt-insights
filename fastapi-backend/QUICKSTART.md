# FastAPI Backend - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
cd fastapi-backend
pip install -r requirements.txt
```

### Step 2: Start the Server

**Option A: Using Python directly**
```bash
python main.py
```

**Option B: Using the startup script**
```bash
chmod +x start.sh
./start.sh
```

**Option C: Using uvicorn directly**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Verify Server is Running

Open your browser and visit:
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

You should see the interactive API documentation.

## First API Calls

### Using Swagger UI (Easiest)

1. Go to http://localhost:8000/docs
2. Click on any endpoint (e.g., `POST /api/v1/analysis/basic-stats`)
3. Click "Try it out"
4. Click "Execute"
5. See the response below

### Using curl

**1. Health Check**
```bash
curl http://localhost:8000/health
```

**2. Basic Statistics (All Data)**
```bash
curl -X POST http://localhost:8000/api/v1/analysis/basic-stats \
  -H "Content-Type: application/json" \
  -d '{}'
```

**3. Basic Statistics (Filtered by Region)**
```bash
curl -X POST http://localhost:8000/api/v1/analysis/basic-stats \
  -H "Content-Type: application/json" \
  -d '{"region_filter": "강남구"}'
```

**4. Price Trend Analysis**
```bash
curl -X POST http://localhost:8000/api/v1/analysis/price-trend \
  -H "Content-Type: application/json" \
  -d '{
    "region_filter": "강남구",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  }'
```

**5. Regional Analysis (Top 5)**
```bash
curl -X POST http://localhost:8000/api/v1/analysis/regional \
  -H "Content-Type: application/json" \
  -d '{"top_n": 5}'
```

**6. Clear Cache**
```bash
curl -X POST http://localhost:8000/api/v1/analysis/cache/clear
```

### Using Python requests

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Basic stats
response = requests.post(
    f"{BASE_URL}/api/v1/analysis/basic-stats",
    json={"region_filter": "강남구"}
)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### Using JavaScript fetch

```javascript
const BASE_URL = "http://localhost:8000";

async function getBasicStats() {
  const response = await fetch(`${BASE_URL}/api/v1/analysis/basic-stats`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      region_filter: '강남구'
    })
  });

  const data = await response.json();
  console.log(data);
}

getBasicStats();
```

## Running Tests

```bash
# Make sure server is running first
python test_api.py
```

Expected output:
```
========================================
FastAPI Backend Test Suite
========================================
...
✅ Health Check - PASSED
✅ Root Endpoint - PASSED
✅ Basic Stats (All) - PASSED
...
========================================
Test Results: 8 passed, 0 failed
========================================
```

## Understanding the Response Format

All successful responses follow this structure:

```json
{
  "success": true,
  "data": {
    // Endpoint-specific data here
  },
  "meta": {
    "total_records": 63809,
    "filtered_records": 1234,
    "data_source": "postgresql",
    "timestamp": "2026-02-07T12:00:00",
    "processing_time_ms": 45.23
  }
}
```

Error responses:

```json
{
  "success": false,
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## Common Use Cases

### 1. Get Overall Market Statistics

```bash
curl -X POST http://localhost:8000/api/v1/analysis/basic-stats \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Returns:**
- Total transaction count
- Average, min, max, median prices
- Average area
- Breakdown by region

### 2. Analyze Price Trends for Specific Area

```bash
curl -X POST http://localhost:8000/api/v1/analysis/price-trend \
  -H "Content-Type: application/json" \
  -d '{
    "region_filter": "강남구",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  }'
```

**Returns:**
- Monthly price trends
- Overall trend direction (increasing/decreasing/stable)
- Price change percentage

### 3. Compare Multiple Regions

```bash
curl -X POST http://localhost:8000/api/v1/analysis/regional \
  -H "Content-Type: application/json" \
  -d '{
    "regions": ["강남구", "서초구", "송파구"],
    "top_n": 3
  }'
```

**Returns:**
- Statistics for each region
- Sorted by average price
- Top region identifier

### 4. Filter by Date Range

```bash
curl -X POST http://localhost:8000/api/v1/analysis/basic-stats \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2023-06-01",
    "end_date": "2023-12-31"
  }'
```

**Returns:**
- Statistics for transactions in date range
- Works with any analysis endpoint

## Troubleshooting

### Server won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Connection refused

**Error:** `Connection refused at http://localhost:8000`

**Solution:**
- Make sure the server is running
- Check if port 8000 is already in use
- Try a different port: `uvicorn main:app --port 8001`

### No data returned

**Error:** `"total_count": 0`

**Solution:**
- Check if JSON files exist in `../api_*/output/` directories
- Or set `USE_DATABASE=true` in parent `.env` file
- Make sure you're running from `fastapi-backend/` directory

### Import errors

**Error:** `ModuleNotFoundError: No module named 'backend'`

**Solution:**
- The backend automatically adds parent directory to sys.path
- Make sure you're running from `fastapi-backend/` directory
- Check that `../backend/` directory exists

### Validation errors

**Error:** `422 Unprocessable Entity`

**Solution:**
- Check request body format
- Dates must be in YYYY-MM-DD format
- top_n must be between 1 and 100
- See Swagger UI for exact schema requirements

## Environment Variables

The backend automatically inherits settings from parent `.env`:

```bash
# In parent directory (apt_test/)
USE_DATABASE=true   # Use PostgreSQL (requires setup)
USE_DATABASE=false  # Use JSON files (default)
```

No additional configuration needed for basic operation.

## Performance Tips

1. **First request is slow**: Data loading takes time (cache miss)
2. **Subsequent requests are fast**: 5-minute cache active
3. **Clear cache**: Use `/cache/clear` endpoint after data updates
4. **Filter early**: Use region/date filters to reduce processing time
5. **PostgreSQL is faster**: Set USE_DATABASE=true for better performance

## Next Steps

1. **Explore Swagger UI**: http://localhost:8000/docs
   - Interactive documentation
   - Try all endpoints
   - See request/response schemas

2. **Read the README**: Full API documentation
   - Detailed endpoint descriptions
   - Request/response examples
   - Integration guides

3. **Check Architecture**: ARCHITECTURE.md
   - System design
   - Data flow diagrams
   - Design patterns

4. **Add More Endpoints**: 20 analyzer functions available
   - See `backend/analyzer.py` for full list
   - Follow contribution guidelines in ARCHITECTURE.md

## Support

For issues or questions:
1. Check Swagger UI documentation: http://localhost:8000/docs
2. Review logs in console output
3. Check `backend/analyzer.py` for available functions
4. See ARCHITECTURE.md for system design details

## Quick Reference Card

| Task | Command |
|------|---------|
| Start server | `python main.py` |
| View docs | http://localhost:8000/docs |
| Health check | `curl http://localhost:8000/health` |
| Run tests | `python test_api.py` |
| Clear cache | `curl -X POST http://localhost:8000/api/v1/analysis/cache/clear` |

| Endpoint | Purpose |
|----------|---------|
| `/health` | Server health check |
| `/api/v1/analysis/basic-stats` | Basic statistics |
| `/api/v1/analysis/price-trend` | Price trends over time |
| `/api/v1/analysis/regional` | Regional comparison |
| `/api/v1/analysis/cache/clear` | Clear data cache |

**Happy API building!** 🚀
