"""
비동기 API + Redis 캐시 성능 벤치마크

Usage:
    python benchmark_async_cache.py
"""
import asyncio
import time
from datetime import datetime
from typing import List, Dict

# Sync APIs
from api_02.api_02_apt_trade import AptTradeAPI

# Async APIs
from api_02.async_apt_trade import AsyncAptTradeAPI

# Batch Collector
from batch_collector import BatchCollector

# Redis Cache
from backend.cache.redis_client import get_redis_cache


def benchmark_sync(lawd_cd: str, date_range: List[str]) -> Dict:
    """
    동기 방식 벤치마크

    Args:
        lawd_cd: 지역코드
        date_range: 계약년월 리스트

    Returns:
        벤치마크 결과
    """
    print(f"\n{'='*60}")
    print(f"🐢 동기 방식 벤치마크")
    print(f"{'='*60}")
    print(f"지역: {lawd_cd}")
    print(f"기간: {len(date_range)}개월 ({date_range[0]} ~ {date_range[-1]})")
    print(f"{'='*60}\n")

    api = AptTradeAPI()

    results = []
    start_time = time.time()

    for idx, deal_ymd in enumerate(date_range, 1):
        print(f"[{idx}/{len(date_range)}] {deal_ymd} 수집 중...", end=' ', flush=True)

        month_start = time.time()
        result = api.get_trade_data_parsed(
            lawd_cd=lawd_cd,
            deal_ymd=deal_ymd,
            num_of_rows=100
        )
        month_elapsed = time.time() - month_start

        results.append(result)
        print(f"✅ {month_elapsed:.2f}초")

        # API 호출 간 딜레이
        if idx < len(date_range):
            time.sleep(0.5)

    total_elapsed = time.time() - start_time

    # 통계
    successful = [r for r in results if not r.get('error')]
    total_items = sum(len(r.get('items', [])) for r in successful)

    print(f"\n{'='*60}")
    print(f"동기 방식 완료:")
    print(f"  - 총 시간: {total_elapsed:.2f}초")
    print(f"  - 평균 시간/월: {total_elapsed / len(date_range):.2f}초")
    print(f"  - 성공: {len(successful)}/{len(date_range)}건")
    print(f"  - 총 데이터: {total_items}건")
    print(f"{'='*60}")

    return {
        'mode': 'sync',
        'total_time': total_elapsed,
        'avg_time_per_month': total_elapsed / len(date_range),
        'successful': len(successful),
        'total_items': total_items,
    }


async def benchmark_async(lawd_cd: str, date_range: List[str]) -> Dict:
    """
    비동기 방식 벤치마크

    Args:
        lawd_cd: 지역코드
        date_range: 계약년월 리스트

    Returns:
        벤치마크 결과
    """
    print(f"\n{'='*60}")
    print(f"⚡ 비동기 방식 벤치마크")
    print(f"{'='*60}")
    print(f"지역: {lawd_cd}")
    print(f"기간: {len(date_range)}개월 ({date_range[0]} ~ {date_range[-1]})")
    print(f"병렬 처리: {len(date_range)}개 동시 요청")
    print(f"{'='*60}\n")

    api = AsyncAptTradeAPI()

    start_time = time.time()

    results = await api.get_batch_data_async(
        lawd_cd=lawd_cd,
        date_range=date_range,
        num_of_rows=100
    )

    total_elapsed = time.time() - start_time

    # 통계
    successful = [r for r in results if not r.get('error')]
    total_items = sum(len(r.get('items', [])) for r in successful)

    print(f"\n{'='*60}")
    print(f"비동기 방식 완료:")
    print(f"  - 총 시간: {total_elapsed:.2f}초")
    print(f"  - 평균 시간/월: {total_elapsed / len(date_range):.2f}초")
    print(f"  - 성공: {len(successful)}/{len(date_range)}건")
    print(f"  - 총 데이터: {total_items}건")
    print(f"{'='*60}")

    return {
        'mode': 'async',
        'total_time': total_elapsed,
        'avg_time_per_month': total_elapsed / len(date_range),
        'successful': len(successful),
        'total_items': total_items,
    }


