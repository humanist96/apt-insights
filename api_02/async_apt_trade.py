"""
API 02: 아파트 매매 실거래가 자료 (Async Version)
aiohttp 기반 비동기 API 클라이언트
"""
import sys
from pathlib import Path

# 상위 디렉토리의 모듈 import
sys.path.insert(0, str(Path(__file__).parent.parent))

from async_api_client import AsyncAPIClient
from config import SERVICE_KEY


class AsyncAptTradeAPI(AsyncAPIClient):
    """아파트 매매 실거래가 API 비동기 클라이언트"""

    BASE_URL = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade"
    ENDPOINT = "/getRTMSDataSvcAptTrade"

    def __init__(self, service_key: str = SERVICE_KEY):
        """
        Args:
            service_key: 공공데이터포털 인증키
        """
        super().__init__(service_key)


if __name__ == "__main__":
    import asyncio
    import aiohttp

    async def test():
        api = AsyncAptTradeAPI()
        print(f"✅ Async API 클라이언트 초기화 성공")
        print(f"   URL: {api.full_url}")

        # 간단한 비동기 테스트
        async with aiohttp.ClientSession() as session:
            result = await api.get_trade_data_parsed_async(
                session=session,
                lawd_cd='11680',
                deal_ymd='202312',
                num_of_rows=5
            )
            print(f"   응답 레코드: {len(result.get('items', []))}개")

    asyncio.run(test())
