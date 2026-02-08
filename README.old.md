# 아파트 실거래가 API 통합 테스트

국토교통부 공공데이터 API를 활용한 아파트 실거래가 조회 프로젝트입니다.

## 프로젝트 구조

```
apt_test/
├── config.py              # 인증키 설정
├── common.py              # 공통 유틸리티 모듈
├── batch_collector.py     # 배치 데이터 수집 모듈
├── collect_data.py        # 배치 데이터 수집 CLI 스크립트
├── requirements.txt       # 의존성 관리
├── README.md              # 프로젝트 문서
├── API_Ref.md             # API 참조 문서
│
├── api_01/                # API 01: 분양권전매 실거래가
│   ├── __init__.py
│   ├── api_01_silv_trade.py
│   ├── main.py            # CLI 실행 스크립트
│   ├── API_01_분양권전매_실거래가.md
│   └── test_results_01.md
│
├── api_02/                # API 02: 매매 실거래가
│   ├── __init__.py
│   └── API_02_매매_실거래가.md
│
├── api_03/                # API 03: 매매 실거래가 상세
│   ├── __init__.py
│   └── API_03_매매_실거래가_상세.md
│
└── api_04/                # API 04: 전월세 실거래가
    ├── __init__.py
    └── API_04_전월세_실거래가.md
```

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

### 배치 데이터 수집 (권장)

법정동코드와 기간 범위를 지정하여 모든 API에서 데이터를 일괄 수집할 수 있습니다.

```bash
# 기본 사용법: 모든 API에서 데이터 수집
python collect_data.py [법정동코드] [시작년월] [종료년월]

# 예시: 강남구 2023년 전체 데이터 수집
python collect_data.py 11680 202301 202312

# 특정 API만 선택하여 수집
python collect_data.py 11680 202301 202312 --api api_01 api_02

# 사용자 지정 출력 디렉토리
python collect_data.py 11680 202301 202312 --output-dir ./custom_output

# API 호출 딜레이 및 재시도 설정
python collect_data.py 11680 202301 202312 --delay 1.0 --max-retries 5
```

**옵션 설명:**
- `--api`: 수집할 API 타입 선택 (`api_01`, `api_02`, `api_03`, `api_04`). 선택하지 않으면 모든 API 수집
- `--output-dir`: 출력 디렉토리 경로. 선택하지 않으면 각 API의 기본 `output` 디렉토리 사용
- `--delay`: API 호출 간 딜레이 시간(초). 기본값: 0.5
- `--max-retries`: API 호출 실패 시 최대 재시도 횟수. 기본값: 3

**Python 모듈로 사용:**
```python
from batch_collector import BatchCollector

collector = BatchCollector(delay_seconds=0.5)

# 데이터 수집
result = collector.collect_data(
    lawd_cd='11680',
    start_ym='202301',
    end_ym='202312',
    api_types=['api_01', 'api_02']  # None이면 모든 API
)

# 결과 저장
for api_type in result['api_results'].keys():
    filepath = collector.save_results(result, api_type)
    print(f"저장 완료: {filepath}")
```

### 개별 API 사용

#### API 01: 분양권전매 실거래가
```bash
# 기본 테스트
python api_01/main.py

# 특정 지역/기간 테스트
python api_01/main.py [지역코드] [계약년월]

# 예시
python api_01/main.py 11680 202312
```

#### 모듈 import 사용
```python
from api_01.api_01_silv_trade import SilvTradeAPI

api = SilvTradeAPI()
result = api.get_trade_data_parsed('11680', '202312')
print(result)
```

## API 목록

- **API 01**: 아파트 분양권전매 실거래가 자료 (`api_01/`)
  - ✅ 구현 완료
  - Base URL: `apis.data.go.kr/1613000/RTMSDataSvcSilvTrade`
  
- **API 02**: 아파트 매매 실거래가 자료 (`api_02/`)
  - ⏳ 구현 예정
  - Base URL: `apis.data.go.kr/1613000/RTMSDataSvcAptTrade`
  
- **API 03**: 아파트 매매 실거래가 상세 자료 (`api_03/`)
  - ⏳ 구현 예정
  - Base URL: `apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev`
  
- **API 04**: 아파트 전월세 실거래가 자료 (`api_04/`)
  - ⏳ 구현 예정
  - Base URL: `apis.data.go.kr/1613000/RTMSDataSvcAptRent`

## 지역코드 참고

법정동코드는 5자리 숫자로 구성됩니다.

**주요 지역코드 예시:**
- 서울특별시 종로구: `11110`
- 서울특별시 강남구: `11680`
- 서울특별시 서초구: `11650`
- 서울특별시 송파구: `11710`
- 경기도 수원시 영통구: `41117`
- 경기도 수원시 권선구: `41113`

기타 지역코드는 공공데이터포털에서 제공하는 법정동코드 목록을 참조하세요.

## 인증키

인증키는 `config.py` 파일에 저장되어 있습니다.

## 주요 기능

### 배치 데이터 수집
- 법정동코드와 기간 범위를 지정하여 여러 API에서 일괄 수집
- 자동 페이지네이션 처리 (대량 데이터 수집 지원)
- 진행 상황 실시간 표시
- 에러 처리 및 자동 재시도
- 기존 JSON 형식으로 결과 저장

### 개별 API 호출
- 각 API별 독립적인 클라이언트 클래스 제공
- XML 응답 자동 파싱 (`common.py`)
- 에러 처리 및 데이터 포맷팅

### 데이터 처리
- 중복 데이터 제거 (`backend/data_loader.py`)
- 데이터 정규화 및 필터링
- 지역별 필터링 지원
