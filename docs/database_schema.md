# 데이터베이스 스키마 문서

## 개요

아파트 실거래가 데이터를 저장하는 PostgreSQL 16 데이터베이스 스키마입니다.
4개 API (분양권, 매매, 매매상세, 전월세)의 데이터를 하나의 테이블에 통합 저장합니다.

## 테이블 구조

### `transactions` 테이블

#### 필드 목록

**Primary Key:**
- `id` (SERIAL): 자동 증가 ID

**API 메타 정보:**
- `transaction_type` (VARCHAR(10)): API 타입 (api_01, api_02, api_03, api_04)
- `source_file` (VARCHAR(500)): 소스 JSON 파일 경로
- `created_at` (TIMESTAMP): 생성 시각

**아파트 정보:**
- `apt_seq` (VARCHAR(50)): 아파트 일련번호
- `apt_nm` (VARCHAR(100)): 아파트 이름
- `excl_use_ar` (VARCHAR(20)): 전용면적
- `build_year` (VARCHAR(4)): 건축년도

**위치 정보:**
- `umd_nm` (VARCHAR(100)): 읍면동명
- `jibun` (VARCHAR(50)): 지번
- `sgg_cd` (VARCHAR(5)): 시군구 코드
- `floor` (VARCHAR(10)): 층

**거래 정보:**
- `deal_amount` (VARCHAR(50)): 거래금액 (문자열)
- `deal_year` (VARCHAR(4)): 거래년도
- `deal_month` (VARCHAR(2)): 거래월
- `deal_day` (VARCHAR(2)): 거래일

**정규화된 필드 (9개, _ prefix):**
- `_deal_amount_numeric` (DECIMAL(15,2)): 거래금액 (숫자)
- `_area_numeric` (DECIMAL(10,2)): 면적 (숫자)
- `_deal_date` (DATE): 거래일자
- `_year_month` (VARCHAR(6)): 년월 (YYYYMM)
- `_build_year_int` (INTEGER): 건축년도 (정수)
- `_floor_int` (INTEGER): 층 (정수)
- `_deposit_numeric` (DECIMAL(15,2)): 보증금 (숫자)
- `_monthly_rent_numeric` (DECIMAL(15,2)): 월세 (숫자)
- `_region_name` (VARCHAR(100)): 지역명

#### 제약 조건

**Unique Constraint:**
```sql
UNIQUE (transaction_type, apt_seq, deal_year, deal_month, deal_day, deal_amount)
```

#### 인덱스

성능 최적화를 위한 7개 인덱스:

1. `idx_deal_date` - 거래일자
2. `idx_region` - 지역코드
3. `idx_transaction_type` - API 타입
4. `idx_apt_nm` - 아파트 이름
5. `idx_year_month` - 년월
6. `idx_apt_seq` - 아파트 일련번호
7. `idx_composite_region_date` - 복합 인덱스 (지역 + 날짜)

## 쿼리 예시

### 1. 최근 1년 거래 조회
```sql
SELECT * FROM transactions
WHERE _deal_date >= CURRENT_DATE - INTERVAL '1 year'
ORDER BY _deal_date DESC
LIMIT 100;
```

### 2. 특정 지역 매매 조회
```sql
SELECT * FROM transactions
WHERE sgg_cd = '11680'  -- 강남구
  AND transaction_type = 'api_02'  -- 매매
ORDER BY _deal_date DESC;
```

### 3. 아파트별 평균 거래가
```sql
SELECT
    apt_nm,
    COUNT(*) as trade_count,
    AVG(_deal_amount_numeric) as avg_price,
    MIN(_deal_date) as first_trade,
    MAX(_deal_date) as last_trade
FROM transactions
WHERE transaction_type = 'api_02'
GROUP BY apt_nm
HAVING COUNT(*) >= 10
ORDER BY avg_price DESC;
```

### 4. 월별 거래량 추이
```sql
SELECT
    _year_month,
    COUNT(*) as trade_count,
    AVG(_deal_amount_numeric) as avg_price
FROM transactions
WHERE transaction_type = 'api_02'
  AND _deal_date >= '2023-01-01'
GROUP BY _year_month
ORDER BY _year_month;
```

## 성능 목표

- 전체 데이터 로드 (98K 레코드): **< 2초**
- 지역별 필터링: **< 500ms**
- 날짜별 필터링: **< 300ms**

## 마이그레이션

### 초기 마이그레이션

```bash
# 1. Docker로 PostgreSQL 시작
docker-compose up -d postgres

# 2. 테이블 생성
python -c "from backend.db.session import init_db; init_db()"

# 3. JSON 데이터 마이그레이션
python backend/db/migrate_json_to_postgres.py

# 4. 검증
python backend/db/migrate_json_to_postgres.py --dry-run
```

### Dry-Run 모드

```bash
# 실제 삽입 없이 검증만 수행
python backend/db/migrate_json_to_postgres.py --dry-run
```

## 롤백 절차

PostgreSQL로 전환 후 문제 발생 시:

```bash
# .env 파일 수정
USE_DATABASE=false

# Streamlit 재시작
streamlit run frontend/app.py
```

즉시 JSON 모드로 복귀됩니다.

## 유지보수

### 통계 정보 업데이트
```sql
ANALYZE transactions;
```

### 인덱스 재구성
```sql
REINDEX TABLE transactions;
```

### 디스크 공간 확인
```sql
SELECT pg_size_pretty(pg_total_relation_size('transactions'));
```

## 참고 자료

- PostgreSQL 16 문서: https://www.postgresql.org/docs/16/
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/
