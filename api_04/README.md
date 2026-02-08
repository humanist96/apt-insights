# API 04: 아파트 전월세 실거래가 자료

## 개요
국토교통부 공공데이터 API를 사용하여 아파트 전세 및 월세 실거래가 정보를 조회합니다.

## 상태
⏳ 구현 예정

## API 정보
- Base URL: `https://apis.data.go.kr/1613000/RTMSDataSvcAptRent`
- Endpoint: `/getRTMSDataSvcAptRent`
- Method: GET

## 파일 구조
- `API_04_전월세_실거래가.md`: 상세 API 문서

## 특징
- 전세와 월세 데이터를 함께 제공
- 월세의 경우 "보증금/월세" 형식으로 제공
- 거래유형 필드로 전세/월세 구분
