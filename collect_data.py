#!/usr/bin/env python3
"""
배치 데이터 수집 CLI 스크립트
법정동코드와 기간 범위를 지정하여 모든 API에서 데이터를 수집합니다.
"""
import sys
import argparse
from pathlib import Path

# 프로젝트 루트를 path에 추가
sys.path.insert(0, str(Path(__file__).parent))

from batch_collector import BatchCollector


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description='법정동코드와 기간 범위를 지정하여 아파트 실거래가 데이터를 수집합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  # 강남구 2023년 전체 데이터 수집 (모든 API)
  python collect_data.py 11680 202301 202312
  
  # 강남구 2023년 1분기 데이터 수집 (특정 API만)
  python collect_data.py 11680 202301 202303 --api api_01 api_02
  
  # 사용자 지정 출력 디렉토리
  python collect_data.py 11680 202301 202312 --output-dir ./custom_output

법정동코드 예시:
  - 서울특별시 종로구: 11110
  - 서울특별시 강남구: 11680
  - 서울특별시 서초구: 11650
  - 서울특별시 송파구: 11710
  - 경기도 수원시 영통구: 41117
        """
    )
    
    parser.add_argument(
        'lawd_cd',
        type=str,
        help='법정동코드 (5자리 숫자)'
    )
    
    parser.add_argument(
        'start_ym',
        type=str,
        help='시작년월 (YYYYMM 형식, 예: 202301)'
    )
    
    parser.add_argument(
        'end_ym',
        type=str,
        help='종료년월 (YYYYMM 형식, 예: 202312)'
    )
    
    parser.add_argument(
        '--api',
        nargs='+',
        choices=['api_01', 'api_02', 'api_03', 'api_04'],
        help='수집할 API 타입 선택 (선택하지 않으면 모든 API 수집)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        help='출력 디렉토리 경로 (선택하지 않으면 각 API의 기본 output 디렉토리 사용)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=0.5,
        help='API 호출 간 딜레이 시간(초) (기본값: 0.5)'
    )
    
    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='API 호출 실패 시 최대 재시도 횟수 (기본값: 3)'
    )
    
    args = parser.parse_args()
    
    try:
        # BatchCollector 인스턴스 생성
        collector = BatchCollector(delay_seconds=args.delay)
        
        # 출력 디렉토리 설정
        output_dir = None
        if args.output_dir:
            output_dir = Path(args.output_dir)
        
        # 데이터 수집 실행
        result = collector.collect_data(
            lawd_cd=args.lawd_cd,
            start_ym=args.start_ym,
            end_ym=args.end_ym,
            api_types=args.api,
            max_retries=args.max_retries
        )
        
        # 결과 저장
        print(f"\n{'='*60}")
        print(f"결과 저장 중...")
        print(f"{'='*60}")
        
        saved_files = []
        
        # 각 API별로 결과 저장
        for api_type in result['api_results'].keys():
            if output_dir:
                # 사용자 지정 디렉토리에 API별 하위 디렉토리 생성
                api_output_dir = output_dir / api_type
            else:
                api_output_dir = None  # 기본 디렉토리 사용
            
            filepath = collector.save_results(
                collection_result=result,
                api_type=api_type,
                custom_output_dir=api_output_dir
            )
            saved_files.append(filepath)
            print(f"  [{api_type}] 저장 완료: {filepath}")
        
        # 최종 요약
        print(f"\n{'='*60}")
        print(f"모든 작업 완료")
        print(f"{'='*60}")
        print(f"저장된 파일:")
        for filepath in saved_files:
            print(f"  - {filepath}")
        print(f"\n수집 요약:")
        print(f"  - 전체 성공: {result['summary']['total_successful']}건")
        print(f"  - 전체 실패: {result['summary']['total_failed']}건")
        print(f"  - 전체 데이터: {result['summary']['total_items']}건")
        
    except ValueError as e:
        print(f"❌ 오류: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n⚠️ 사용자에 의해 중단되었습니다.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"❌ 예상치 못한 오류 발생: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
