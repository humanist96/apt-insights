# FastAPI Backend - File Structure

```
fastapi-backend/
│
├── 📄 main.py                          # FastAPI application entry point
│   ├── FastAPI app initialization
│   ├── CORS middleware setup
│   ├── Logging middleware setup
│   ├── Router registration
│   ├── Health check endpoint
│   ├── Root endpoint
│   └── Global exception handler
│
├── 📁 routers/                         # API endpoint routers
│   ├── __init__.py                     # Router exports
│   └── analysis.py                     # Analysis endpoints
│       ├── POST /api/v1/analysis/basic-stats
│       ├── POST /api/v1/analysis/price-trend
│       ├── POST /api/v1/analysis/regional
│       └── POST /api/v1/analysis/cache/clear
│
├── 📁 schemas/                         # Pydantic models
│   ├── __init__.py                     # Schema exports
│   ├── requests.py                     # Request validation models
│   │   ├── BasicStatsRequest
│   │   ├── PriceTrendRequest
│   │   └── RegionalAnalysisRequest
│   └── responses.py                    # Response formatting models
│       ├── StandardResponse[T]
│       ├── MetaData
│       ├── BasicStatsResponse
│       ├── PriceTrendResponse
│       └── RegionalAnalysisResponse
│
├── 📁 services/                        # Business logic layer
│   ├── __init__.py                     # Service exports
│   └── analyzer_service.py             # Analyzer service
│       ├── AnalyzerService class
│       ├── Data loading with cache
│       ├── Filter methods
│       └── Wrapper methods for backend
│
├── 📁 middleware/                      # Custom middleware
│   ├── __init__.py                     # Middleware exports
│   ├── cors.py                         # CORS configuration
│   └── logging.py                      # Request logging
│       └── LoggingMiddleware class
│
├── 📄 test_api.py                      # Integration test suite
│   ├── test_health_check()
│   ├── test_root()
│   ├── test_basic_stats_all()
│   ├── test_basic_stats_filtered()
│   ├── test_price_trend()
│   ├── test_regional_analysis()
│   ├── test_validation_error()
│   └── test_cache_clear()
│
├── 📄 requirements.txt                 # Python dependencies
│   ├── fastapi==0.115.0
│   ├── uvicorn[standard]==0.32.0
│   ├── pydantic==2.9.2
│   ├── structlog==24.4.0
│   ├── psycopg2-binary==2.9.10
│   └── ... (12 total packages)
│
├── 📄 start.sh                         # Startup script
│   ├── Virtual environment setup
│   ├── Dependency installation
│   └── Server startup
│
├── 📄 .env.example                     # Environment template
├── 📄 .gitignore                       # Git ignore patterns
│
├── 📖 README.md                        # Complete API documentation
│   ├── Installation instructions
│   ├── Endpoint documentation
│   ├── Request/response examples
│   ├── Testing instructions
│   └── Integration guides
│
├── 📖 QUICKSTART.md                    # 5-minute setup guide
│   ├── Quick installation
│   ├── First API calls
│   ├── Common use cases
│   └── Troubleshooting
│
├── 📖 ARCHITECTURE.md                  # System design documentation
│   ├── Architecture diagrams
│   ├── Layer responsibilities
│   ├── Data flow examples
│   ├── Design patterns
│   └── Future enhancements
│
├── 📖 PROJECT_SUMMARY.md               # Project overview
│   ├── What was built
│   ├── Implementation details
│   ├── Success metrics
│   └── Recommendations
│
└── 📖 STRUCTURE.md                     # This file
```

## File Counts

```
Total Files: 19
├── Python files (.py): 10
├── Documentation (.md): 5
├── Configuration: 3 (.txt, .sh, .env.example)
└── Git: 1 (.gitignore)
```

## Lines of Code

```
Estimated Distribution:
├── Python code: ~1,200 lines
│   ├── main.py: ~150 lines
│   ├── routers/analysis.py: ~350 lines
│   ├── schemas/: ~250 lines
│   ├── services/analyzer_service.py: ~250 lines
│   ├── middleware/: ~100 lines
│   └── test_api.py: ~100 lines
│
├── Documentation: ~2,500 lines
│   ├── README.md: ~500 lines
│   ├── ARCHITECTURE.md: ~900 lines
│   ├── QUICKSTART.md: ~400 lines
│   ├── PROJECT_SUMMARY.md: ~600 lines
│   └── STRUCTURE.md: ~100 lines
│
└── Configuration: ~100 lines
    ├── requirements.txt: ~20 lines
    ├── start.sh: ~30 lines
    └── .gitignore: ~50 lines
```

## Import Relationships

```
main.py
  ↓
  ├─→ middleware.cors.setup_cors()
  ├─→ middleware.logging.setup_logging()
  └─→ routers.analysis.router
        ↓
        ├─→ schemas.requests (validation)
        ├─→ schemas.responses (formatting)
        └─→ services.analyzer_service.AnalyzerService
              ↓
              ├─→ backend.data_loader.load_all_json_data()
              └─→ backend.analyzer.* (23 functions)
                    ↓
                    └─→ PostgreSQL or JSON files
```

## Request Flow (Visual)

