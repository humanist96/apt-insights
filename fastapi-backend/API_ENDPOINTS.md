# FastAPI Backend - Complete API Endpoint Documentation

## Overview

Complete apartment transaction analysis API with 23 endpoints across 5 categories:
- Analysis (3 endpoints) - Basic statistics and trends
- Segmentation (5 endpoints) - Analyze by area, floor, year, apartment
- Premium (4 endpoints) - Price per area and premium analysis
- Investment (3 endpoints) - Jeonse ratio, gap investment, bargain sales
- Market (8 endpoints) - Market signals, trends, and period comparisons

**Base URL**: `http://localhost:8000`

**Total Dataset**: 63,809 apartment transactions from Korean Ministry of Land APIs

---

## Table of Contents

1. [Analysis Endpoints](#analysis-endpoints)
2. [Segmentation Endpoints](#segmentation-endpoints)
3. [Premium Endpoints](#premium-endpoints)
4. [Investment Endpoints](#investment-endpoints)
5. [Market Endpoints](#market-endpoints)
6. [Common Parameters](#common-parameters)
7. [Response Format](#response-format)
8. [Error Handling](#error-handling)

---

## Analysis Endpoints

### 1. Calculate Basic Statistics
**POST** `/api/v1/analysis/basic-stats`

Calculate comprehensive statistics for apartment transactions.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "total_count": 1234,
    "avg_price": 85000,
    "max_price": 150000,
    "min_price": 30000,
    "median_price": 80000,
    "avg_area": 84.5,
    "regions": {
      "강남구": {
        "count": 500,
        "avg_price": 95000,
        "max_price": 150000,
        "min_price": 50000
      }
    }
  },
  "meta": {
    "total_records": 63809,
    "filtered_records": 1234,
    "data_source": "json",
    "processing_time_ms": 45.2
  }
}
```

### 2. Analyze Price Trends
**POST** `/api/v1/analysis/price-trend`

Analyze price trends over time with monthly aggregation.

**Request Body**:
```json
{
  "region_filter": "서초구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "group_by": "month"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "trend_data": [
      {
        "year_month": "2023-01",
        "count": 45,
        "avg_price": 78000,
        "max_price": 120000,
        "min_price": 35000,
        "median_price": 75000
      }
    ],
    "overall_trend": "increasing",
    "price_change_pct": 12.5
  }
}
```

### 3. Regional Analysis
**POST** `/api/v1/analysis/regional`

Compare statistics across different regions.

**Request Body**:
```json
{
  "regions": ["강남구", "서초구", "송파구"],
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "top_n": 10
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "regions": [
      {
        "region_name": "강남구",
        "count": 500,
        "avg_price": 95000,
        "max_price": 150000,
        "min_price": 50000,
        "median_price": 90000,
        "total_volume": 47500000
      }
    ],
    "top_region": "강남구",
    "total_regions": 3
  }
}
```

---

## Segmentation Endpoints

### 4. Analyze by Area
**POST** `/api/v1/analysis/by-area`

Segment transactions by exclusive area size.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "bins": [50, 60, 85, 100, 135]
}
```

**Response**: Statistics grouped by area bins.

### 5. Analyze by Floor
**POST** `/api/v1/analysis/by-floor`

Segment transactions by floor level.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**: Statistics for low (1-5), mid (6-15), high (16+) floors.

### 6. Analyze by Build Year
**POST** `/api/v1/analysis/by-build-year`

Segment transactions by building construction year.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**: Statistics grouped by construction year.

### 7. Analyze by Apartment
**POST** `/api/v1/analysis/by-apartment`

Analyze statistics for each apartment complex.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "min_count": 5
}
```

**Response**: Statistics for each apartment (with minimum transaction count).

### 8. Get Apartment Detail
**POST** `/api/v1/analysis/apartment-detail`

Get detailed information for a specific apartment complex.

**Request Body**:
```json
{
  "apt_name": "래미안",
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**: Comprehensive apartment statistics including transaction history.

---

## Premium Endpoints

### 9. Calculate Price Per Area
**POST** `/api/v1/premium/price-per-area`

Calculate price per area (평당가) statistics.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**: Price per square meter statistics.

### 10. Price Per Area Trend
**POST** `/api/v1/premium/price-per-area-trend`

Analyze price per area trends over time.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**: Monthly price per area trends.

### 11. Floor Premium Analysis
**POST** `/api/v1/premium/floor-premium`

Analyze price premium by floor level.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**: Floor premium percentages and price differences.

### 12. Building Age Premium
**POST** `/api/v1/premium/building-age-premium`

Analyze price premium by building age.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**: Premium by building age groups (new, mid-age, old).

---

## Investment Endpoints

### 13. Calculate Jeonse Ratio
**POST** `/api/v1/investment/jeonse-ratio`

Calculate jeonse ratio (전세가율 = Jeonse Price / Sale Price × 100).

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**:
- Average jeonse ratio by region
- High ratio apartments (>80% - strong rental demand)
- Low ratio apartments (<60% - weak rental market)

### 14. Gap Investment Analysis
**POST** `/api/v1/investment/gap-investment`

Analyze gap investment opportunities (Gap = Sale Price - Jeonse Price).

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "min_gap_ratio": 0.7
}
```

**Response**: Top gap investment candidates with leverage analysis.

### 15. Detect Bargain Sales
**POST** `/api/v1/investment/bargain-sales`

Detect transactions significantly below market average.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "threshold_pct": 10.0
}
```

**Response**: Potential bargain sales with discount percentages.

---

## Market Endpoints

### 16. Rent vs Jeonse Analysis
**POST** `/api/v1/market/rent-vs-jeonse`

Compare monthly rent vs jeonse transaction patterns.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**: Transaction count and prices by rental type.

### 17. Dealing Type Analysis
**POST** `/api/v1/market/dealing-type`

Analyze transaction dealing type distribution.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**: Direct vs agent transaction distribution.

### 18. Buyer/Seller Type Analysis
**POST** `/api/v1/market/buyer-seller-type`

Analyze buyer and seller type distribution.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**: Individual vs corporate transaction patterns.

### 19. Cancelled Deals Analysis
**POST** `/api/v1/market/cancelled-deals`

Analyze cancelled transaction patterns.

**Request Body**:
```json
{
  "region_filter": "강남구",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**: Cancellation rates and patterns.

### 20. Period Summary
**POST** `/api/v1/market/period-summary`

Generate comprehensive summary for a specific period.

**Request Body**:
```json
{
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "region_filter": "강남구"
}
```

**Response**: Complete period statistics and trends.

### 21. Baseline Summary
**POST** `/api/v1/market/baseline-summary`

Build baseline summary from previous period (for comparison).

**Request Body**:
```json
{
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "region_filter": "강남구"
}
```

**Response**: Previous period statistics (same duration before start_date).

### 22. Compare Periods
**POST** `/api/v1/market/compare-periods`

Compare two time periods.

**Request Body**:
```json
{
  "current_start_date": "2023-07-01",
  "current_end_date": "2023-12-31",
  "previous_start_date": "2023-01-01",
  "previous_end_date": "2023-06-30",
  "region_filter": "강남구",
  "current_label": "H2 2023",
  "previous_label": "H1 2023"
}
```

**Response**: Period-over-period comparison with change percentages.

### 23. Detect Market Signals
**POST** `/api/v1/market/signals`

Detect market signals and anomalies.

**Request Body**:
```json
{
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "region_filter": "강남구"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "signals": [
      {
        "type": "price_surge",
        "severity": "high",
        "message": "Strong price increase detected",
        "change_pct": 12.5
      }
    ],
    "current_period": { ... },
    "baseline_period": { ... },
    "comparison": { ... }
  }
}
```

**Signal Types**:
- `price_surge` - Price increase >10%
- `price_decline` - Price decrease <-5%
- `transaction_surge` - Volume increase >50%
- `market_freeze` - Volume decrease <-30%
- `high_jeonse_ratio` - Jeonse ratio >85%

---

## Common Parameters

### Date Range Filters
All endpoints support optional date filtering:
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format

### Region Filter
Filter by region name (partial match):
- `region_filter`: Region name (e.g., "강남구", "서초구 반포동")

### Pagination
- `top_n`: Limit results (for regional/apartment analysis)
- `min_count`: Minimum transaction count threshold

---

## Response Format

All endpoints return a standard response structure:

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "meta": {
    "total_records": 63809,
    "filtered_records": 1234,
    "data_source": "json",
    "timestamp": "2023-12-01T10:30:00",
    "processing_time_ms": 45.2
  }
}
```

**Fields**:
- `success`: Boolean indicating success/failure
- `data`: Response data (varies by endpoint)
- `error`: Error message (if success is false)
- `meta`: Metadata about the response
  - `total_records`: Total records in database
  - `filtered_records`: Records after filtering
  - `data_source`: "json" or "postgresql"
  - `timestamp`: Response timestamp (ISO format)
  - `processing_time_ms`: Processing time in milliseconds

---

## Error Handling

### Error Response Format
```json
{
  "success": false,
  "data": null,
  "error": "Error message here",
  "detail": "Detailed error information"
}
```

### HTTP Status Codes
- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

### Common Errors
- Invalid date format (use YYYY-MM-DD)
- Date range too large
- No data found for filters
- Missing required parameters

---

## Usage Examples

### Python
```python
import requests

url = "http://localhost:8000/api/v1/analysis/basic-stats"
payload = {
    "region_filter": "강남구",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
}

response = requests.post(url, json=payload)
data = response.json()

print(f"Total transactions: {data['data']['total_count']}")
print(f"Average price: {data['data']['avg_price']}")
```

### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/investment/jeonse-ratio" \
  -H "Content-Type: application/json" \
  -d '{
    "region_filter": "강남구",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  }'
