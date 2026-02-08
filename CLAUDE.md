ㅔ# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Korean apartment real estate transaction price API integration and analysis platform. Fetches data from the Korean Ministry of Land (국토교통부) public data APIs and provides a Streamlit-based visualization frontend.

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run individual API tests
python api_01/main.py [region_code] [year_month]  # e.g., python api_01/main.py 11680 202312

# Run batch tests with report generation
python api_01/test_runner.py
python api_02/test_runner.py
python api_03/test_runner.py
python api_04/test_runner.py

# Run region-specific tests (Suwon)
python api_01/test_suwon.py

# Launch Streamlit frontend
streamlit run frontend/app.py

# Performance Testing & Optimization
python scripts/performance_check.py           # Quick performance check
python scripts/benchmark.py                   # Full API benchmark
./scripts/optimize_all.sh                     # Run all optimizations
cd tests/load && locust -f locustfile.py      # Load testing with Locust
```

## Architecture

### Data Flow
```
API Request → XML Response → XML Parser (common.py) → JSON →
Test Output (api_*/output/*.json) → Data Loader (backend/) →
Analyzer → Streamlit Visualization
```

### Core Modules

- **`config.py`** - API service key storage
- **`common.py`** - XML/JSON parsing utilities (`parse_xml_response`, `parse_api_response`)
- **`api_XX/api_XX_*.py`** - API client classes (SilvTradeAPI, AptTradeAPI, etc.)
- **`api_XX/test_runner.py`** - Batch test execution with report generation
- **`backend/data_loader.py`** - Aggregates JSON from all `api_*/output/` directories
- **`backend/analyzer.py`** - Statistical analysis functions
- **`frontend/app.py`** - Streamlit web UI

### API Modules

| Directory | API | Class | Description |
|-----------|-----|-------|-------------|
| `api_01/` | RTMSDataSvcSilvTrade | `SilvTradeAPI` | 분양권전매 (Pre-sale Rights) |
| `api_02/` | RTMSDataSvcAptTrade | `AptTradeAPI` | 매매 (Apartment Trade) |
| `api_03/` | RTMSDataSvcAptTradeDev | `AptTradeDevAPI` | 매매 상세 (Detailed Trade) |
| `api_04/` | RTMSDataSvcAptRent | `AptRentAPI` | 전월세 (Rental) |

### Test Output Structure

Tests generate two files in `api_XX/output/`:
- `test_results_YYYYMMDD_HHMMSS.json` - Raw data for backend processing
- `test_report_YYYYMMDD_HHMMSS.md` - Human-readable report

### Key Patterns

**API Client Pattern:**
```python
from api_01.api_01_silv_trade import SilvTradeAPI

api = SilvTradeAPI()
result = api.get_trade_data_parsed('11680', '202312')  # lawd_cd, deal_ymd
```

**TestRunner Pattern:**
```python
runner = TestRunner()
runner.run_test_case(name='Test', lawd_cd='11680', deal_ymd='202312', description='...')
runner.generate_report()
```

**API Response Success Codes:** `'00'` or `'000'`

## Region Codes (lawd_cd)

- Seoul Jongno-gu: `11110`
- Seoul Gangnam-gu: `11680`
- Seoul Seocho-gu: `11650`
- Seoul Songpa-gu: `11710`

## Performance Testing & Optimization

### Quick Start
See `PERFORMANCE_QUICK_START.md` for 5-minute setup guide.

### Tools & Scripts

- **Load Testing**: `tests/load/locustfile.py` - Locust-based load testing with user simulation
- **Benchmarking**: `scripts/benchmark.py` - Comprehensive API endpoint benchmarking
- **Quick Check**: `scripts/performance_check.py` - Fast performance validation
- **Optimization**: `scripts/optimize_all.sh` - Run all optimization tasks
- **DB Optimizer**: `fastapi-backend/db/query_optimizer.py` - Database query analysis and optimization
- **Cache Warmer**: `fastapi-backend/cache/cache_warming.py` - Redis cache pre-population

### Performance Targets

| Metric | Target | Tool |
|--------|--------|------|
| p50 Response Time | < 50ms | benchmark.py |
| p95 Response Time | < 200ms | benchmark.py |
| p99 Response Time | < 500ms | benchmark.py |
| Throughput | 1000 req/min | Locust |
| Error Rate | < 0.1% | Locust |
| Cache Hit Rate | > 80% | cache_warming.py |

### Documentation

- **Comprehensive Guide**: `PERFORMANCE_OPTIMIZATION.md`
- **Quick Start**: `PERFORMANCE_QUICK_START.md`
- **Load Testing**: `tests/load/README.md`
- **Scripts**: `scripts/README.md`

## Important Notes

- Frontend loads only from real test output JSON files - no mock data
- API classes are duplicated in both `api_XX/` and `backend/api_modules/`
- Normalized fields in data_loader.py are prefixed with underscore (e.g., `_deal_amount_numeric`, `_region_name`)
- Performance tests run in CI/CD pipeline via `.github/workflows/performance.yml`