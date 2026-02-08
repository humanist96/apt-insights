# API 01: 아파트 분양권전매 실거래가 자료

## 개요
국토교통부 공공데이터 API를 사용하여 아파트 분양권전매 실거래가 정보를 조회합니다.

## 사용법

### CLI 실행
```bash
# 기본 테스트 (종로구, 2024년 1월)
python api_01/main.py

# 특정 지역/기간 테스트
python api_01/main.py [지역코드] [계약년월]

# 예시
python api_01/main.py 11680 202312
```

### Python 모듈로 사용
```python
from api_01.api_01_silv_trade import SilvTradeAPI

api = SilvTradeAPI()
result = api.get_trade_data_parsed(
    lawd_cd='11680',  # 강남구
    deal_ymd='202312'  # 2023년 12월
)

if not result.get('error'):
    print(f"전체 건수: {result['total_count']}")
    for item in result['items']:
        print(f"아파트: {item.get('aptNm')}")
        print(f"거래금액: {item.get('dealAmount')}만원")
```

## API 정보
- Base URL: `https://apis.data.go.kr/1613000/RTMSDataSvcSilvTrade`
- Endpoint: `/getRTMSDataSvcSilvTrade`
- Method: GET

## 파일 구조
- `api_01_silv_trade.py`: API 클라이언트 클래스
- `main.py`: CLI 실행 스크립트
- `API_01_분양권전매_실거래가.md`: 상세 API 문서
- `test_results_01.md`: 테스트 결과

## 테스트 결과
✅ 정상 작동 확인
- XML 응답 파싱 정상
- 데이터 추출 정상
- CLI 출력 정상
