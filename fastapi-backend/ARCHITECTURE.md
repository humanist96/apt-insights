# FastAPI Backend Architecture

## Overview

This FastAPI backend provides a RESTful API interface to the apartment transaction analysis platform. It wraps the existing `backend.analyzer` module and exposes 23 analysis functions through well-designed API endpoints.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (Frontend/API Consumer)            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ HTTP/REST
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   FastAPI Application                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  main.py - Application Entry Point                   │   │
│  │  - CORS Middleware                                    │   │
│  │  - Logging Middleware                                 │   │
│  │  - Exception Handlers                                 │   │
│  │  - OpenAPI/Swagger Documentation                      │   │
│  └───────────────────┬──────────────────────────────────┘   │
│                      │                                       │
│  ┌───────────────────▼──────────────────────────────────┐   │
│  │  routers/analysis.py - API Endpoints                  │   │
│  │  - POST /api/v1/analysis/basic-stats                  │   │
│  │  - POST /api/v1/analysis/price-trend                  │   │
│  │  - POST /api/v1/analysis/regional                     │   │
│  │  - POST /api/v1/analysis/cache/clear                  │   │
│  └───────────────────┬──────────────────────────────────┘   │
│                      │                                       │
│  ┌───────────────────▼──────────────────────────────────┐   │
│  │  schemas/ - Pydantic Models                           │   │
│  │  - requests.py: Request validation                    │   │
│  │  - responses.py: Response formatting                  │   │
│  └───────────────────┬──────────────────────────────────┘   │
│                      │                                       │
│  ┌───────────────────▼──────────────────────────────────┐   │
│  │  services/analyzer_service.py - Business Logic        │   │
│  │  - Data loading with caching                          │   │
│  │  - Filter application (region, date)                  │   │
│  │  - Wrapper methods for analyzer functions             │   │
│  └───────────────────┬──────────────────────────────────┘   │
└────────────────────┬─┴───────────────────────────────────────┘
                     │
                     │
