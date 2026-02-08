# FastAPI Backend - Apartment Transaction Analysis

RESTful API backend for Korean apartment real estate transaction analysis platform.

## Features

- **RESTful API** with FastAPI framework
- **Automatic API documentation** with Swagger UI and ReDoc
- **Pydantic validation** for request/response models
- **Structured logging** with structlog
- **CORS support** for frontend integration
- **Data caching** (5-minute TTL)
- **PostgreSQL integration** (auto-detects USE_DATABASE env var)
- **JSON fallback mode** for development

## Architecture

```
fastapi-backend/
├── main.py                  # FastAPI app entry point
├── routers/
│   ├── analysis.py          # Analysis endpoints (3)
│   ├── segmentation.py      # Segmentation endpoints (5)
│   ├── premium.py           # Premium analysis endpoints (4)
│   ├── investment.py        # Investment endpoints (3)
│   └── market.py            # Market signals endpoints (8)
├── schemas/
│   ├── requests.py          # Pydantic request models
│   └── responses.py         # Pydantic response models
├── services/
│   └── analyzer_service.py  # Business logic layer
├── middleware/
│   ├── cors.py              # CORS configuration
│   └── logging.py           # Logging middleware
├── test_new_endpoints.py    # Test script for all endpoints
├── API_ENDPOINTS.md         # Complete API documentation
└── requirements.txt         # Python dependencies
```

## Installation

### 1. Install Dependencies

```bash
cd fastapi-backend
pip install -r requirements.txt
```

### 2. Environment Variables

The backend automatically detects the `USE_DATABASE` environment variable from the parent project's `.env` file.

- `USE_DATABASE=true` → Load data from PostgreSQL
- `USE_DATABASE=false` → Load data from JSON files (default)

## Running the Server

### Development Mode (with auto-reload)

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Available Endpoints

**Total: 23 endpoints** across 5 categories

For complete API documentation, see [API_ENDPOINTS.md](./API_ENDPOINTS.md)

### Health & Info

- `GET /health` - Health check
- `GET /` - API information

### Analysis Endpoints (3)

Core analysis endpoints under `/api/v1/analysis`:

#### 1. Basic Statistics

**POST** `/api/v1/analysis/basic-stats`

Calculate basic statistics including count, average/min/max prices, and regional breakdown.

**Request:**
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_count": 1234,
    "avg_price": 120000,
    "max_price": 250000,
    "min_price": 50000,
    "median_price": 115000,
    "avg_area": 84.5,
    "regions": {
      "강남구 역삼동": {
        "count": 123,
        "avg_price": 130000,
        "max_price": 200000,
        "min_price": 80000
      }
    }
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

#### 2. Price Trend

**POST** `/api/v1/analysis/price-trend`

Analyze price trends over time with monthly aggregation.

