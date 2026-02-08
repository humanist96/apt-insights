-- 아파트 실거래가 데이터베이스 스키마
-- PostgreSQL 16+

-- 거래 데이터 테이블 (통합: API 01, 02, 03, 04)
CREATE TABLE IF NOT EXISTS transactions (
    -- Primary Key
    id SERIAL PRIMARY KEY,

    -- API 메타 정보
    transaction_type VARCHAR(10) NOT NULL,  -- 'api_01', 'api_02', 'api_03', 'api_04'
    source_file VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),

    -- 공통 필드 (48 fields from original JSON)
    -- 아파트 정보
    apt_seq VARCHAR(50),
    apt_nm VARCHAR(100),
    excl_use_ar VARCHAR(20),
    build_year VARCHAR(4),

    -- 위치 정보
    umd_nm VARCHAR(100),
    jibun VARCHAR(50),
    sgg_cd VARCHAR(5),
    floor VARCHAR(10),

    -- 거래 정보
    deal_amount VARCHAR(50),
    deal_year VARCHAR(4),
    deal_month VARCHAR(2),
    deal_day VARCHAR(2),
    req_gbn VARCHAR(10),

    -- 전월세 정보 (API 04)
    deposit VARCHAR(50),
    monthly_rent VARCHAR(50),
    previous_contract_deposit VARCHAR(50),
    previous_contract_monthly_rent VARCHAR(50),
    contract_term VARCHAR(50),
    contract_type VARCHAR(20),
    contract_gbn VARCHAR(10),

    -- 상세 정보 (API 03)
    buyer_gbn VARCHAR(20),
    seller_gbn VARCHAR(20),
    registration_gbn VARCHAR(20),
    deal_gbn VARCHAR(20),
    cancel_deal_day VARCHAR(10),
    cancel_deal_type VARCHAR(20),
    dealer_lawdnm VARCHAR(100),
    dealer_sigungu VARCHAR(100),

    -- 정규화된 필드 (9 normalized fields with _ prefix)
    _deal_amount_numeric DECIMAL(15, 2),
    _area_numeric DECIMAL(10, 2),
    _deal_date DATE,
    _year_month VARCHAR(6),
    _build_year_int INTEGER,
    _floor_int INTEGER,
    _deposit_numeric DECIMAL(15, 2),
    _monthly_rent_numeric DECIMAL(15, 2),
    _region_name VARCHAR(100),

    -- Unique constraint (중복 방지)
    CONSTRAINT unique_transaction UNIQUE (transaction_type, apt_seq, deal_year, deal_month, deal_day, deal_amount)
);

-- 인덱스 생성 (성능 최적화)
CREATE INDEX IF NOT EXISTS idx_deal_date ON transactions(_deal_date);
CREATE INDEX IF NOT EXISTS idx_region ON transactions(sgg_cd);
CREATE INDEX IF NOT EXISTS idx_transaction_type ON transactions(transaction_type);
CREATE INDEX IF NOT EXISTS idx_apt_nm ON transactions(apt_nm);
CREATE INDEX IF NOT EXISTS idx_year_month ON transactions(_year_month);
CREATE INDEX IF NOT EXISTS idx_apt_seq ON transactions(apt_seq);
CREATE INDEX IF NOT EXISTS idx_composite_region_date ON transactions(sgg_cd, _deal_date);

-- 통계 정보 업데이트
ANALYZE transactions;

-- 뷰: 최근 거래 데이터 (자주 사용되는 쿼리 최적화)
CREATE OR REPLACE VIEW recent_transactions AS
SELECT
    *,
    _deal_amount_numeric / NULLIF(_area_numeric, 0) as price_per_sqm
FROM transactions
WHERE _deal_date >= CURRENT_DATE - INTERVAL '1 year'
ORDER BY _deal_date DESC;

-- 함수: 거래 데이터 통계
CREATE OR REPLACE FUNCTION get_transaction_stats()
RETURNS TABLE (
    transaction_type VARCHAR,
    total_count BIGINT,
    avg_price DECIMAL,
    min_date DATE,
    max_date DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.transaction_type,
        COUNT(*) as total_count,
        AVG(t._deal_amount_numeric) as avg_price,
        MIN(t._deal_date) as min_date,
        MAX(t._deal_date) as max_date
    FROM transactions t
    GROUP BY t.transaction_type
    ORDER BY t.transaction_type;
END;
$$ LANGUAGE plpgsql;

-- 코멘트 추가
COMMENT ON TABLE transactions IS '아파트 실거래가 통합 데이터 (API 01~04)';
COMMENT ON COLUMN transactions.transaction_type IS 'API 타입: api_01(분양권), api_02(매매), api_03(매매상세), api_04(전월세)';
COMMENT ON COLUMN transactions._deal_amount_numeric IS '정규화된 거래금액 (숫자)';
COMMENT ON COLUMN transactions._area_numeric IS '정규화된 면적 (숫자)';
COMMENT ON COLUMN transactions._deal_date IS '정규화된 거래일자 (DATE)';
