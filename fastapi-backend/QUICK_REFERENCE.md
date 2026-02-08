# API Quick Reference Guide

## Endpoint Summary

Total: 23 endpoints across 5 categories

---

## Analysis (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/analysis/basic-stats` | Calculate basic statistics |
| POST | `/api/v1/analysis/price-trend` | Analyze price trends over time |
| POST | `/api/v1/analysis/regional` | Compare statistics by region |
| POST | `/api/v1/analysis/cache/clear` | Clear data cache |

---

## Segmentation (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/analysis/by-area` | Analyze by exclusive area |
| POST | `/api/v1/analysis/by-floor` | Analyze by floor level |
| POST | `/api/v1/analysis/by-build-year` | Analyze by construction year |
| POST | `/api/v1/analysis/by-apartment` | Analyze by apartment complex |
| POST | `/api/v1/analysis/apartment-detail` | Get specific apartment details |

---

## Premium (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/premium/price-per-area` | Calculate price per area |
| POST | `/api/v1/premium/price-per-area-trend` | Price per area trends |
| POST | `/api/v1/premium/floor-premium` | Floor premium analysis |
| POST | `/api/v1/premium/building-age-premium` | Building age premium |

---

## Investment (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/investment/jeonse-ratio` | Calculate jeonse ratio |
| POST | `/api/v1/investment/gap-investment` | Gap investment analysis |
| POST | `/api/v1/investment/bargain-sales` | Detect bargain sales |

---

## Market (8 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/market/rent-vs-jeonse` | Rent vs jeonse comparison |
| POST | `/api/v1/market/dealing-type` | Dealing type distribution |
| POST | `/api/v1/market/buyer-seller-type` | Buyer/seller type analysis |
| POST | `/api/v1/market/cancelled-deals` | Cancelled deals analysis |
| POST | `/api/v1/market/period-summary` | Period summary |
| POST | `/api/v1/market/baseline-summary` | Baseline (previous period) |
| POST | `/api/v1/market/compare-periods` | Period comparison |
| POST | `/api/v1/market/signals` | Market signals detection |

---

## Common Request Parameters

```json
{
  "region_filter": "강남구",           // Optional: Filter by region name
  "start_date": "2023-01-01",        // Optional: Start date (YYYY-MM-DD)
  "end_date": "2023-12-31"           // Optional: End date (YYYY-MM-DD)
}
```

## Response Format

All endpoints return:

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "total_records": 63809,
    "filtered_records": 1234,
    "data_source": "json",
    "timestamp": "2023-12-01T10:30:00",
    "processing_time_ms": 45.2
  }
}
```

## Quick Test Commands

```bash
# Start server
python main.py

# Test basic stats
curl -X POST http://localhost:8000/api/v1/analysis/basic-stats \
  -H "Content-Type: application/json" \
  -d '{"region_filter": "강남구"}'

# Test market signals
curl -X POST http://localhost:8000/api/v1/market/signals \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2023-01-01", "end_date": "2023-12-31"}'

# Run all tests
python test_new_endpoints.py
```

## Interactive Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Key Features

- All endpoints support **region filtering**
- All endpoints support **date range filtering**
- **5-minute cache** for performance
- **Automatic validation** with Pydantic
- **Structured logging** with request/response tracking
- **CORS enabled** for frontend integration

## Response Time Guidelines

- Simple queries: 20-50ms
- Complex aggregations: 50-200ms
- Full dataset analysis: 200-500ms
- Cached requests: <10ms

## Data Sources

- **JSON Mode**: Loads from `api_*/output/*.json` files
- **Database Mode**: Loads from PostgreSQL (when USE_DATABASE=true)

Total records: **63,809 transactions**

---

For complete documentation, see [API_ENDPOINTS.md](./API_ENDPOINTS.md)