```
HTTP Request
    ↓
┌───────────────────────────────┐
│  CORS Middleware              │ → Allow origins
└───────────┬───────────────────┘
            ↓
┌───────────────────────────────┐
│  Logging Middleware           │ → Log request start
└───────────┬───────────────────┘
            ↓
┌───────────────────────────────┐
│  Router (analysis.py)         │ → Route to endpoint
└───────────┬───────────────────┘
            ↓
┌───────────────────────────────┐
│  Pydantic Validation          │ → Validate request
│  (schemas/requests.py)        │
└───────────┬───────────────────┘
            ↓
┌───────────────────────────────┐
│  Service Layer                │ → Business logic
│  (analyzer_service.py)        │
│    ├─ Load data (with cache)  │
│    ├─ Apply filters           │
│    └─ Call analyzer function  │
└───────────┬───────────────────┘
            ↓
┌───────────────────────────────┐
│  Backend Analyzer             │ → Analysis logic
│  (backend/analyzer.py)        │
└───────────┬───────────────────┘
            ↓
┌───────────────────────────────┐
│  Format Response              │ → Pydantic model
│  (schemas/responses.py)       │
└───────────┬───────────────────┘
            ↓
┌───────────────────────────────┐
│  Logging Middleware           │ → Log response
└───────────┬───────────────────┘
            ↓
HTTP Response (JSON)
```

## Key Entry Points

### 1. Starting the Server
```bash
# Entry: start.sh
./start.sh
  ↓
# Activates: main.py
uvicorn main:app --reload
  ↓
# Loads: FastAPI app
app = FastAPI(...)
  ↓
# Registers: routers/analysis.py
app.include_router(analysis_router)
```

### 2. Making API Call
```bash
# Entry: HTTP POST
curl -X POST /api/v1/analysis/basic-stats
  ↓
# Handled by: routers/analysis.py
@router.post("/basic-stats")
  ↓
# Validated: schemas/requests.py
BasicStatsRequest.parse_obj(...)
  ↓
# Processed: services/analyzer_service.py
analyzer_service.get_basic_stats(...)
  ↓
# Analyzed: backend/analyzer.py
analyzer.calculate_basic_stats(...)
  ↓
# Formatted: schemas/responses.py
BasicStatsResponse(success=True, data=...)
```

### 3. Running Tests
```bash
# Entry: test_api.py
python test_api.py
  ↓
# Executes: 8 test functions
test_health_check()
test_basic_stats_all()
...
  ↓
# Makes requests to: localhost:8000
requests.post("/api/v1/analysis/...")
  ↓
# Validates: Response structure
assert response.json()["success"] is True
```

## Documentation Hierarchy

```
Quick Start Flow:
1. QUICKSTART.md       → Get started in 5 minutes
2. README.md           → Learn API endpoints
3. ARCHITECTURE.md     → Understand system design
4. PROJECT_SUMMARY.md  → See complete overview
5. STRUCTURE.md        → Navigate file structure
```

## Dependencies Graph

```
Application Dependencies:
├── FastAPI (web framework)
│   ├── Pydantic (validation)
│   ├── Starlette (ASGI)
│   └── Uvicorn (server)
├── Structlog (logging)
├── psycopg2-binary (PostgreSQL)
├── SQLAlchemy (ORM)
├── python-dotenv (env vars)
└── httpx (HTTP client)

Backend Integration:
└── ../backend/
    ├── data_loader.py
    ├── analyzer.py
    └── db/ (optional, if USE_DATABASE=true)
```

## Testing Pyramid

```
Integration Tests (test_api.py)
├── 8 endpoint tests
├── Request validation test
├── Error handling test
└── Cache management test
    ↓
Unit Tests (TODO)
├── Service layer tests
├── Schema validation tests
└── Utility function tests
    ↓
End-to-End Tests (TODO)
├── Full user workflows
└── Performance tests
```

## Deployment Structure

```
Development:
fastapi-backend/
├── venv/ (local virtual env)
├── .env (local config)
└── Run: python main.py

Production:
docker-container/
├── app/ (copied from fastapi-backend/)
├── Dockerfile
└── Run: uvicorn with multiple workers
    ↓
    Load Balancer
    ├── Pod 1 (FastAPI)
    ├── Pod 2 (FastAPI)
    └── Pod 3 (FastAPI)
          ↓
    PostgreSQL Cluster
```

## Quick Navigation

| Need | Go To |
|------|-------|
| Get started quickly | QUICKSTART.md |
| Learn API endpoints | README.md |
| Understand architecture | ARCHITECTURE.md |
| See project overview | PROJECT_SUMMARY.md |
| Navigate files | STRUCTURE.md (this file) |
| Run server | start.sh |
| Test API | test_api.py |
| Configure | .env.example |

## File Purposes at a Glance

| File | Purpose | Critical? |
|------|---------|-----------|
| main.py | App entry point | ✅ |
| routers/analysis.py | API endpoints | ✅ |
| schemas/requests.py | Request validation | ✅ |
| schemas/responses.py | Response formatting | ✅ |
| services/analyzer_service.py | Business logic | ✅ |
| middleware/cors.py | CORS setup | ✅ |
| middleware/logging.py | Request logging | ⚠️ |
| test_api.py | Integration tests | ⚠️ |
| requirements.txt | Dependencies | ✅ |
| start.sh | Startup script | ⚠️ |
| README.md | API docs | 📖 |
| QUICKSTART.md | Quick setup | 📖 |
| ARCHITECTURE.md | System design | 📖 |
| PROJECT_SUMMARY.md | Overview | 📖 |
| .env.example | Config template | ⚠️ |
| .gitignore | Git config | ⚠️ |

Legend:
- ✅ Critical (required for operation)
- ⚠️ Important (recommended)
- 📖 Documentation (helpful)

---

**Last Updated:** 2026-02-07
