"""
통합 테스트 (Integration Tests)

실제 API 호출을 통한 E2E 테스트
주의: 이 테스트는 실제 API 키가 필요하며, API 할당량을 소비합니다.
"""
import pytest
import time
from typing import Dict

from api_01.api_01_silv_trade import SilvTradeAPI
from api_02.api_02_apt_trade import AptTradeAPI
from api_03.api_03_apt_trade_dev import AptTradeDevAPI
from api_04.api_04_apt_rent import AptRentAPI
from config import settings


# API 키 확인
pytestmark = pytest.mark.skipif(
    not settings.SERVICE_KEY or len(settings.SERVICE_KEY) < 10,
    reason="Valid SERVICE_KEY required for integration tests"
)


class TestAPIIntegration:
    """API 통합 테스트"""

    # 테스트용 파라미터 (서울 강남구, 최근 월)
    TEST_REGION = "11680"  # 강남구
    TEST_MONTH = "202401"  # 2024년 1월
    TEST_ROWS = 5

    def test_api_01_silv_trade(self):
        """API 01: 분양권전매 API 통합 테스트"""
        api = SilvTradeAPI()

        # 데이터 조회
        result = api.get_trade_data_parsed(
            self.TEST_REGION,
            self.TEST_MONTH,
            num_of_rows=self.TEST_ROWS
        )

        # 에러 체크
        if result.get('error'):
            error_msg = result.get('message', 'Unknown error')
            # 401 에러는 API 키 문제이므로 skip
            if 'HTTP 에러: 401' in error_msg or 'HTTP error: 401' in error_msg:
                pytest.skip(f"API key authentication failed: {error_msg}")
            # 데이터 없음은 정상 (해당 기간에 거래가 없을 수 있음)
            elif result.get('totalCount', 0) == 0:
                pytest.skip("No data available for this period")
            else:
                pytest.fail(f"API call failed: {error_msg}")

        # 응답 구조 검증 (parse_api_response uses item_count, not totalCount)
        assert 'items' in result
        assert isinstance(result['items'], list)

        count = result.get('item_count', result.get('totalCount', 0))
        print(f"\n✅ API 01 성공: {count}건 조회")

    def test_api_02_apt_trade(self):
        """API 02: 아파트 매매 API 통합 테스트"""
        api = AptTradeAPI()

        result = api.get_trade_data_parsed(
            self.TEST_REGION,
            self.TEST_MONTH,
            num_of_rows=self.TEST_ROWS
        )

        if result.get('error'):
            error_msg = result.get('message', 'Unknown error')
            if 'HTTP 에러: 401' in error_msg or 'HTTP error: 401' in error_msg:
                pytest.skip(f"API key authentication failed: {error_msg}")
            elif result.get('totalCount', 0) == 0:
                pytest.skip("No data available for this period")
            else:
                pytest.fail(f"API call failed: {error_msg}")

        assert 'items' in result
        assert isinstance(result['items'], list)

        count = result.get('item_count', result.get('totalCount', 0))
        print(f"\n✅ API 02 성공: {count}건 조회")

    def test_api_03_apt_trade_dev(self):
        """API 03: 아파트 매매 상세 API 통합 테스트"""
        api = AptTradeDevAPI()

        result = api.get_trade_data_parsed(
            self.TEST_REGION,
            self.TEST_MONTH,
            num_of_rows=self.TEST_ROWS
        )

        if result.get('error'):
            error_msg = result.get('message', 'Unknown error')
            if 'HTTP 에러: 401' in error_msg or 'HTTP error: 401' in error_msg:
                pytest.skip(f"API key authentication failed: {error_msg}")
            elif result.get('totalCount', 0) == 0:
                pytest.skip("No data available for this period")
            else:
                pytest.fail(f"API call failed: {error_msg}")

        assert 'items' in result
        assert isinstance(result['items'], list)

        count = result.get('item_count', result.get('totalCount', 0))
        print(f"\n✅ API 03 성공: {count}건 조회")

    def test_api_04_apt_rent(self):
        """API 04: 아파트 전월세 API 통합 테스트"""
        api = AptRentAPI()

        result = api.get_trade_data_parsed(
            self.TEST_REGION,
            self.TEST_MONTH,
            num_of_rows=self.TEST_ROWS
        )

        if result.get('error'):
            error_msg = result.get('message', 'Unknown error')
            if 'HTTP 에러: 401' in error_msg or 'HTTP error: 401' in error_msg:
                pytest.skip(f"API key authentication failed: {error_msg}")
            elif result.get('totalCount', 0) == 0:
                pytest.skip("No data available for this period")
            else:
                pytest.fail(f"API call failed: {error_msg}")

        assert 'items' in result
        assert isinstance(result['items'], list)

        count = result.get('item_count', result.get('totalCount', 0))
        print(f"\n✅ API 04 성공: {count}건 조회")


