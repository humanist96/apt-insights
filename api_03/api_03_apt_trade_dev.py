"""
API 03: 아파트 매매 실거래 상세 자료
국토교통부 공공데이터 API

BaseAPIClient를 사용한 리팩토링 버전
"""
import sys
from pathlib import Path

# 상위 디렉토리의 모듈 import
sys.path.insert(0, str(Path(__file__).parent.parent))

from base_api_client import BaseAPIClient
from config import SERVICE_KEY


class AptTradeDevAPI(BaseAPIClient):
    """아파트 매매 실거래 상세 API 클라이언트"""

    BASE_URL = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev"
    ENDPOINT = "/getRTMSDataSvcAptTradeDev"

    def __init__(self, service_key: str = SERVICE_KEY):
        """
        Args:
            service_key: 공공데이터포털 인증키
        """
        super().__init__(service_key)


if __name__ == "__main__":
    # 테스트 코드
    api = AptTradeDevAPI()
    print(f"✅ API 클라이언트 초기화 성공")
    print(f"   URL: {api.full_url}")
