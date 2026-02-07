"""
API 01: 아파트 분양권전매 실거래가 자료
국토교통부 공공데이터 API

BaseAPIClient를 사용한 리팩토링 버전
"""
import sys
from pathlib import Path

# 상위 디렉토리의 모듈 import
sys.path.insert(0, str(Path(__file__).parent.parent))

from base_api_client import BaseAPIClient
from config import SERVICE_KEY


class SilvTradeAPI(BaseAPIClient):
    """아파트 분양권전매 실거래가 API 클라이언트"""

    BASE_URL = "https://apis.data.go.kr/1613000/RTMSDataSvcSilvTrade"
    ENDPOINT = "/getRTMSDataSvcSilvTrade"

    def __init__(self, service_key: str = SERVICE_KEY):
        """
        Args:
            service_key: 공공데이터포털 인증키
        """
        super().__init__(service_key)

    # 모든 핵심 기능은 BaseAPIClient에서 상속됨:
    # - get_trade_data()
    # - parse_response()
    # - get_trade_data_parsed()
    # - get_all_pages()


# 하위 호환성을 위한 별칭 (점진적 마이그레이션용)
if __name__ == "__main__":
    # 테스트 코드
    api = SilvTradeAPI()
    print(f"✅ API 클라이언트 초기화 성공")
    print(f"   URL: {api.full_url}")

    # 샘플 조회 (실제 API 호출)
    print("\n📡 API 테스트 (강남구 2023-12)...")
    result = api.get_trade_data_parsed('11680', '202312', num_of_rows=5)

    if result.get('error'):
        print(f"❌ 에러: {result.get('message')}")
    else:
        print(f"✅ 성공: {result.get('totalCount', 0)}건 조회")
        items = result.get('items', [])
        if items:
            print(f"   첫 번째 항목: {items[0].get('아파트', 'N/A')}")
