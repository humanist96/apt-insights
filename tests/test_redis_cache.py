"""
Redis 캐시 테스트
"""
import pytest
import time
from datetime import datetime

from backend.cache.redis_client import RedisCache, get_redis_cache, USE_REDIS


@pytest.mark.skipif(not USE_REDIS, reason="Redis가 비활성화되어 있습니다")
class TestRedisCache:
    """Redis 캐시 테스트"""

    @pytest.fixture
    def cache(self):
        """캐시 인스턴스 생성"""
        cache = get_redis_cache()
        if cache:
            # 테스트 전 통계 초기화
            cache.reset_stats()
        return cache

    def test_connection(self, cache):
        """Redis 연결 테스트"""
        if not cache:
            pytest.skip("Redis 연결 실패")

        assert cache.is_connected() is True

    def test_set_and_get(self, cache):
        """캐시 설정 및 조회 테스트"""
        if not cache:
            pytest.skip("Redis 연결 실패")

        # 테스트 데이터
        test_data = {
            'items': [
                {'아파트': '테스트아파트', '거래금액': '100,000'},
                {'아파트': '테스트아파트2', '거래금액': '200,000'},
            ],
            'totalCount': 2,
            'error': False
        }

        # 캐시 저장
        success = cache.set(
            api_type='api_02',
            lawd_cd='11680',
            deal_ymd='202312',
            data=test_data,
            ttl=60  # 1분
        )
        assert success is True

        # 캐시 조회
        cached_data = cache.get(
            api_type='api_02',
            lawd_cd='11680',
            deal_ymd='202312'
        )

        assert cached_data is not None
        assert cached_data['totalCount'] == 2
        assert len(cached_data['items']) == 2

    def test_cache_hit_and_miss(self, cache):
        """캐시 히트/미스 테스트"""
        if not cache:
            pytest.skip("Redis 연결 실패")

        # 통계 초기화
        cache.reset_stats()

        # 캐시 미스 (존재하지 않는 키)
        result = cache.get('api_02', '99999', '209901')
        assert result is None
        assert cache.stats['misses'] == 1

        # 캐시 설정
        cache.set('api_02', '11680', '202312', {'test': 'data'})

        # 캐시 히트
        result = cache.get('api_02', '11680', '202312')
        assert result is not None
        assert cache.stats['hits'] == 1

        # 통계 확인
        stats = cache.get_stats()
        assert stats['hits'] >= 1
        assert stats['misses'] >= 1
        assert stats['hit_rate_percent'] >= 0

    def test_adaptive_ttl(self, cache):
        """Adaptive TTL 테스트"""
        if not cache:
            pytest.skip("Redis 연결 실패")

        # 현재 월
        current_month = datetime.now().strftime('%Y%m')
        ttl_current = cache._calculate_ttl(current_month)
        assert ttl_current == 3600  # 1시간

        # 과거 데이터
        ttl_historical = cache._calculate_ttl('202001')
        assert ttl_historical == 604800  # 7일

        print(f"\n📊 Adaptive TTL:")
        print(f"   현재 월 ({current_month}): {ttl_current}초 (1시간)")
        print(f"   과거 (202001): {ttl_historical}초 (7일)")

    def test_cache_delete(self, cache):
        """캐시 삭제 테스트"""
        if not cache:
            pytest.skip("Redis 연결 실패")

        # 데이터 저장
        cache.set('api_02', '11680', '202312', {'test': 'data'})

        # 존재 확인
        assert cache.get('api_02', '11680', '202312') is not None

        # 삭제
        deleted = cache.delete('api_02', '11680', '202312')
        assert deleted is True

        # 삭제 확인
        assert cache.get('api_02', '11680', '202312') is None

    def test_cache_performance(self, cache):
        """캐시 성능 테스트"""
        if not cache:
            pytest.skip("Redis 연결 실패")

        test_data = {
            'items': [{'data': i} for i in range(100)],
            'totalCount': 100
        }

        # 캐시 설정 성능
        set_times = []
        for i in range(10):
            start = time.time()
            cache.set('api_02', '11680', f'20231{i%10}', test_data)
            elapsed = time.time() - start
            set_times.append(elapsed)

        avg_set_time = sum(set_times) / len(set_times)

        # 캐시 조회 성능
        get_times = []
        for i in range(10):
            start = time.time()
            cache.get('api_02', '11680', f'20231{i%10}')
            elapsed = time.time() - start
            get_times.append(elapsed)

        avg_get_time = sum(get_times) / len(get_times)

        print(f"\n⚡ 캐시 성능:")
        print(f"   평균 설정 시간: {avg_set_time*1000:.2f}ms")
        print(f"   평균 조회 시간: {avg_get_time*1000:.2f}ms")

        # 캐시는 10ms 이내여야 함
        assert avg_get_time < 0.01  # 10ms


@pytest.mark.skipif(not USE_REDIS, reason="Redis가 비활성화되어 있습니다")
class TestCacheIntegration:
    """캐시 통합 테스트"""

    def test_cache_stats(self):
        """캐시 통계 조회 테스트"""
        cache = get_redis_cache()
        if not cache:
            pytest.skip("Redis 연결 실패")

        stats = cache.get_stats()

        assert 'hits' in stats
        assert 'misses' in stats
        assert 'sets' in stats
        assert 'hit_rate_percent' in stats
        assert 'connected' in stats

        print(f"\n📊 현재 캐시 통계:")
        print(f"   히트: {stats['hits']}")
        print(f"   미스: {stats['misses']}")
        print(f"   저장: {stats['sets']}")
        print(f"   히트율: {stats['hit_rate_percent']:.2f}%")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
