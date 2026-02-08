"""
비동기 API 클라이언트 테스트
"""
import pytest
import asyncio
import aiohttp
from datetime import datetime

# Async APIs
from api_01.async_silv_trade import AsyncSilvTradeAPI
from api_02.async_apt_trade import AsyncAptTradeAPI
from api_03.async_apt_trade_dev import AsyncAptTradeDevAPI
from api_04.async_apt_rent import AsyncAptRentAPI


@pytest.mark.asyncio
class TestAsyncAPIClient:
    """비동기 API 클라이언트 테스트"""

    async def test_async_silv_trade_api(self):
        """분양권전매 API 비동기 테스트"""
        api = AsyncSilvTradeAPI()

        async with aiohttp.ClientSession() as session:
            result = await api.get_trade_data_parsed_async(
                session=session,
                lawd_cd='11680',
                deal_ymd='202312',
                num_of_rows=5
            )

            # 응답 검증
            assert result is not None
            assert isinstance(result, dict)
            # 에러가 없거나, 데이터가 있으면 성공
            assert not result.get('error') or 'items' in result

    async def test_async_apt_trade_api(self):
        """아파트 매매 API 비동기 테스트"""
        api = AsyncAptTradeAPI()

        async with aiohttp.ClientSession() as session:
            result = await api.get_trade_data_parsed_async(
                session=session,
                lawd_cd='11680',
                deal_ymd='202312',
                num_of_rows=5
            )

            assert result is not None
            assert isinstance(result, dict)

    async def test_async_batch_collection(self):
        """여러 월 병렬 수집 테스트"""
        api = AsyncAptTradeAPI()

        date_range = ['202311', '202312']

        start_time = asyncio.get_event_loop().time()

        results = await api.get_batch_data_async(
            lawd_cd='11680',
            date_range=date_range,
            num_of_rows=5
        )

        elapsed = asyncio.get_event_loop().time() - start_time

        # 검증
        assert len(results) == len(date_range)
        print(f"\n⚡ 병렬 수집 시간: {elapsed:.2f}초")
        print(f"   월별 평균: {elapsed / len(date_range):.2f}초")

    async def test_async_performance_comparison(self):
        """동기 vs 비동기 성능 비교"""
        # 비동기 API
        async_api = AsyncAptTradeAPI()

        # 테스트 데이터
        test_months = ['202310', '202311', '202312']

        # 비동기 수집
        async_start = asyncio.get_event_loop().time()
        async_results = await async_api.get_batch_data_async(
            lawd_cd='11680',
            date_range=test_months,
            num_of_rows=5
        )
        async_elapsed = asyncio.get_event_loop().time() - async_start

        print(f"\n📊 성능 비교:")
        print(f"   비동기: {async_elapsed:.2f}초 ({len(test_months)}개월)")
        print(f"   예상 동기: ~{len(test_months) * 3:.0f}초")
        print(f"   ⚡ 성능 향상: ~{(len(test_months) * 3 / async_elapsed):.1f}x")

        # 비동기가 동기보다 빠르야 함
        expected_sync_time = len(test_months) * 3
        assert async_elapsed < expected_sync_time


@pytest.mark.asyncio
class TestAsyncAPIAllTypes:
    """모든 API 타입 통합 테스트"""

    async def test_all_apis_parallel(self):
        """4개 API를 병렬로 테스트"""
        apis = [
            AsyncSilvTradeAPI(),
            AsyncAptTradeAPI(),
            AsyncAptTradeDevAPI(),
            AsyncAptRentAPI(),
        ]

        async with aiohttp.ClientSession() as session:
            tasks = [
                api.get_trade_data_parsed_async(
                    session=session,
                    lawd_cd='11680',
                    deal_ymd='202312',
                    num_of_rows=5
                )
                for api in apis
            ]

            start_time = asyncio.get_event_loop().time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            elapsed = asyncio.get_event_loop().time() - start_time

            print(f"\n🚀 4개 API 병렬 실행:")
            print(f"   소요 시간: {elapsed:.2f}초")
            print(f"   예상 순차 실행: ~{len(apis) * 3:.0f}초")
            print(f"   성능 향상: ~{(len(apis) * 3 / elapsed):.1f}x")

            # 최소 하나의 API는 성공해야 함
            successful = [r for r in results if isinstance(r, dict) and not r.get('error')]
            assert len(successful) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