┌────────────────────▼─────────────────────────────────────────┐
│              Backend Modules (Existing)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  backend/data_loader.py                               │   │
│  │  - load_all_json_data()                               │   │
│  │  - PostgreSQL or JSON mode (auto-detect)              │   │
│  └───────────────────┬──────────────────────────────────┘   │
│                      │                                       │
│  ┌───────────────────▼──────────────────────────────────┐   │
│  │  backend/analyzer.py - 23 Analysis Functions          │   │
│  │  - calculate_basic_stats()                            │   │
│  │  - calculate_price_trend()                            │   │
│  │  - analyze_by_region()                                │   │
│  │  - analyze_by_area()                                  │   │
│  │  - analyze_by_floor()                                 │   │
│  │  - ... and 18 more functions                          │   │
│  └───────────────────┬──────────────────────────────────┘   │
└────────────────────┬─┴───────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                    Data Sources                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  PostgreSQL (USE_DATABASE=true)                       │   │
│  │  - 63,809 apartment transactions                      │   │
│  │  - Normalized schema                                  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  JSON Files (USE_DATABASE=false)                      │   │
│  │  - api_01/output/*.json                               │   │
│  │  - api_02/output/*.json                               │   │
│  │  - api_03/output/*.json                               │   │
│  │  - api_04/output/*.json                               │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. FastAPI Application Layer (main.py)

**Responsibilities:**
- Application initialization and configuration
- Middleware setup (CORS, logging)
- Router registration
- Global exception handling
- OpenAPI documentation generation
- Health check endpoints

**Key Features:**
- Auto-generated Swagger UI at `/docs`
- ReDoc documentation at `/redoc`
- Structured logging with request/response metrics
- CORS enabled for frontend integration

### 2. Router Layer (routers/analysis.py)

**Responsibilities:**
- Define API endpoints and routes
- Request validation (via Pydantic)
- Response formatting
- HTTP status code handling
- Error handling and logging

**Design Patterns:**
- RESTful API design
- POST for analysis endpoints (supports request body)
- Consistent URL structure: `/api/v1/{resource}/{action}`
- Standard response format

### 3. Schema Layer (schemas/)

**Responsibilities:**
- Request validation models
- Response formatting models
- Data type definitions
- Field validation rules

**Key Components:**

**requests.py:**
- `BasicStatsRequest` - Region/date filters
- `PriceTrendRequest` - Trend analysis parameters
- `RegionalAnalysisRequest` - Regional comparison params
- Built-in validators for dates, enums

**responses.py:**
- `StandardResponse[T]` - Generic wrapper with success/error/meta
- `BasicStatsData` - Stats response structure
- `PriceTrendData` - Trend data with monthly breakdowns
- `RegionalAnalysisData` - Regional comparison data
- `MetaData` - Common metadata (counts, timing, source)

### 4. Service Layer (services/analyzer_service.py)

**Responsibilities:**
- Business logic implementation
- Data loading and caching
- Filter application (region, date range)
- Wrapper methods for backend analyzer functions
- Error handling and logging

**Key Features:**

**Data Caching:**
```python
class AnalyzerService:
    _data_cache: List[Dict]          # In-memory cache
    _cache_timestamp: datetime        # Cache creation time
    _cache_ttl_seconds: int = 300     # 5-minute TTL
```

**Filter Methods:**
- `_filter_by_date_range()` - ISO date filtering
- `_filter_by_region()` - Case-insensitive partial match
- Chainable filters for complex queries

**Public API:**
- `get_basic_stats()` → `analyzer.calculate_basic_stats()`
- `get_price_trend()` → `analyzer.calculate_price_trend()`
- `get_regional_analysis()` → `analyzer.analyze_by_region()`
- `clear_cache()` - Manual cache invalidation

### 5. Backend Integration Layer

**Data Loading:**
```python
# Auto-detects USE_DATABASE environment variable
items, debug_info = load_all_json_data(base_path=backend_path, debug=True)

# Returns:
# - items: List[Dict] - Transaction records
# - debug_info: Dict - Metadata about data source, counts, errors
```

**Analyzer Functions:**
- All 23 functions take `List[Dict]` as input
- Return structured dictionaries
- Pure functions (no side effects)
- Can be composed and chained

## Data Flow

### Example: GET /api/v1/analysis/basic-stats

```
1. Client Request
   POST /api/v1/analysis/basic-stats
   {
     "region_filter": "강남구",
     "start_date": "2023-01-01",
     "end_date": "2023-12-31"
   }
   ↓

2. Router (analysis.py)
   - Validate request via Pydantic
   - Start timing
   - Log request
   ↓

3. Service (analyzer_service.py)
   - Check cache (5-min TTL)
   - Load data if cache miss
   - Apply date filter: 2023-01-01 to 2023-12-31
   - Apply region filter: "강남구" (case-insensitive)
   ↓

4. Backend (analyzer.py)
   - calculate_basic_stats(filtered_items)
   - Compute: count, avg, min, max, median
   - Group by region
   - Return dict
   ↓

5. Service (analyzer_service.py)
   - Prepare metadata (counts, timing, source)
   - Return (stats, metadata)
   ↓

6. Router (analysis.py)
   - Convert to Pydantic models
   - Build StandardResponse
   - Calculate processing time
   - Log completion
   ↓

7. Client Response
   {
     "success": true,
     "data": {
       "total_count": 1234,
       "avg_price": 120000,
       "regions": {...}
     },
     "meta": {
       "total_records": 63809,
       "filtered_records": 1234,
       "data_source": "postgresql",
       "processing_time_ms": 45.23
     }
   }
```

## Design Patterns

### 1. Repository Pattern
- `AnalyzerService` acts as repository
- Abstracts data loading and caching
- Provides clean interface to routers

### 2. Service Layer Pattern
- Business logic separated from routing
- Testable without FastAPI dependencies
- Reusable across multiple endpoints

### 3. Standard Response Wrapper
```python
class StandardResponse[T]:
    success: bool
    data: Optional[T]
    error: Optional[str]
    meta: Optional[MetaData]
```

Benefits:
- Consistent response format
- Easy error handling on client
- Metadata for debugging and monitoring

### 4. Dependency Injection
- Services initialized as singletons
- Easy to mock for testing
- Can be replaced with DI framework later

### 5. Middleware Chain
```python
Request → CORS → Logging → Router → Response
```

Each middleware:
- Adds specific functionality
- Can be enabled/disabled independently
- Follows single responsibility principle

## Error Handling Strategy

### Request Validation (422)
```python
# Automatic via Pydantic
{
  "detail": [
    {
      "loc": ["body", "start_date"],
      "msg": "Date must be in YYYY-MM-DD format",
      "type": "value_error"
    }
  ]
}
```

### Application Errors (500)
```python
# Caught by router exception handler
{
  "success": false,
  "error": "Failed to calculate basic statistics",
  "detail": "Division by zero",
  "timestamp": "2026-02-07T12:00:00"
}
```

### Global Exception Handler
```python
# Catches any unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # Log error with context
    # Return standardized error response
```

## Logging Strategy

### Structured Logging with structlog

**Request Started:**
```json
{
  "event": "request_started",
  "method": "POST",
  "path": "/api/v1/analysis/basic-stats",
  "client_host": "127.0.0.1",
  "timestamp": "2026-02-07T12:00:00"
}
```

**Request Completed:**
```json
{
  "event": "request_completed",
  "method": "POST",
  "path": "/api/v1/analysis/basic-stats",
  "status_code": 200,
  "processing_time_ms": 45.23,
  "timestamp": "2026-02-07T12:00:00"
}
```

**Business Logic:**
```json
{
  "event": "data_loaded",
  "record_count": 63809,
  "data_source": "postgresql",
  "timestamp": "2026-02-07T12:00:00"
}
```

## Performance Optimizations

### 1. Data Caching
- 5-minute TTL cache in AnalyzerService
- Reduces database/file reads
- Shared across all requests
- Manual invalidation via `/cache/clear`

### 2. Processing Time Tracking
- Every response includes `processing_time_ms`
- Custom header: `X-Processing-Time-Ms`
- Helps identify bottlenecks

### 3. Async Request Handling
- FastAPI runs on ASGI (async)
- Non-blocking I/O
- Can handle concurrent requests efficiently

### 4. Lazy Loading
- Data loaded on first request
- Cached for subsequent requests
- No startup delay

## Security Considerations

### Current Implementation (Development)
- CORS: Allow all origins (`*`)
- No authentication/authorization
- No rate limiting
- No input sanitization beyond Pydantic validation

### Production Requirements
1. **CORS**: Restrict to known frontend domains
2. **Authentication**: Add JWT/OAuth2
3. **Rate Limiting**: Implement per-IP/per-user limits
4. **Input Sanitization**: Additional validation layers
5. **HTTPS**: TLS encryption
6. **API Keys**: For external integrations
7. **Logging**: PII masking
8. **Secrets**: Environment-based configuration

## Testing Strategy

### Unit Tests (TODO)
```python
# Test service layer
def test_analyzer_service_basic_stats():
    service = AnalyzerService()
    stats, meta = service.get_basic_stats()
    assert stats['total_count'] > 0
```

### Integration Tests (TODO)
```python
# Test full endpoint
from fastapi.testclient import TestClient

def test_basic_stats_endpoint():
    client = TestClient(app)
    response = client.post("/api/v1/analysis/basic-stats", json={})
    assert response.status_code == 200
```

### Current Testing
- `test_api.py` - Manual integration tests
- Requires running server
- Tests all endpoints with assertions

## Deployment Options

### 1. Development
```bash
python main.py
# or
uvicorn main:app --reload
```

### 2. Production (Single Server)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Production (Gunicorn + Uvicorn)
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 4. Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5. Kubernetes
- Horizontal Pod Autoscaler
- Load balancer
- Health checks via `/health`
- Rolling updates

## Monitoring and Observability

### Metrics to Track
- Request count by endpoint
- Response time percentiles (p50, p95, p99)
- Error rate by type
- Cache hit/miss ratio
- Data source (PostgreSQL vs JSON)
- Processing time by analysis type

### Logging Integration
- Send structured logs to ELK/Splunk
- Alert on error spikes
- Track slow queries (>1s processing time)

### Health Checks
- `/health` - Application health
- Database connectivity (if USE_DATABASE=true)
- Cache status
- Dependency health

## Future Enhancements

### 1. Additional Endpoints
Wrap remaining 20 analyzer functions:
- `/api/v1/analysis/area` - analyze_by_area()
- `/api/v1/analysis/floor` - analyze_by_floor()
- `/api/v1/analysis/building-age` - analyze_by_build_year()
- `/api/v1/analysis/price-per-area` - calculate_price_per_area()
- `/api/v1/analysis/apartment/{name}` - get_apartment_detail()
- etc.

### 2. WebSocket Support
- Real-time data updates
- Live price trend graphs
- Push notifications for bargain sales

### 3. Background Jobs
- Periodic data refresh from APIs
- Scheduled analysis reports
- Email notifications

### 4. GraphQL API
- Alternative to REST
- Client-defined queries
- Reduced over-fetching

### 5. Advanced Caching
- Redis for distributed cache
- Cache warming strategies
- Per-user cache isolation

### 6. API Versioning
- `/api/v2/...` for breaking changes
- Deprecation warnings
- Migration guides

## Contributing Guidelines

### Adding New Endpoints

1. **Create Request Schema** (schemas/requests.py)
```python
class NewAnalysisRequest(BaseModel):
    param1: str
    param2: Optional[int] = None
```

2. **Create Response Schema** (schemas/responses.py)
```python
class NewAnalysisData(BaseModel):
    result_field: str

class NewAnalysisResponse(StandardResponse[NewAnalysisData]):
    pass
```

3. **Add Service Method** (services/analyzer_service.py)
```python
def get_new_analysis(self, param1: str) -> Tuple[Dict, Dict]:
    items, debug_info = self._load_data()
    # Apply filters
    result = analyzer.new_analysis_function(items, param1)
    metadata = {...}
    return result, metadata
```

4. **Create Router Endpoint** (routers/analysis.py)
```python
@router.post("/new-analysis", response_model=NewAnalysisResponse)
async def new_analysis(request: NewAnalysisRequest):
    # Implementation
```

5. **Update Documentation**
- Add endpoint to README.md
- Update OpenAPI description
- Add example requests/responses

6. **Write Tests**
- Unit tests for service method
- Integration test for endpoint
- Add to test_api.py

## Conclusion

This FastAPI backend provides a robust, scalable, and well-documented API interface to the apartment transaction analysis platform. The layered architecture ensures:

- **Separation of Concerns**: Each layer has clear responsibilities
- **Testability**: Pure functions and dependency injection
- **Scalability**: Async handling and caching
- **Maintainability**: Clean code and comprehensive documentation
- **Extensibility**: Easy to add new endpoints and features

The current implementation covers the core functionality with 3 endpoints, providing a solid foundation for future expansion to all 23 analyzer functions.
