"""
BaseAPIClient 단위 테스트

pytest를 사용하여 BaseAPIClient의 핵심 기능을 테스트합니다.
"""
import pytest
from unittest.mock import Mock, patch
import requests

from base_api_client import BaseAPIClient
from config import SERVICE_KEY


class TestAPIClient(BaseAPIClient):
    """테스트용 API 클라이언트"""
    BASE_URL = "https://test.api.com"
    ENDPOINT = "/test"


class TestBaseAPIClientInitialization:
    """BaseAPIClient 초기화 테스트"""

    def test_init_with_service_key(self):
        """서비스 키로 초기화"""
        client = TestAPIClient(service_key="test_key")
        assert client.service_key == "test_key"

    def test_init_with_default_service_key(self):
        """기본 서비스 키로 초기화"""
        client = TestAPIClient()
        assert client.service_key == SERVICE_KEY

    def test_init_without_service_key_raises_error(self):
        """서비스 키 없이 초기화하면 에러 발생"""
        with pytest.raises(ValueError, match="SERVICE_KEY가 설정되지 않았습니다"):
            TestAPIClient(service_key="")

    def test_full_url_property(self):
        """전체 URL 프로퍼티"""
        client = TestAPIClient()
        assert client.full_url == "https://test.api.com/test"


class TestBaseAPIClientBuildParams:
    """파라미터 빌더 테스트"""

    def test_build_params_basic(self):
        """기본 파라미터 생성"""
        client = TestAPIClient()
        params = client._build_params(
            lawd_cd="11680",
            deal_ymd="202312"
        )

        assert params['serviceKey'] == client.service_key
        assert params['LAWD_CD'] == "11680"
        assert params['DEAL_YMD'] == "202312"
        assert params['numOfRows'] == 10
        assert params['pageNo'] == 1

    def test_build_params_custom(self):
        """커스텀 파라미터"""
        client = TestAPIClient()
        params = client._build_params(
            lawd_cd="11680",
            deal_ymd="202312",
            num_of_rows=50,
            page_no=2
        )

        assert params['numOfRows'] == 50
        assert params['pageNo'] == 2

    def test_build_params_extra(self):
        """추가 파라미터"""
        client = TestAPIClient()
        params = client._build_params(
            lawd_cd="11680",
            deal_ymd="202312",
            extra_param="value"
        )

        assert params['extra_param'] == "value"


