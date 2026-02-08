"""
Redis 캐시 관리 CLI

Usage:
    python -m backend.cache.cache_manager stats      # 통계 조회
    python -m backend.cache.cache_manager clear      # 전체 삭제
    python -m backend.cache.cache_manager reset      # 통계 초기화
    python -m backend.cache.cache_manager ping       # 연결 테스트
"""
import sys
import argparse
from pathlib import Path

# 프로젝트 루트를 path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.cache.redis_client import get_redis_cache, USE_REDIS


def print_stats():
    """캐시 통계 출력"""
    cache = get_redis_cache()

    if not cache:
        print("❌ Redis 캐시를 사용할 수 없습니다.")
        print(f"   USE_REDIS={USE_REDIS}")
        print("   .env 파일에서 USE_REDIS=true로 설정하세요.")
        return 1

    if not cache.is_connected():
        print("❌ Redis 서버에 연결할 수 없습니다.")
        print(f"   URL: {cache.url}")
        return 1

    stats = cache.get_stats()

    print("\n" + "="*60)
    print("📊 Redis 캐시 통계")
    print("="*60)

    print(f"\n✅ 연결 상태: {'연결됨' if stats['connected'] else '연결 끊김'}")

    print(f"\n📈 요청 통계:")
    print(f"  - 캐시 히트: {stats['hits']:,}건")
    print(f"  - 캐시 미스: {stats['misses']:,}건")
    print(f"  - 총 요청: {stats['total_requests']:,}건")
    print(f"  - 히트율: {stats['hit_rate_percent']:.2f}%")

    print(f"\n💾 저장 통계:")
    print(f"  - 캐시 설정: {stats['sets']:,}건")
    print(f"  - 에러: {stats['errors']:,}건")

    if 'total_keys' in stats:
        print(f"\n🗄️  Redis 서버:")
        print(f"  - 총 키 개수: {stats['total_keys']:,}개")
        print(f"  - 서버 히트: {stats.get('server_hits', 0):,}건")
        print(f"  - 서버 미스: {stats.get('server_misses', 0):,}건")

    print("\n" + "="*60)

    return 0


def clear_cache():
    """캐시 전체 삭제"""
    cache = get_redis_cache()

    if not cache:
        print("❌ Redis 캐시를 사용할 수 없습니다.")
        return 1

    if not cache.is_connected():
        print("❌ Redis 서버에 연결할 수 없습니다.")
        return 1

    # 확인 프롬프트
    print("\n⚠️  경고: 모든 캐시를 삭제합니다.")
    confirm = input("계속하시겠습니까? (yes/no): ").strip().lower()

    if confirm != 'yes':
        print("❌ 취소되었습니다.")
        return 0

    # 삭제 실행
    deleted = cache.clear_all(pattern='apt_insights:*')

    print(f"\n✅ 캐시 삭제 완료: {deleted:,}개 키 삭제됨")

    return 0


def reset_stats():
    """통계 초기화"""
    cache = get_redis_cache()

    if not cache:
        print("❌ Redis 캐시를 사용할 수 없습니다.")
        return 1

    cache.reset_stats()
    print("\n✅ 통계가 초기화되었습니다.")

    return 0


def ping():
    """Redis 연결 테스트"""
    cache = get_redis_cache()

    print("\n" + "="*60)
    print("🔌 Redis 연결 테스트")
    print("="*60)

    if not cache:
        print("\n❌ Redis 캐시를 사용할 수 없습니다.")
        print(f"   USE_REDIS={USE_REDIS}")
        print("\n해결 방법:")
        print("  1. .env 파일에서 USE_REDIS=true로 설정")
        print("  2. redis 모듈 설치: pip install redis hiredis")
        return 1

    print(f"\nRedis URL: {cache.url}")

    if cache.is_connected():
        print("\n✅ 연결 성공!")
        print(f"   Ping 응답: OK")

        # 간단한 테스트
        try:
            test_key = "apt_insights:test:ping"
            cache.client.set(test_key, "pong", ex=10)
            value = cache.client.get(test_key)
            cache.client.delete(test_key)

            if value == "pong":
                print(f"   읽기/쓰기 테스트: OK")
        except Exception as e:
            print(f"   읽기/쓰기 테스트: 실패 ({e})")

        print("\n" + "="*60)
        return 0
    else:
        print("\n❌ 연결 실패!")
        print("\n해결 방법:")
        print("  1. Redis 서버가 실행 중인지 확인:")
        print("     docker-compose ps")
        print("  2. Redis 시작:")
        print("     docker-compose up -d redis")
        print("  3. 로그 확인:")
        print("     docker-compose logs redis")
        print("\n" + "="*60)
        return 1


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='Redis 캐시 관리 CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 통계 조회
  python -m backend.cache.cache_manager stats

  # 전체 캐시 삭제
  python -m backend.cache.cache_manager clear

  # 통계 초기화
  python -m backend.cache.cache_manager reset

  # 연결 테스트
  python -m backend.cache.cache_manager ping
        """
    )

    parser.add_argument(
        'command',
        choices=['stats', 'clear', 'reset', 'ping'],
        help='실행할 명령'
    )

    args = parser.parse_args()

    # 명령 실행
    if args.command == 'stats':
        return print_stats()
    elif args.command == 'clear':
        return clear_cache()
    elif args.command == 'reset':
        return reset_stats()
    elif args.command == 'ping':
        return ping()
    else:
        print(f"❌ 알 수 없는 명령: {args.command}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
