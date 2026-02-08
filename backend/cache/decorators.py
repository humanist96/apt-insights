"""
캐시 데코레이터
API 응답 자동 캐싱
"""
import functools
from typing import Callable, Any
from logger import get_logger
from .redis_client import get_redis_cache

logger = get_logger(__name__)


def cache_api_response(api_type_field: str = '_api_type'):
    """
    API 응답을 Redis에 캐싱하는 데코레이터

    Args:
        api_type_field: API 타입을 나타내는 필드명

    Usage:
        @cache_api_response(api_type_field='api_02')
        async def get_trade_data_parsed_async(self, session, lawd_cd, deal_ymd, **kwargs):
            ...

    Cache Key Format:
        apt_insights:{api_type}:{lawd_cd}:{deal_ymd}

    TTL Strategy:
        - Current month: 1 hour
        - Recent 3 months: 6 hours
        - Historical: 7 days
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            """비동기 함수용 래퍼"""
            cache = get_redis_cache()

            # Redis가 비활성화되어 있으면 캐싱 없이 실행
            if not cache or not cache.is_connected():
                logger.debug("cache_disabled_or_disconnected", func=func.__name__)
                return await func(*args, **kwargs)

            # 캐시 키 생성에 필요한 파라미터 추출
            # 일반적으로 (self, session, lawd_cd, deal_ymd, ...) 형태
            try:
                # args에서 추출
                if len(args) >= 4:
                    self = args[0]
                    lawd_cd = args[2]
                    deal_ymd = args[3]
                # kwargs에서 추출
                else:
                    lawd_cd = kwargs.get('lawd_cd')
                    deal_ymd = kwargs.get('deal_ymd')
                    self = args[0] if args else None

                # API 타입 결정
                if hasattr(self, 'BASE_URL'):
                    # BaseURL에서 API 타입 추출
                    if 'SilvTrade' in self.BASE_URL:
                        api_type = 'api_01'
                    elif 'AptTradeDev' in self.BASE_URL:
                        api_type = 'api_03'
                    elif 'AptTrade' in self.BASE_URL:
                        api_type = 'api_02'
                    elif 'AptRent' in self.BASE_URL:
                        api_type = 'api_04'
                    else:
                        api_type = 'unknown'
                else:
                    api_type = 'unknown'

            except (IndexError, KeyError) as e:
                logger.warning("cache_key_extraction_failed", error=str(e))
                # 캐시 키 생성 실패 시 캐싱 없이 실행
                return await func(*args, **kwargs)

            # 캐시 조회
            cached_data = cache.get(api_type, lawd_cd, deal_ymd)
            if cached_data is not None:
                logger.debug(
                    "cache_hit_decorator",
                    func=func.__name__,
                    api_type=api_type,
                    lawd_cd=lawd_cd,
                    deal_ymd=deal_ymd
                )
                return cached_data

            # 캐시 미스 - 함수 실행
            logger.debug(
                "cache_miss_decorator",
                func=func.__name__,
                api_type=api_type,
                lawd_cd=lawd_cd,
                deal_ymd=deal_ymd
            )
            result = await func(*args, **kwargs)

            # 결과를 캐시에 저장 (에러가 아닌 경우에만)
            if result and not result.get('error'):
                cache.set(api_type, lawd_cd, deal_ymd, result)
                logger.debug(
                    "cache_set_decorator",
                    func=func.__name__,
                    api_type=api_type,
                    lawd_cd=lawd_cd,
                    deal_ymd=deal_ymd
                )

            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            """동기 함수용 래퍼"""
            cache = get_redis_cache()

            # Redis가 비활성화되어 있으면 캐싱 없이 실행
            if not cache or not cache.is_connected():
                return func(*args, **kwargs)

            # 캐시 키 생성 (동일 로직)
            try:
                if len(args) >= 3:
                    self = args[0]
                    lawd_cd = args[1]
                    deal_ymd = args[2]
                else:
                    lawd_cd = kwargs.get('lawd_cd')
                    deal_ymd = kwargs.get('deal_ymd')
                    self = args[0] if args else None

                # API 타입 결정
                if hasattr(self, 'BASE_URL'):
                    if 'SilvTrade' in self.BASE_URL:
                        api_type = 'api_01'
                    elif 'AptTradeDev' in self.BASE_URL:
                        api_type = 'api_03'
                    elif 'AptTrade' in self.BASE_URL:
                        api_type = 'api_02'
                    elif 'AptRent' in self.BASE_URL:
                        api_type = 'api_04'
                    else:
                        api_type = 'unknown'
                else:
                    api_type = 'unknown'

            except (IndexError, KeyError):
                return func(*args, **kwargs)

            # 캐시 조회
            cached_data = cache.get(api_type, lawd_cd, deal_ymd)
            if cached_data is not None:
                logger.debug("cache_hit_sync", api_type=api_type, lawd_cd=lawd_cd, deal_ymd=deal_ymd)
                return cached_data

            # 캐시 미스 - 함수 실행
            result = func(*args, **kwargs)

            # 결과 캐싱
            if result and not result.get('error'):
                cache.set(api_type, lawd_cd, deal_ymd, result)

            return result

        # 함수가 코루틴이면 async_wrapper, 아니면 sync_wrapper
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def invalidate_cache(api_type: str, lawd_cd: str, deal_ymd: str):
    """
    특정 캐시 무효화

    Args:
        api_type: API 타입
        lawd_cd: 지역코드
        deal_ymd: 계약년월

    Usage:
        invalidate_cache('api_02', '11680', '202312')
    """
    cache = get_redis_cache()
    if cache:
        cache.delete(api_type, lawd_cd, deal_ymd)
        logger.info("cache_invalidated", api_type=api_type, lawd_cd=lawd_cd, deal_ymd=deal_ymd)
