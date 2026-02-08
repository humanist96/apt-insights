# API 1: 아파트 분양권전매 실거래가 자료

## 개요
국토교통부에서 제공하는 아파트 분양권전매 실거래가 공개 자료 API입니다. 아파트 분양권 전매 거래 정보를 조회할 수 있습니다.

## 기본 정보
- **제공기관**: 국토교통부
- **Base URL**: `https://apis.data.go.kr/1613000/RTMSDataSvcSilvTrade`
- **HTTP Method**: `GET`
- **엔드포인트**: `/getRTMSDataSvcSilvTrade`
- **인증 방식**: Service Key (공공데이터포털 인증키)

## 요청 파라미터

| 파라미터명 | 타입 | 필수 | 설명 | 예시 |
|-----------|------|------|------|------|
| serviceKey | string | 필수 | 공공데이터포털에서 발급받은 인증키 | `YOUR_SERVICE_KEY` |
| LAWD_CD | string | 필수 | 지역코드 (법정동코드 5자리) | `11110` (서울특별시 종로구) |
| DEAL_YMD | string | 필수 | 계약년월 (YYYYMM 형식) | `202401` |
| numOfRows | number | 선택 | 한 페이지 결과 수 (기본값: 10) | `10` |
| pageNo | number | 선택 | 페이지 번호 (기본값: 1) | `1` |

### 지역코드 (LAWD_CD) 참고
- 법정동코드 5자리 사용
- 예: 서울특별시 종로구 = `11110`, 강남구 = `11680`
- 전체 지역코드는 공공데이터포털에서 제공하는 법정동코드 목록 참조

## 요청 예시

### cURL
```bash
curl "https://apis.data.go.kr/1613000/RTMSDataSvcSilvTrade/getRTMSDataSvcSilvTrade?serviceKey=YOUR_SERVICE_KEY&LAWD_CD=11110&DEAL_YMD=202401&numOfRows=10&pageNo=1"
```

### JavaScript (fetch)
```javascript
const serviceKey = 'YOUR_SERVICE_KEY';
const lawdCd = '11110'; // 종로구
const dealYmd = '202401'; // 2024년 1월
const numOfRows = 10;
const pageNo = 1;

const url = `https://apis.data.go.kr/1613000/RTMSDataSvcSilvTrade/getRTMSDataSvcSilvTrade?serviceKey=${serviceKey}&LAWD_CD=${lawdCd}&DEAL_YMD=${dealYmd}&numOfRows=${numOfRows}&pageNo=${pageNo}`;

fetch(url)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

### Python (requests)
```python
import requests

service_key = 'YOUR_SERVICE_KEY'
lawd_cd = '11110'  # 종로구
deal_ymd = '202401'  # 2024년 1월
num_of_rows = 10
page_no = 1

url = 'https://apis.data.go.kr/1613000/RTMSDataSvcSilvTrade/getRTMSDataSvcSilvTrade'
params = {
    'serviceKey': service_key,
    'LAWD_CD': lawd_cd,
    'DEAL_YMD': deal_ymd,
    'numOfRows': num_of_rows,
    'pageNo': page_no
}

response = requests.get(url, params=params)
data = response.json()
print(data)
```

## 응답 구조

### 성공 응답 (200 OK)

```json
{
  "response": {
    "header": {
      "resultCode": "00",
      "resultMsg": "NORMAL_SERVICE"
    },
    "body": {
      "items": {
        "item": [
          {
            "거래금액": "50000",
            "건축년도": "2010",
            "년": "2024",
            "법정동": "청와대로",
            "아파트": "청와대아파트",
            "월": "1",
            "일": "15",
            "전용면적": "84.95",
            "지번": "1",
            "지역코드": "11110",
            "층": "5"
          }
        ]
      },
      "numOfRows": 10,
      "pageNo": 1,
      "totalCount": 1
    }
  }
}
```

### 응답 필드 설명

#### Header
| 필드명 | 타입 | 설명 |
|--------|------|------|
| resultCode | string | 결과코드 (`00`: 정상, 그 외: 오류) |
| resultMsg | string | 결과메시지 |

#### Body
| 필드명 | 타입 | 설명 |
|--------|------|------|
| totalCount | number | 전체 결과 수 |
| numOfRows | number | 한 페이지 결과 수 |
| pageNo | number | 현재 페이지 번호 |
| items.item[] | array | 거래 정보 배열 |

#### Item 필드
| 필드명 | 타입 | 설명 |
|--------|------|------|
| 거래금액 | string | 거래금액 (만원 단위, 쉼표 제거) |
| 건축년도 | string | 건축년도 |
| 년 | string | 계약년도 |
| 법정동 | string | 법정동명 |
| 아파트 | string | 아파트명 |
| 월 | string | 계약월 |
| 일 | string | 계약일 |
| 전용면적 | string | 전용면적 (㎡) |
| 지번 | string | 지번 |
| 지역코드 | string | 지역코드 (법정동코드) |
| 층 | string | 층수 |

## 에러 코드

| resultCode | resultMsg | 설명 |
|------------|-----------|------|
| 00 | NORMAL_SERVICE | 정상 처리 |
| 01 | APPLICATION_ERROR | 어플리케이션 에러 |
| 02 | DB_ERROR | 데이터베이스 에러 |
| 03 | NODATA_ERROR | 데이터 없음 |
| 04 | HTTP_ERROR | HTTP 에러 |
| 05 | SERVICETIME_OUT | 서비스 연결 실패 |
| 10 | INVALID_REQUEST_PARAMETER_ERROR | 잘못된 요청 파라미터 |
| 11 | NO_MANDATORY_REQUEST_PARAMETERS_ERROR | 필수 파라미터 누락 |
| 12 | NO_OPENAPI_SERVICE_ERROR | 해당 오픈API 서비스가 없거나 폐기됨 |
| 20 | SERVICE_ACCESS_DENIED_ERROR | 서비스 접근 거부 |
| 22 | LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR | 서비스 요청제한횟수 초과 |
| 30 | SERVICE_KEY_IS_NOT_REGISTERED_ERROR | 등록되지 않은 서비스키 |
| 31 | DEADLINE_HAS_EXPIRED_ERROR | 기한 만료된 서비스키 |
| 32 | UNREGISTERED_IP_ERROR | 등록되지 않은 IP |
| 33 | UNSIGNED_CALL_ERROR | 서명되지 않은 호출 |

## 주의사항
1. **인증키**: 공공데이터포털에서 발급받은 서비스키를 사용해야 합니다.
2. **요청 제한**: 일일 요청 횟수 제한이 있을 수 있습니다.
3. **데이터 지연**: 실거래가 데이터는 등기 완료 후 공개되므로 1-2개월 지연될 수 있습니다.
4. **지역코드**: 정확한 법정동코드를 사용해야 합니다.
5. **계약년월**: YYYYMM 형식으로 입력해야 합니다 (예: 202401).

## 참고사항
- 공공데이터포털: https://www.data.go.kr
- 법정동코드 조회: 공공데이터포털에서 제공하는 법정동코드 API 참조
- 데이터 제공 주기: 매월 업데이트
