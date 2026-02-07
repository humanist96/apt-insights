"""
Base API Client for 국토교통부 공공데이터 API
모든 API 클라이언트가 공통으로 사용하는 베이스 클래스
"""
import requests
import time
from typing import Dict, Optional
from abc import ABC, abstractmethod

from config import SERVICE_KEY
from common import parse_xml_response, parse_api_response, API_TIMEOUT_SECONDS
from logger import get_logger, APILogger


class BaseAPIClient(ABC):
    """
    국토교통부 API 베이스 클라이언트

    모든 API 클라이언트는 이 클래스를 상속받아 구현합니다.
    공통 로직:
    - HTTP 요청 처리
    - XML/JSON 응답 파싱
    - 에러 핸들링
    - 재시도 로직 (선택적)

    서브클래스는 다음을 정의해야 합니다:
    - BASE_URL: API 기본 URL
    - ENDPOINT: API 엔드포인트 경로
    """

    # 서브클래스에서 반드시 정의해야 하는 속성
    BASE_URL: str = ""
    ENDPOINT: str = ""

    def __init__(self, service_key: str = SERVICE_KEY):
        """
        Args:
            service_key: 공공데이터포털 인증키
        """
        if not service_key:
            raise ValueError("SERVICE_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

        self.service_key = service_key

        # 서브클래스에서 BASE_URL과 ENDPOINT가 설정되었는지 확인
        if not self.BASE_URL or not self.ENDPOINT:
            raise NotImplementedError(
                f"{self.__class__.__name__}에서 BASE_URL과 ENDPOINT를 정의해야 합니다."
            )

        # API별 로거 초기화
        api_name = self.__class__.__name__.replace("API", "").lower()
        self.api_logger = APILogger(api_name)
        self.logger = get_logger(self.__class__.__name__)

    @property
    def full_url(self) -> str:
        """전체 API URL 반환"""
        return f"{self.BASE_URL}{self.ENDPOINT}"

    def _build_params(
        self,
        lawd_cd: str,
        deal_ymd: str,
        num_of_rows: int = 10,
        page_no: int = 1,
        **extra_params
    ) -> Dict:
        """
        API 요청 파라미터 생성

        Args:
            lawd_cd: 지역코드 (법정동코드 5자리)
            deal_ymd: 계약년월 (YYYYMM 형식)
            num_of_rows: 한 페이지 결과 수
            page_no: 페이지 번호
            **extra_params: 추가 파라미터

        Returns:
            API 요청 파라미터 딕셔너리
        """
        params = {
            'serviceKey': self.service_key,
            'LAWD_CD': lawd_cd,
            'DEAL_YMD': deal_ymd,
            'numOfRows': num_of_rows,
            'pageNo': page_no
        }

        # 추가 파라미터 병합
        params.update(extra_params)

        return params

    def _make_request(
        self,
        params: Dict,
        timeout: int = API_TIMEOUT_SECONDS,
        max_retries: int = 3
    ) -> Dict:
        """
        HTTP GET 요청 실행

        Args:
            params: 요청 파라미터
            timeout: 타임아웃 (초)
            max_retries: 최대 재시도 횟수

        Returns:
            파싱된 응답 데이터
        """
        url = self.full_url
        last_error = None
        start_time = time.time()

        # 요청 로깅
        self.api_logger.log_request("GET", url, params)

        for attempt in range(max_retries):
            try:
                self.logger.debug(
                    "api_request_attempt",
                    attempt=attempt + 1,
                    max_retries=max_retries,
                    url=url
                )

                response = requests.get(url, params=params, timeout=timeout)
                response.raise_for_status()

                # 응답 내용 확인
                text_response = response.text.strip()

                # 응답 성공 로깅
                response_time = time.time() - start_time
                self.api_logger.log_response(
                    status_code=response.status_code,
                    response_time=response_time,
                    response_length=len(text_response)
                )

                # XML 응답 처리
                if text_response.startswith('<?xml') or text_response.startswith('<'):
                    return parse_xml_response(text_response)

                # JSON 응답 처리
                elif text_response.startswith('{') or text_response.startswith('['):
                    return response.json()

                # 예상치 못한 형식
                else:
                    self.logger.warning(
                        "unexpected_response_format",
                        format=text_response[:100]
                    )
                    return {
                        'error': True,
                        'message': '예상치 못한 응답 형식',
                        'raw_response': text_response[:500]
                    }

            except requests.exceptions.Timeout as e:
                last_error = e
                if attempt < max_retries - 1:
                    self.api_logger.log_retry(
                        attempt=attempt + 1,
                        max_retries=max_retries,
                        reason="Timeout"
                    )
                    continue
                else:
                    self.api_logger.log_error(
                        "Request timeout after retries",
                        error_code="TIMEOUT"
                    )

            except requests.exceptions.HTTPError as e:
                last_error = e
                self.api_logger.log_error(
                    f"HTTP error: {e.response.status_code}",
                    error_code="HTTP_ERROR"
                )
                return {
                    'error': True,
                    'message': f'HTTP 에러: {e.response.status_code}',
                    'detail': str(e)
                }

            except requests.exceptions.RequestException as e:
                last_error = e
                self.api_logger.log_error(
                    "API request failed",
                    error_code="REQUEST_FAILED",
                    detail=str(e)
                )
                return {
                    'error': True,
                    'message': f'API 요청 실패: {str(e)}'
                }

            except Exception as e:
                last_error = e
                self.logger.error(
                    "response_processing_error",
                    error=str(e),
                    exc_info=True
                )
                return {
                    'error': True,
                    'message': f'응답 처리 실패: {str(e)}',
                    'raw_response': response.text[:500] if 'response' in locals() else 'N/A'
                }

        # 최대 재시도 횟수 초과
        return {
            'error': True,
            'message': f'최대 재시도 횟수 초과 ({max_retries}회)',
            'detail': str(last_error)
        }

    def get_trade_data(
        self,
        lawd_cd: str,
        deal_ymd: str,
        num_of_rows: int = 10,
        page_no: int = 1,
        **extra_params
    ) -> Dict:
        """
        실거래가 데이터 조회

        Args:
            lawd_cd: 지역코드 (법정동코드 5자리, 예: '11110')
            deal_ymd: 계약년월 (YYYYMM 형식, 예: '202401')
            num_of_rows: 한 페이지 결과 수 (기본값: 10)
            page_no: 페이지 번호 (기본값: 1)
            **extra_params: API별 추가 파라미터

        Returns:
            API 응답 데이터 (dict)
        """
        params = self._build_params(
            lawd_cd=lawd_cd,
            deal_ymd=deal_ymd,
            num_of_rows=num_of_rows,
            page_no=page_no,
            **extra_params
        )

        return self._make_request(params)

    def parse_response(self, response: Dict) -> Dict:
        """
        API 응답 파싱 및 정리

        Args:
            response: API 응답 데이터

        Returns:
            파싱된 데이터
        """
        return parse_api_response(response)

    def get_trade_data_parsed(
        self,
        lawd_cd: str,
        deal_ymd: str,
        num_of_rows: int = 10,
        page_no: int = 1,
        **extra_params
    ) -> Dict:
        """
        실거래가 데이터 조회 및 파싱 (통합 메서드)

        Args:
            lawd_cd: 지역코드 (법정동코드 5자리)
            deal_ymd: 계약년월 (YYYYMM 형식)
            num_of_rows: 한 페이지 결과 수
            page_no: 페이지 번호
            **extra_params: API별 추가 파라미터

        Returns:
            파싱된 데이터
        """
        response = self.get_trade_data(
            lawd_cd=lawd_cd,
            deal_ymd=deal_ymd,
            num_of_rows=num_of_rows,
            page_no=page_no,
            **extra_params
        )
        return self.parse_response(response)

    def get_all_pages(
        self,
        lawd_cd: str,
        deal_ymd: str,
        num_of_rows: int = 100,
        max_pages: int = 10,
        **extra_params
    ) -> Dict:
        """
        모든 페이지 데이터 조회 (페이지네이션 자동 처리)

        Args:
            lawd_cd: 지역코드
            deal_ymd: 계약년월
            num_of_rows: 페이지당 결과 수 (최대 100 권장)
            max_pages: 최대 페이지 수 (무한 루프 방지)
            **extra_params: API별 추가 파라미터

        Returns:
            모든 페이지 데이터를 합친 결과
        """
        all_items = []
        page_no = 1
        total_count = 0

        while page_no <= max_pages:
            self.logger.info(
                "fetching_page",
                page=page_no,
                max_pages=max_pages,
                lawd_cd=lawd_cd,
                deal_ymd=deal_ymd
            )

            result = self.get_trade_data_parsed(
                lawd_cd=lawd_cd,
                deal_ymd=deal_ymd,
                num_of_rows=num_of_rows,
                page_no=page_no,
                **extra_params
            )

            # 에러 체크
            if result.get('error'):
                self.logger.error(
                    "page_fetch_failed",
                    page=page_no,
                    error=result.get('message')
                )
                break

            # 첫 페이지에서 전체 개수 확인
            if page_no == 1:
                total_count = result.get('totalCount', 0)
                self.logger.info(
                    "total_count_detected",
                    total_count=total_count
                )

            # 아이템 추가
            items = result.get('items', [])
            if not items:
                self.logger.info(
                    "no_more_items",
                    page=page_no
                )
                break

            all_items.extend(items)
            self.logger.info(
                "page_collected",
                page=page_no,
                items_in_page=len(items),
                total_collected=len(all_items)
            )

            # 전체 데이터를 다 가져왔으면 종료
            if len(all_items) >= total_count:
                self.logger.info(
                    "all_data_collected",
                    total_items=len(all_items)
                )
                break

            page_no += 1

        return {
            'totalCount': len(all_items),
            'items': all_items,
            'numOfRows': num_of_rows,
            'pageNo': page_no,
            'error': False
        }


class RateLimitedAPIClient(BaseAPIClient):
    """
    Rate Limiting이 적용된 API 클라이언트
    (Phase 1에서 사용 예정)
    """

    def __init__(self, service_key: str = SERVICE_KEY, calls_per_second: int = 10):
        super().__init__(service_key)
        self.calls_per_second = calls_per_second
        # TODO: Phase 1에서 Redis 기반 Rate Limiter 구현
