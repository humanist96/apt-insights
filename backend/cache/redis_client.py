"""
Redis 캐싱 클라이언트
Adaptive TTL 기반 API 응답 캐싱
"""
import os
import json
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

try:
    import redis
    from redis import Redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from logger import get_logger

# 환경변수 로드
load_dotenv()

# Redis 사용 여부
USE_REDIS = os.getenv('USE_REDIS', 'False').lower() == 'true'
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Adaptive TTL 설정 (초)
CACHE_TTL_CURRENT_MONTH = int(os.getenv('CACHE_TTL_CURRENT_MONTH', '3600'))      # 1시간
CACHE_TTL_RECENT_MONTHS = int(os.getenv('CACHE_TTL_RECENT_MONTHS', '21600'))     # 6시간
CACHE_TTL_HISTORICAL = int(os.getenv('CACHE_TTL_HISTORICAL', '604800'))          # 7일


class RedisCache:
    """
    Redis 기반 캐싱 클라이언트

    Features:
    - Adaptive TTL (최신 데이터 짧게, 과거 데이터 길게)
    - 자동 직렬화/역직렬화
    - 캐시 통계 추적
    - CLI 관리 명령어

    TTL 전략:
    - 현재 월: 1시간 (자주 변경됨)
    - 최근 3개월: 6시간 (간헐적 변경)
    - 과거 데이터: 7일 (거의 변경 안 됨)
    """

    def __init__(self, url: str = REDIS_URL):
        """
        Args:
            url: Redis 연결 URL
        """
        if not REDIS_AVAILABLE:
            raise ImportError(
                "redis 모듈이 설치되지 않았습니다. "
                "설치: pip install redis hiredis"
            )

        self.logger = get_logger(__name__)
        self.url = url
        self.client: Optional[Redis] = None
        self.stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'errors': 0,
        }

        # Redis 연결 시도
        self._connect()

    def _connect(self):
        """Redis 연결"""
        try:
            self.client = redis.from_url(
                self.url,
                encoding='utf-8',
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # 연결 테스트
            self.client.ping()
            self.logger.info("redis_connected", url=self.url)
        except Exception as e:
            self.logger.error("redis_connection_failed", error=str(e))
            self.client = None

    def is_connected(self) -> bool:
        """Redis 연결 상태 확인"""
        if not self.client:
            return False
        try:
            self.client.ping()
            return True
        except:
            return False

    def _calculate_ttl(self, deal_ymd: str) -> int:
        """
        Adaptive TTL 계산

        Args:
            deal_ymd: 계약년월 (YYYYMM 형식)

        Returns:
            TTL (초)
        """
        try:
            deal_date = datetime.strptime(deal_ymd, '%Y%m')
            now = datetime.now()
            current_month = now.strftime('%Y%m')

            # 현재 월: 1시간
            if deal_ymd == current_month:
                return CACHE_TTL_CURRENT_MONTH

            # 최근 3개월: 6시간
            three_months_ago = now - timedelta(days=90)
            if deal_date >= three_months_ago:
                return CACHE_TTL_RECENT_MONTHS

            # 과거 데이터: 7일
            return CACHE_TTL_HISTORICAL

        except ValueError:
            # 날짜 파싱 실패 시 기본 TTL
            self.logger.warning("invalid_date_format", deal_ymd=deal_ymd)
            return CACHE_TTL_RECENT_MONTHS

    def _build_key(
        self,
        api_type: str,
        lawd_cd: str,
        deal_ymd: str,
        extra: Optional[str] = None
    ) -> str:
        """
        캐시 키 생성

        Args:
            api_type: API 타입 (api_01, api_02, etc.)
            lawd_cd: 지역코드
            deal_ymd: 계약년월
            extra: 추가 식별자 (선택)

        Returns:
            Redis 키
        """
        parts = ['apt_insights', api_type, lawd_cd, deal_ymd]
        if extra:
            parts.append(extra)
        return ':'.join(parts)

    def get(
        self,
        api_type: str,
        lawd_cd: str,
        deal_ymd: str,
        extra: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        캐시에서 데이터 조회

        Args:
            api_type: API 타입
            lawd_cd: 지역코드
            deal_ymd: 계약년월
            extra: 추가 식별자

        Returns:
            캐시된 데이터 (없으면 None)
        """
        if not self.is_connected():
            self.stats['errors'] += 1
            return None

        key = self._build_key(api_type, lawd_cd, deal_ymd, extra)

        try:
            start_time = time.time()
            data = self.client.get(key)
            elapsed = time.time() - start_time

            if data:
                self.stats['hits'] += 1
                self.logger.debug(
                    "cache_hit",
                    key=key,
                    response_time=f"{elapsed*1000:.2f}ms"
                )
                return json.loads(data)
            else:
                self.stats['misses'] += 1
                self.logger.debug("cache_miss", key=key)
                return None

        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error("cache_get_error", key=key, error=str(e))
            return None

    def set(
        self,
        api_type: str,
        lawd_cd: str,
        deal_ymd: str,
        data: Dict[str, Any],
        extra: Optional[str] = None,
        ttl: Optional[int] = None
    ) -> bool:
        """
        데이터를 캐시에 저장

        Args:
            api_type: API 타입
            lawd_cd: 지역코드
            deal_ymd: 계약년월
            data: 저장할 데이터
            extra: 추가 식별자
            ttl: TTL (None이면 자동 계산)

        Returns:
            성공 여부
        """
        if not self.is_connected():
            self.stats['errors'] += 1
            return False

        key = self._build_key(api_type, lawd_cd, deal_ymd, extra)

        # TTL 계산
        if ttl is None:
            ttl = self._calculate_ttl(deal_ymd)

        try:
            start_time = time.time()
            serialized = json.dumps(data, ensure_ascii=False)
            self.client.setex(key, ttl, serialized)
            elapsed = time.time() - start_time

            self.stats['sets'] += 1
            self.logger.debug(
                "cache_set",
                key=key,
                ttl=ttl,
                size=len(serialized),
                response_time=f"{elapsed*1000:.2f}ms"
            )
            return True

        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error("cache_set_error", key=key, error=str(e))
            return False

    def delete(
        self,
        api_type: str,
        lawd_cd: str,
        deal_ymd: str,
        extra: Optional[str] = None
    ) -> bool:
        """
        캐시 삭제

        Args:
            api_type: API 타입
            lawd_cd: 지역코드
            deal_ymd: 계약년월
            extra: 추가 식별자

        Returns:
            성공 여부
        """
        if not self.is_connected():
            return False

        key = self._build_key(api_type, lawd_cd, deal_ymd, extra)

        try:
            deleted = self.client.delete(key)
            self.logger.debug("cache_delete", key=key, deleted=deleted)
            return bool(deleted)
        except Exception as e:
            self.logger.error("cache_delete_error", key=key, error=str(e))
            return False

    def clear_all(self, pattern: str = 'apt_insights:*') -> int:
        """
        패턴에 매칭되는 모든 캐시 삭제

        Args:
            pattern: Redis 키 패턴

        Returns:
            삭제된 키 개수
        """
        if not self.is_connected():
            return 0

        try:
            keys = self.client.keys(pattern)
            if keys:
                deleted = self.client.delete(*keys)
                self.logger.info("cache_cleared", pattern=pattern, deleted=deleted)
                return deleted
            return 0
        except Exception as e:
            self.logger.error("cache_clear_error", pattern=pattern, error=str(e))
            return 0

    def get_stats(self) -> Dict[str, Any]:
        """
        캐시 통계 조회

        Returns:
            통계 정보
        """
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0

        stats = {
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'sets': self.stats['sets'],
            'errors': self.stats['errors'],
            'total_requests': total_requests,
            'hit_rate_percent': round(hit_rate, 2),
            'connected': self.is_connected(),
        }

        # Redis 서버 정보 추가
        if self.is_connected():
            try:
                info = self.client.info('stats')
                stats.update({
                    'server_hits': info.get('keyspace_hits', 0),
                    'server_misses': info.get('keyspace_misses', 0),
                    'total_keys': self.client.dbsize(),
                })
            except:
                pass

        return stats

    def reset_stats(self):
        """통계 초기화"""
        self.stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'errors': 0,
        }
        self.logger.info("cache_stats_reset")


# 싱글톤 인스턴스
_redis_cache: Optional[RedisCache] = None


def get_redis_cache() -> Optional[RedisCache]:
    """
    Redis 캐시 싱글톤 인스턴스 반환

    Returns:
        RedisCache 인스턴스 (연결 실패 시 None)
    """
    global _redis_cache

    # Redis가 비활성화되어 있으면 None 반환
    if not USE_REDIS:
        return None

    # 이미 인스턴스가 있으면 반환
    if _redis_cache is not None:
        return _redis_cache

    # 새 인스턴스 생성
    try:
        _redis_cache = RedisCache(REDIS_URL)
        if not _redis_cache.is_connected():
            _redis_cache = None
    except Exception as e:
        logger = get_logger(__name__)
        logger.error("redis_cache_init_failed", error=str(e))
        _redis_cache = None

    return _redis_cache