**Request:**
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "group_by": "month"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "trend_data": [
      {
        "year_month": "2023-01",
        "count": 45,
        "avg_price": 115000,
        "max_price": 180000,
        "min_price": 70000,
        "median_price": 112000
      }
    ],
    "overall_trend": "increasing",
    "price_change_pct": 8.5
  },
  "meta": {
    "total_records": 63809,
    "filtered_records": 540,
    "data_source": "postgresql",
    "processing_time_ms": 67.89
  }
}
```

#### 3. Regional Analysis

**POST** `/api/v1/analysis/regional`

Compare statistics across different regions.

**Request:**
```json
{
  "regions": ["강남구", "서초구", "송파구"],
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "top_n": 10
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "regions": [
      {
        "region_name": "강남구 역삼동",
        "count": 123,
        "avg_price": 130000,
        "max_price": 200000,
        "min_price": 80000,
        "median_price": 125000,
        "total_volume": 15990000
      }
    ],
    "top_region": "강남구 역삼동",
    "total_regions": 10
  },
  "meta": {
    "total_records": 63809,
    "filtered_records": 450,
    "processing_time_ms": 52.11
  }
}
```

#### 4. Cache Management

**POST** `/api/v1/analysis/cache/clear`

Clear the in-memory data cache to force reload on next request.

**Response:**
```json
{
  "success": true,
  "message": "Cache cleared successfully",
  "timestamp": "2026-02-07T12:00:00"
}
```

### Segmentation Endpoints (5)

Under `/api/v1/analysis`:

5. **POST** `/by-area` - Analyze transactions by exclusive area size
6. **POST** `/by-floor` - Analyze by floor level (low/mid/high)
7. **POST** `/by-build-year` - Analyze by construction year
8. **POST** `/by-apartment` - Analyze by apartment complex
9. **POST** `/apartment-detail` - Get detailed info for specific apartment

### Premium Endpoints (4)

Under `/api/v1/premium`:

10. **POST** `/price-per-area` - Calculate price per area (평당가)
11. **POST** `/price-per-area-trend` - Price per area trends over time
12. **POST** `/floor-premium` - Floor premium analysis (low/mid/high)
13. **POST** `/building-age-premium` - Premium by building age

### Investment Endpoints (3)

Under `/api/v1/investment`:

14. **POST** `/jeonse-ratio` - Calculate jeonse ratio (전세가율)
15. **POST** `/gap-investment` - Gap investment opportunities
16. **POST** `/bargain-sales` - Detect bargain sales (급매물)

### Market Endpoints (8)

Under `/api/v1/market`:

17. **POST** `/rent-vs-jeonse` - Compare monthly rent vs jeonse
18. **POST** `/dealing-type` - Transaction type distribution
19. **POST** `/buyer-seller-type` - Buyer/seller type analysis
20. **POST** `/cancelled-deals` - Cancelled transaction patterns
21. **POST** `/period-summary` - Comprehensive period summary
22. **POST** `/baseline-summary` - Previous period baseline
23. **POST** `/compare-periods` - Period-over-period comparison
24. **POST** `/signals` - Detect market signals and anomalies

## Request Validation

All requests are validated using Pydantic models:

- **Date format**: `YYYY-MM-DD`
- **Region filter**: Optional string (partial match supported)
- **top_n**: Integer between 1 and 100

Invalid requests return a 422 Unprocessable Entity error with detailed validation messages.

## Error Handling

Standard error response format:

```json
{
  "success": false,
  "error": "Error message",
  "detail": "Detailed error information",
  "timestamp": "2026-02-07T12:00:00"
}
```

HTTP Status Codes:
- `200 OK` - Successful request
- `400 Bad Request` - Invalid request parameters
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Data Caching

The service implements an in-memory cache with:
- **TTL**: 5 minutes (configurable in `analyzer_service.py`)
- **Automatic invalidation**: Cache expires after TTL
- **Manual clearing**: Use `/api/v1/analysis/cache/clear` endpoint

## Logging

All requests are logged with:
- Request method and path
- Query parameters
- Processing time
- Response status code
- Errors (with stack traces)

Logs are structured JSON format using structlog.

## Integration with Backend

The FastAPI backend integrates with the existing backend modules:

- `backend.data_loader.load_all_json_data()` - Data loading
- `backend.analyzer.*` - Analysis functions (23 available)

The service layer (`analyzer_service.py`) wraps these functions and provides:
- Data caching
- Filter application (region, date range)
- Response formatting
- Error handling

## Testing

### Automated Tests

Run the comprehensive test suite:

```bash
python test_new_endpoints.py
```

This tests all 23 endpoints and provides a detailed report.

### Manual Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Basic stats (all data)
curl -X POST http://localhost:8000/api/v1/analysis/basic-stats \
  -H "Content-Type: application/json" \
  -d '{}'

# Basic stats (filtered by region)
curl -X POST http://localhost:8000/api/v1/analysis/basic-stats \
  -H "Content-Type: application/json" \
  -d '{"region_filter": "강남구"}'

# Price trend
curl -X POST http://localhost:8000/api/v1/analysis/price-trend \
  -H "Content-Type: application/json" \
  -d '{"region_filter": "강남구", "start_date": "2023-01-01", "end_date": "2023-12-31"}'

# Regional analysis
curl -X POST http://localhost:8000/api/v1/analysis/regional \
  -H "Content-Type: application/json" \
  -d '{"regions": ["강남구", "서초구"], "top_n": 5}'

# Jeonse ratio analysis
curl -X POST http://localhost:8000/api/v1/investment/jeonse-ratio \
  -H "Content-Type: application/json" \
  -d '{"region_filter": "강남구", "start_date": "2023-01-01", "end_date": "2023-12-31"}'

# Market signals detection
curl -X POST http://localhost:8000/api/v1/market/signals \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2023-01-01", "end_date": "2023-12-31", "region_filter": "강남구"}'

# Floor premium analysis
curl -X POST http://localhost:8000/api/v1/premium/floor-premium \
  -H "Content-Type: application/json" \
  -d '{"region_filter": "강남구", "start_date": "2023-01-01", "end_date": "2023-12-31"}'
```

## Implementation Status

All 23 analyzer endpoints have been fully implemented:

**Analysis (3/3)** ✓
- Basic statistics
- Price trends
- Regional analysis

**Segmentation (5/5)** ✓
- By area
- By floor
- By build year
- By apartment
- Apartment detail

**Premium (4/4)** ✓
- Price per area
- Price per area trend
- Floor premium
- Building age premium

**Investment (3/3)** ✓
- Jeonse ratio
- Gap investment
- Bargain sales

**Market (8/8)** ✓
- Rent vs jeonse
- Dealing type
- Buyer/seller type
- Cancelled deals
- Period summary
- Baseline summary
- Period comparison
- Market signals

For detailed documentation of each endpoint, see [API_ENDPOINTS.md](./API_ENDPOINTS.md)

## Production Considerations

Before deploying to production:

1. **CORS**: Update `middleware/cors.py` to restrict allowed origins
2. **Environment**: Set proper environment variables
3. **Workers**: Use multiple workers with gunicorn or uvicorn
4. **Reverse Proxy**: Setup nginx or similar
5. **SSL**: Configure HTTPS
6. **Rate Limiting**: Add rate limiting middleware
7. **Monitoring**: Setup monitoring and alerting
8. **Database**: Ensure PostgreSQL is properly configured with connection pooling
