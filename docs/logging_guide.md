# Logging 시스템 가이드

## 📚 개요

structlog 기반의 구조화된 로깅 시스템

### 주요 기능

- 🎨 **컬러 출력** (개발 환경)
- 📊 **JSON 로그** (프로덕션)
- 🔒 **민감 데이터 마스킹** (API 키, 비밀번호 자동 제거)
- 📈 **성능 메트릭**
- 🐛 **상세 에러 추적**
- 📁 **파일 로깅** (로그 로테이션)

---

## 🚀 빠른 시작

### 1. 기본 사용법

```python
from logger import get_logger

logger = get_logger(__name__)

logger.info("사용자 로그인", user_id=123, success=True)
logger.warning("디스크 사용량 높음", usage_percent=95)
logger.error("데이터베이스 연결 실패", error_code="DB_TIMEOUT")
```

**출력**:
```
2026-02-07T01:26:42.168Z [INFO    ] 사용자 로그인
  app=apt-insights environment=development user_id=123 success=True
```

### 2. API 요청 로깅

```python
from logger import APILogger

api_logger = APILogger("api_01")

# 요청 로깅
api_logger.log_request(
    "GET",
    "https://apis.data.go.kr/api",
    params={"LAWD_CD": "11680", "DEAL_YMD": "202312"}
)

# 응답 로깅
api_logger.log_response(200, 0.5, item_count=10)

# 재시도 로깅
api_logger.log_retry(2, 3, "Timeout")

# 에러 로깅
api_logger.log_error("Connection failed", error_code="TIMEOUT")
```

### 3. 성능 측정

```python
from logger import PerformanceLogger

with PerformanceLogger("data_processing") as perf:
    # 처리 로직
    result = process_large_dataset()

    # 메트릭 추가
    perf.add_metric("records_processed", len(result))
    perf.add_metric("errors", 0)
```

**출력**:
```
2026-02-07T01:26:42.271Z [INFO    ] operation_complete
  operation=data_processing duration=0.102 records_processed=1000 errors=0
```

---

## 🔧 설정

### 환경변수

`.env` 파일에서 설정:

```bash
# 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# 환경 (development, staging, production)
ENVIRONMENT=development
```

### 로그 포맷

**Development** (컬러 출력):
```
2026-02-07T01:26:42.168Z [INFO    ] api_request
  api=api_01 method=GET url=https://... status=200
```

**Production** (JSON):
```json
{
  "timestamp": "2026-02-07T01:26:42.168Z",
  "level": "INFO",
  "event": "api_request",
  "api": "api_01",
  "method": "GET",
  "url": "https://...",
  "status": 200,
  "app": "apt-insights",
  "environment": "production",
  "version": "0.1.0"
}
```

### 프로그래밍 방식 설정

```python
from logger import configure_logging

# 개발 환경: 컬러 출력, DEBUG 레벨
configure_logging(
    log_level="DEBUG",
    json_logs=False
)

# 프로덕션: JSON, INFO 레벨
configure_logging(
    log_level="INFO",
    json_logs=True,
    log_file="/var/log/apt-insights/app.log"
)
```

---

## 🔒 보안: 민감 데이터 자동 마스킹

**Before**:
```python
logger.info("api_request", params={"serviceKey": "abc123..."})
```

**After** (자동 마스킹):
```
api_request params={'serviceKey': '***REDACTED***'}
```

**마스킹되는 키워드**:
- `serviceKey`, `service_key`
- `api_key`, `apiKey`
- `password`, `passwd`
- `token`, `access_token`
- `secret`, `api_secret`
- `authorization`, `auth`
- `cookie`

### 커스텀 마스킹 추가

`logger.py`의 `censor_sensitive_data()` 함수 수정:

```python
sensitive_keys = [
    "serviceKey", "api_key", "password", "token",
    "your_custom_key"  # 추가
]
```

---

## 📊 로그 레벨 가이드