```

### JavaScript/Fetch
```javascript
const response = await fetch('http://localhost:8000/api/v1/premium/floor-premium', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    region_filter: '강남구',
    start_date: '2023-01-01',
    end_date: '2023-12-31'
  })
});

const data = await response.json();
console.log(data);
```

---

## Interactive Documentation

Visit the following URLs for interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Cache Management

### Clear Cache
**POST** `/api/v1/analysis/cache/clear`

Clear the in-memory data cache to force reload.

**Response**:
```json
{
  "success": true,
  "message": "Cache cleared successfully",
  "timestamp": "2023-12-01T10:30:00"
}
```

**Note**: Cache TTL is 5 minutes by default.

---

## Performance Tips

1. **Use date filters** - Reduces data processing time
2. **Use region filters** - Narrows down dataset
3. **Cache is automatic** - Subsequent requests within 5 minutes use cache
4. **Limit top_n** - For large result sets, use pagination
5. **Parallel requests** - Endpoints can be called in parallel

---

## Support

For issues or questions:
- Check logs in `logs/` directory
- Review error messages in response
- Check interactive docs at `/docs`
- Verify date format (YYYY-MM-DD)
- Ensure region names match database values

---

**Last Updated**: 2026-02-07
**API Version**: 1.0.0
**Total Endpoints**: 23 (3 analysis + 5 segmentation + 4 premium + 3 investment + 8 market)