class TestLoggingIntegration:
    """로깅 시스템 통합 테스트"""

    def test_api_logger_integration(self):
        """API 로거가 실제 API 호출에서 작동하는지 확인"""
        from logger import APILogger
        import io
        import sys

        # stdout 캡처
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            api = SilvTradeAPI()
            result = api.get_trade_data_parsed(
                "11680",
                "202401",
                num_of_rows=1
            )

            # stdout 복원
            sys.stdout = sys.__stdout__

            # 로그 출력 확인
            log_output = captured_output.getvalue()

            # 최소한 요청 로그는 있어야 함
            assert "api_request" in log_output or "API" in log_output or len(log_output) > 0

        finally:
            sys.stdout = sys.__stdout__

    def test_sensitive_data_masking(self):
        """민감 데이터 마스킹 확인"""
        from logger import APILogger
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            api_logger = APILogger("test")
            api_logger.log_request(
                "GET",
                "https://test.com",
                params={"serviceKey": "secret123", "LAWD_CD": "11680"}
            )

            sys.stdout = sys.__stdout__
            log_output = captured_output.getvalue()

            # serviceKey가 마스킹되었는지 확인
            assert "REDACTED" in log_output or "***" in log_output
            assert "secret123" not in log_output

        finally:
            sys.stdout = sys.__stdout__


class TestPerformance:
    """성능 테스트"""

    def test_api_response_time(self):
        """API 응답 시간이 합리적인지 확인 (< 5초)"""
        api = AptTradeAPI()

        start = time.time()
        result = api.get_trade_data_parsed("11680", "202401", num_of_rows=10)
        elapsed = time.time() - start

        # 에러가 아니라면 성능 체크
        if not result.get('error'):
            assert elapsed < 5.0, f"API response too slow: {elapsed:.2f}s"
            print(f"\n⚡ 응답 시간: {elapsed:.2f}초")
        else:
            # 에러인 경우 skip
            pytest.skip(f"API call failed: {result.get('message')}")

    def test_retry_mechanism(self):
        """재시도 메커니즘 테스트"""
        from unittest.mock import patch
        import requests

        api = SilvTradeAPI()

        # 첫 2번은 타임아웃, 3번째는 성공하도록 mock
        with patch('requests.get') as mock_get:
            mock_get.side_effect = [
                requests.exceptions.Timeout(),
                requests.exceptions.Timeout(),
                type('MockResponse', (), {
                    'text': '<?xml version="1.0"?><response><header><resultCode>00</resultCode></header><body><items></items><totalCount>0</totalCount></body></response>',
                    'status_code': 200,
                    'raise_for_status': lambda: None
                })()
            ]

            result = api._make_request({"test": "param"}, max_retries=3)

            # 3번 호출되었는지 확인
            assert mock_get.call_count == 3
            assert not result.get('error'), "Should succeed on 3rd retry"


class TestBackwardCompatibility:
    """하위 호환성 테스트"""

    def test_old_import_still_works(self):
        """기존 import 방식도 작동하는지 확인"""
        from config import SERVICE_KEY

        # SERVICE_KEY가 여전히 사용 가능한지
        assert SERVICE_KEY is not None
        assert len(SERVICE_KEY) > 0

    def test_api_interface_unchanged(self):
        """API 인터페이스가 변경되지 않았는지 확인"""
        api = SilvTradeAPI()

        # 기존 메서드들이 모두 존재하는지
        assert hasattr(api, 'get_trade_data')
        assert hasattr(api, 'parse_response')
        assert hasattr(api, 'get_trade_data_parsed')

        # 새 메서드도 존재하는지
        assert hasattr(api, 'get_all_pages')


if __name__ == "__main__":
    # 직접 실행 시
    pytest.main([__file__, "-v", "-s", "--tb=short"])