| 레벨 | 용도 | 예시 |
|------|------|------|
| **DEBUG** | 개발 디버깅 | 변수 값, 함수 호출 |
| **INFO** | 일반 정보 | API 요청/응답, 작업 완료 |
| **WARNING** | 경고 (복구 가능) | 재시도, 디스크 사용량 높음 |
| **ERROR** | 에러 (복구 불가) | API 실패, DB 연결 실패 |
| **CRITICAL** | 시스템 장애 | 서버 다운, 데이터 손실 |

### 예시

```python
logger.debug("변수 값 확인", value=data)
logger.info("작업 완료", records=100)
logger.warning("재시도 중", attempt=2)
logger.error("API 실패", error_code="TIMEOUT")
logger.critical("서버 다운", reason="Out of memory")
```

---

## 📁 로그 파일

### 기본 설정

로그 파일은 `logs/` 디렉토리에 저장:

```
apt_test/
└── logs/
    └── apt_insights.log
```

### 로그 로테이션 (Phase 1)

```python
import logging.handlers

handler = logging.handlers.RotatingFileHandler(
    "logs/apt_insights.log",
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

**결과**:
```
logs/
├── apt_insights.log        (현재)
├── apt_insights.log.1      (백업)
├── apt_insights.log.2
└── apt_insights.log.3
```

---

## 🎯 실전 사용 예시

### 1. BaseAPIClient 통합

```python
class BaseAPIClient:
    def __init__(self):
        self.api_logger = APILogger("api_01")

    def _make_request(self, params):
        # 요청 로깅
        self.api_logger.log_request("GET", url, params)

        try:
            response = requests.get(url, params)
            # 응답 로깅
            self.api_logger.log_response(
                response.status_code,
                response_time=0.5
            )
        except Exception as e:
            # 에러 로깅
            self.api_logger.log_error(str(e), error_code="REQUEST_FAILED")
```

### 2. Streamlit 앱

```python
from logger import get_logger

logger = get_logger("streamlit")

@st.cache_data
def load_data(region, month):
    logger.info("data_load_start", region=region, month=month)

    try:
        data = fetch_api_data(region, month)
        logger.info("data_load_success", records=len(data))
        return data
    except Exception as e:
        logger.error("data_load_failed", error=str(e), exc_info=True)
        st.error(f"데이터 로드 실패: {e}")
```

### 3. 배치 작업

```python
from logger import PerformanceLogger, get_logger

logger = get_logger("batch")

with PerformanceLogger("monthly_collection") as perf:
    results = []

    for region in regions:
        logger.info("collecting_region", region=region)
        data = api.get_trade_data(region, month)
        results.append(data)

    perf.add_metric("total_regions", len(regions))
    perf.add_metric("total_records", sum(len(r) for r in results))
```

---

## 🐛 에러 추적

### 예외 정보 포함

```python
try:
    result = risky_operation()
except Exception as e:
    logger.error("operation_failed", exc_info=True)
```

**출력**:
```
2026-02-07T01:26:42.271Z [ERROR   ] operation_failed
  app=apt-insights environment=development
Traceback (most recent call last):
  File "app.py", line 42, in risky_operation
    result = 1 / 0
ZeroDivisionError: division by zero
```

### 에러 컨텍스트 추가

```python
try:
    process_user_data(user_id)
except Exception as e:
    logger.error(
        "user_processing_failed",
        user_id=user_id,
        stage="data_validation",
        error=str(e),
        exc_info=True
    )
```

---

## 📈 모니터링 통합 (Phase 3)

### Prometheus 메트릭

```python
from prometheus_client import Counter, Histogram

api_requests = Counter('api_requests_total', 'Total API requests')
response_time = Histogram('api_response_seconds', 'API response time')