class TestBaseAPIClientMakeRequest:
    """HTTP 요청 테스트"""

    @patch('base_api_client.requests.get')
    def test_make_request_xml_success(self, mock_get):
        """XML 응답 성공"""
        # Mock XML 응답
        mock_response = Mock()
        mock_response.text = """<?xml version="1.0"?>
        <response>
            <header>
                <resultCode>00</resultCode>
                <resultMsg>SUCCESS</resultMsg>
            </header>
            <body>
                <items>
                    <item>
                        <아파트>테스트아파트</아파트>
                    </item>
                </items>
            </body>
        </response>"""
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = TestAPIClient()
        params = {'test': 'value'}

        result = client._make_request(params)

        # 요청이 호출되었는지 확인
        mock_get.assert_called_once()
        assert 'error' not in result or not result.get('error')

    @patch('base_api_client.requests.get')
    def test_make_request_http_error(self, mock_get):
        """HTTP 에러 처리"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        client = TestAPIClient()
        params = {'test': 'value'}

        result = client._make_request(params)

        assert result['error'] is True
        assert 'HTTP 에러' in result['message']

    @patch('base_api_client.requests.get')
    def test_make_request_timeout_retry(self, mock_get):
        """타임아웃 재시도"""
        mock_get.side_effect = requests.exceptions.Timeout()

        client = TestAPIClient()
        params = {'test': 'value'}

        result = client._make_request(params, max_retries=3)

        # 3번 재시도 확인
        assert mock_get.call_count == 3
        assert result['error'] is True
        assert '최대 재시도' in result['message']

    @patch('base_api_client.requests.get')
    def test_make_request_unexpected_format(self, mock_get):
        """예상치 못한 응답 형식"""
        mock_response = Mock()
        mock_response.text = "Unexpected response format"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = TestAPIClient()
        params = {'test': 'value'}

        result = client._make_request(params)

        assert result['error'] is True
        assert '예상치 못한 응답 형식' in result['message']


class TestBaseAPIClientGetTradeData:
    """거래 데이터 조회 테스트"""

    @patch.object(TestAPIClient, '_make_request')
    def test_get_trade_data(self, mock_request):
        """거래 데이터 조회"""
        mock_request.return_value = {'totalCount': 10, 'items': []}

        client = TestAPIClient()
        result = client.get_trade_data('11680', '202312')

        # _make_request가 호출되었는지 확인
        mock_request.assert_called_once()

        # 파라미터 확인
        call_args = mock_request.call_args[0][0]
        assert call_args['LAWD_CD'] == '11680'
        assert call_args['DEAL_YMD'] == '202312'

    @patch.object(TestAPIClient, '_make_request')
    def test_get_trade_data_parsed(self, mock_request):
        """거래 데이터 조회 및 파싱"""
        mock_request.return_value = {
            'header': {'resultCode': '00'},
            'body': {
                'totalCount': 1,
                'items': [{'아파트': '테스트'}]
            }
        }

        client = TestAPIClient()
        result = client.get_trade_data_parsed('11680', '202312')

        # parse_response를 통과했는지 확인
        assert 'items' in result or 'error' in result


class TestBaseAPIClientGetAllPages:
    """전체 페이지 조회 테스트"""

    @patch.object(TestAPIClient, 'get_trade_data_parsed')
    def test_get_all_pages_single_page(self, mock_parsed):
        """단일 페이지 조회"""
        mock_parsed.return_value = {
            'totalCount': 5,
            'items': [{'id': i} for i in range(5)],
            'error': False
        }

        client = TestAPIClient()
        result = client.get_all_pages('11680', '202312', num_of_rows=10)

        assert len(result['items']) == 5
        assert result['totalCount'] == 5

    @patch.object(TestAPIClient, 'get_trade_data_parsed')
    def test_get_all_pages_multiple_pages(self, mock_parsed):
        """다중 페이지 조회"""
        # 첫 번째 페이지: 100개 (totalCount=150)
        # 두 번째 페이지: 50개
        # 세 번째 페이지: 빈 리스트 (종료)
        mock_parsed.side_effect = [
            {
                'totalCount': 150,
                'items': [{'id': i} for i in range(100)],
                'error': False
            },
            {
                'totalCount': 150,
                'items': [{'id': i} for i in range(100, 150)],
                'error': False
            },
            {
                'totalCount': 150,
                'items': [],
                'error': False
            }
        ]

        client = TestAPIClient()
        result = client.get_all_pages('11680', '202312', num_of_rows=100)

        assert len(result['items']) == 150
        assert result['totalCount'] == 150
        assert mock_parsed.call_count == 2  # 세 번째는 빈 결과라 중단

    @patch.object(TestAPIClient, 'get_trade_data_parsed')
    def test_get_all_pages_error(self, mock_parsed):
        """에러 발생 시 중단"""
        mock_parsed.return_value = {
            'error': True,
            'message': 'API 에러'
        }

        client = TestAPIClient()
        result = client.get_all_pages('11680', '202312')

        assert len(result['items']) == 0
        assert mock_parsed.call_count == 1


class TestBaseAPIClientSubclassValidation:
    """서브클래스 검증 테스트"""

    def test_missing_base_url_raises_error(self):
        """BASE_URL 없이 초기화하면 에러"""
        class IncompleteClient(BaseAPIClient):
            ENDPOINT = "/test"

        with pytest.raises(NotImplementedError, match="BASE_URL과 ENDPOINT를 정의"):
            IncompleteClient()

    def test_missing_endpoint_raises_error(self):
        """ENDPOINT 없이 초기화하면 에러"""
        class IncompleteClient(BaseAPIClient):
            BASE_URL = "https://test.com"

        with pytest.raises(NotImplementedError, match="BASE_URL과 ENDPOINT를 정의"):
            IncompleteClient()


# Pytest 설정
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