async def benchmark_async_with_cache(lawd_cd: str, date_range: List[str]) -> Dict:
    """
    비동기 + 캐시 방식 벤치마크

    Args:
        lawd_cd: 지역코드
        date_range: 계약년월 리스트

    Returns:
        벤치마크 결과
    """
    cache = get_redis_cache()

    if not cache or not cache.is_connected():
        print("\n⚠️  Redis가 연결되지 않았습니다. 캐시 없이 비동기 방식으로 실행합니다.")
        return await benchmark_async(lawd_cd, date_range)

    print(f"\n{'='*60}")
    print(f"🚀 비동기 + 캐시 방식 벤치마크")
    print(f"{'='*60}")
    print(f"지역: {lawd_cd}")
    print(f"기간: {len(date_range)}개월 ({date_range[0]} ~ {date_range[-1]})")
    print(f"캐싱: Redis (Adaptive TTL)")
    print(f"{'='*60}\n")

    # 캐시 초기화
    cache.reset_stats()

    # 첫 번째 실행 (Cold Cache)
    print("🥶 Cold Cache (첫 실행):")
    api = AsyncAptTradeAPI()

    cold_start = time.time()
    cold_results = await api.get_batch_data_async(lawd_cd, date_range, num_of_rows=100)
    cold_elapsed = time.time() - cold_start

    cold_stats = cache.get_stats()
    print(f"  - 시간: {cold_elapsed:.2f}초")
    print(f"  - 캐시 미스: {cold_stats['misses']}")

    # 두 번째 실행 (Warm Cache)
    print("\n🔥 Warm Cache (두 번째 실행):")

    warm_start = time.time()
    warm_results = await api.get_batch_data_async(lawd_cd, date_range, num_of_rows=100)
    warm_elapsed = time.time() - warm_start

    warm_stats = cache.get_stats()
    print(f"  - 시간: {warm_elapsed:.2f}초")
    print(f"  - 캐시 히트: {warm_stats['hits']}")
    print(f"  - 캐시 히트율: {warm_stats['hit_rate_percent']:.2f}%")

    # 성능 향상
    if warm_elapsed > 0:
        speedup = cold_elapsed / warm_elapsed
        print(f"  - 🚀 성능 향상: {speedup:.1f}x")

    print(f"\n{'='*60}")
    print(f"캐시 벤치마크 완료:")
    print(f"  - Cold Cache 시간: {cold_elapsed:.2f}초")
    print(f"  - Warm Cache 시간: {warm_elapsed:.2f}초")
    print(f"  - 캐시 효과: {cold_elapsed - warm_elapsed:.2f}초 절약 ({(cold_elapsed - warm_elapsed) / cold_elapsed * 100:.1f}%)")
    print(f"{'='*60}")

    return {
        'mode': 'async_cache',
        'cold_time': cold_elapsed,
        'warm_time': warm_elapsed,
        'cache_hit_rate': warm_stats['hit_rate_percent'],
        'speedup': cold_elapsed / warm_elapsed if warm_elapsed > 0 else 0,
    }


def print_comparison(sync_result: Dict, async_result: Dict, cache_result: Dict):
    """
    벤치마크 결과 비교 출력

    Args:
        sync_result: 동기 방식 결과
        async_result: 비동기 방식 결과
        cache_result: 캐시 방식 결과
    """
    print(f"\n{'='*60}")
    print(f"📊 성능 비교 요약")
    print(f"{'='*60}\n")

    print(f"{'모드':<20} {'시간(초)':<15} {'배속':<10}")
    print(f"{'-'*60}")

    sync_time = sync_result['total_time']
    async_time = async_result['total_time']
    cache_time = cache_result.get('warm_time', async_time)

    print(f"{'🐢 동기 (Sync)':<20} {sync_time:<15.2f} {'1.0x':<10}")
    print(f"{'⚡ 비동기 (Async)':<20} {async_time:<15.2f} {f'{sync_time/async_time:.1f}x':<10}")
    print(f"{'🚀 비동기+캐시':<20} {cache_time:<15.2f} {f'{sync_time/cache_time:.1f}x':<10}")

    print(f"\n{'='*60}")
    print(f"🎯 결론:")
    print(f"  - 비동기 방식: {sync_time/async_time:.1f}x 빠름")
    print(f"  - 캐시 활용: {sync_time/cache_time:.1f}x 빠름")
    print(f"  - 목표 달성: {'✅ 성공' if (sync_time/async_time) >= 5 else '⚠️  목표 미달 (5x 이상)'}")
    print(f"  - 캐시 히트율: {cache_result.get('cache_hit_rate', 0):.1f}%")
    print(f"{'='*60}\n")


async def main():
    """메인 벤치마크 함수"""
    # 테스트 설정
    lawd_cd = '11680'  # 강남구
    date_range = ['202310', '202311', '202312']  # 3개월

    print("\n" + "="*60)
    print("🏁 비동기 API + Redis 캐시 성능 벤치마크")
    print("="*60)
    print(f"날짜: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"테스트: {lawd_cd} 지역, {len(date_range)}개월")
    print("="*60)

    # 1. 동기 방식
    sync_result = benchmark_sync(lawd_cd, date_range)

    # 2. 비동기 방식
    async_result = await benchmark_async(lawd_cd, date_range)

    # 3. 비동기 + 캐시 방식
    cache_result = await benchmark_async_with_cache(lawd_cd, date_range)

    # 4. 결과 비교
    print_comparison(sync_result, async_result, cache_result)


if __name__ == '__main__':
    asyncio.run(main())