# 로그와 함께 메트릭 증가
logger.info("api_request", url=url)
api_requests.inc()
```

### Sentry 통합

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://...",
    traces_sample_rate=1.0,
    environment=settings.ENVIRONMENT
)

# Sentry가 자동으로 ERROR 이상 로그 캡처
logger.error("critical_error", user_id=123)
```

---

## 🧪 테스트

### 로그 캡처 (pytest)

```python
import pytest
import structlog

def test_logging(caplog):
    logger = structlog.get_logger()

    with caplog.at_level("INFO"):
        logger.info("test_message", value=42)

    assert "test_message" in caplog.text
    assert "value=42" in caplog.text
```

### Mock 로거

```python
from unittest.mock import MagicMock
from logger import get_logger

def test_api_client(monkeypatch):
    mock_logger = MagicMock()
    monkeypatch.setattr("base_api_client.get_logger", lambda x: mock_logger)

    client = BaseAPIClient()
    client.get_trade_data("11680", "202312")

    # 로그 호출 검증
    mock_logger.info.assert_called()
```

---

## 🎓 베스트 프랙티스

### 1. 구조화된 로그

❌ **Bad**:
```python
logger.info(f"User {user_id} logged in at {timestamp}")
```

✅ **Good**:
```python
logger.info("user_login", user_id=user_id, timestamp=timestamp)
```

### 2. 일관된 이벤트 이름

```python
# 동사_명사 형식
logger.info("user_login")
logger.info("data_fetch_complete")
logger.error("api_call_failed")
```

### 3. 컨텍스트 추가

```python
logger.info(
    "api_request",
    method="GET",
    url=url,
    user_id=user_id,
    request_id=request_id
)
```

### 4. 민감 데이터 제외

```python
# 비밀번호, API 키는 자동 마스킹되지만
# 사용자 이름, 이메일도 주의
logger.info("user_created", user_id=123)  # ✅
logger.info("user_created", email="user@example.com")  # ⚠️
```

### 5. 성능 고려

```python
# 대용량 데이터는 길이만 로깅
logger.info("data_loaded", records=len(data))  # ✅
logger.info("data_loaded", data=data)  # ❌ (메모리 낭비)
```

---

## 📝 로그 분석

### jq를 사용한 JSON 로그 분석

```bash
# 에러만 필터링
cat logs/apt_insights.log | jq 'select(.level == "ERROR")'

# API 응답 시간 평균
cat logs/apt_insights.log | jq -r 'select(.event == "api_response") | .response_time' | awk '{sum+=$1; count++} END {print sum/count}'

# 가장 많이 호출된 API
cat logs/apt_insights.log | jq -r 'select(.event == "api_request") | .api' | sort | uniq -c | sort -rn
```

### Grafana Loki (Phase 3)

```promql
# 에러율
sum(rate({app="apt-insights"} |= "ERROR" [5m]))

# API 응답 시간 P95
histogram_quantile(0.95, sum(rate({app="apt-insights"} |= "api_response" [5m])) by (le))
```

---

## 🔄 마이그레이션 가이드

### 기존 코드 (Before)

```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Processing {count} items")
```

### 새 코드 (After)

```python
from logger import get_logger

logger = get_logger(__name__)
logger.info("processing_items", count=count)
```

### 일괄 변경 (sed)

```bash
# logging.getLogger → get_logger
find . -name "*.py" -exec sed -i '' 's/logging.getLogger/get_logger/g' {} \;
```

---

## 🚀 다음 단계 (Phase 1)

1. **로그 집계**
   - Elasticsearch + Kibana
   - Grafana Loki
   - CloudWatch Logs (AWS)

2. **알림**
   - ERROR 로그 발생 시 Slack 알림
   - 일일 로그 요약 이메일

3. **성능 모니터링**
   - Prometheus + Grafana
   - APM (Application Performance Monitoring)

4. **로그 보관**
   - S3 장기 보관 (1년)
   - 로그 압축 (gzip)

---

**최종 업데이트**: 2026-02-07
**버전**: 1.0
**담당**: Phase 0 팀
