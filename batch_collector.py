"""
배치 데이터 수집 모듈
법정동코드와 기간 범위를 지정하여 모든 API에서 데이터를 수집합니다.

Dual-Mode Support:
- Sync Mode (기본값): 순차적 수집 (기존 방식)
- Async Mode (use_async=True): 병렬 수집 (5-10x 빠름)
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
import json
import time
import os
import asyncio

# 프로젝트 루트를 path에 추가
sys.path.insert(0, str(Path(__file__).parent))

# Sync APIs
from api_01.api_01_silv_trade import SilvTradeAPI
from api_02.api_02_apt_trade import AptTradeAPI
from api_03.api_03_apt_trade_dev import AptTradeDevAPI
from api_04.api_04_apt_rent import AptRentAPI

# Async APIs (if available)
try:
    import aiohttp
    from api_01.async_silv_trade import AsyncSilvTradeAPI
    from api_02.async_apt_trade import AsyncAptTradeAPI
    from api_03.async_apt_trade_dev import AsyncAptTradeDevAPI
    from api_04.async_apt_rent import AsyncAptRentAPI
    ASYNC_AVAILABLE = True
except ImportError:
    ASYNC_AVAILABLE = False
    print("⚠️  비동기 모듈 로드 실패. 동기 모드만 사용 가능합니다.")

from backend.data_loader import remove_duplicates


class BatchCollector:
    """
    배치 데이터 수집 클래스

    Dual-Mode:
    - collect_data(): 동기 수집 (순차적)
    - collect_data_async(): 비동기 수집 (병렬, 5-10x 빠름)
    """

    # Sync API 매핑
    API_MAP = {
        'api_01': {
            'name': '분양권전매 실거래가',
            'class': SilvTradeAPI,
            'output_dir': Path(__file__).parent / 'api_01' / 'output'
        },
        'api_02': {
            'name': '매매 실거래가',
            'class': AptTradeAPI,
            'output_dir': Path(__file__).parent / 'api_02' / 'output'
        },
        'api_03': {
            'name': '매매 실거래가 상세',
            'class': AptTradeDevAPI,
            'output_dir': Path(__file__).parent / 'api_03' / 'output'
        },
        'api_04': {
            'name': '전월세 실거래가',
            'class': AptRentAPI,
            'output_dir': Path(__file__).parent / 'api_04' / 'output'
        }
    }

    # Async API 매핑 (ASYNC_AVAILABLE이 True일 때만)
    ASYNC_API_MAP = {
        'api_01': {
            'name': '분양권전매 실거래가',
            'class': AsyncSilvTradeAPI if ASYNC_AVAILABLE else None,
            'output_dir': Path(__file__).parent / 'api_01' / 'output'
        },
        'api_02': {
            'name': '매매 실거래가',
            'class': AsyncAptTradeAPI if ASYNC_AVAILABLE else None,
            'output_dir': Path(__file__).parent / 'api_02' / 'output'
        },
        'api_03': {
            'name': '매매 실거래가 상세',
            'class': AsyncAptTradeDevAPI if ASYNC_AVAILABLE else None,
            'output_dir': Path(__file__).parent / 'api_03' / 'output'
        },
        'api_04': {
            'name': '전월세 실거래가',
            'class': AsyncAptRentAPI if ASYNC_AVAILABLE else None,
            'output_dir': Path(__file__).parent / 'api_04' / 'output'
        }
    } if ASYNC_AVAILABLE else {}
    
    def __init__(self, delay_seconds: float = 0.5):
        """
        Args:
            delay_seconds: API 호출 간 딜레이 시간 (초)
        """
        self.delay_seconds = delay_seconds
        self.apis = {}
        
        # 모든 API 인스턴스 초기화
        for api_key, api_info in self.API_MAP.items():
            self.apis[api_key] = api_info['class']()
            # output 디렉토리 생성
            api_info['output_dir'].mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def generate_date_range(start_ym: str, end_ym: str) -> List[str]:
        """
        시작년월부터 종료년월까지의 모든 월 리스트 생성
        
        Args:
            start_ym: 시작년월 (YYYYMM 형식, 예: '202301')
            end_ym: 종료년월 (YYYYMM 형식, 예: '202312')
        
        Returns:
            YYYYMM 형식의 월 리스트
        
        Raises:
            ValueError: 날짜 형식이 잘못되었거나 시작년월이 종료년월보다 큰 경우
        """
        # 날짜 형식 검증
        try:
            start_date = datetime.strptime(start_ym, '%Y%m')
            end_date = datetime.strptime(end_ym, '%Y%m')
        except ValueError:
            raise ValueError(f"날짜 형식이 잘못되었습니다. YYYYMM 형식이어야 합니다. (예: 202301)")
        
        # 시작년월이 종료년월보다 큰지 확인
        if start_date > end_date:
            raise ValueError(f"시작년월({start_ym})이 종료년월({end_ym})보다 큽니다.")
        
        # 월 리스트 생성
        date_range = []
        current_date = start_date
        
        while current_date <= end_date:
            date_range.append(current_date.strftime('%Y%m'))
            # 다음 달로 이동
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        return date_range
    
    def collect_data(
        self,
        lawd_cd: str,
        start_ym: str,
        end_ym: str,
        api_types: Optional[List[str]] = None,
        max_retries: int = 3,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        배치 데이터 수집 실행
        
        Args:
            lawd_cd: 법정동코드 (5자리)
            start_ym: 시작년월 (YYYYMM 형식)
            end_ym: 종료년월 (YYYYMM 형식)
            api_types: 수집할 API 타입 리스트 (None이면 모든 API)
            max_retries: 최대 재시도 횟수
            progress_callback: 진행 상황 콜백 함수 (선택사항)
        
        Returns:
            수집 결과 요약 딕셔너리
        """
        # 법정동코드 검증
        if not lawd_cd or len(lawd_cd) != 5 or not lawd_cd.isdigit():
            raise ValueError(f"법정동코드는 5자리 숫자여야 합니다. (입력값: {lawd_cd})")
        
        # 기간 범위 생성
        date_range = self.generate_date_range(start_ym, end_ym)
        
        # API 타입 설정
        if api_types is None:
            api_types = list(self.API_MAP.keys())
        else:
            # 유효한 API 타입인지 확인
            invalid_types = [t for t in api_types if t not in self.API_MAP]
            if invalid_types:
                raise ValueError(f"유효하지 않은 API 타입: {invalid_types}")
        
        print(f"\n{'='*60}")
        print(f"배치 데이터 수집 시작")
        print(f"{'='*60}")
        print(f"법정동코드: {lawd_cd}")
        print(f"기간: {start_ym} ~ {end_ym} ({len(date_range)}개월)")
        print(f"API 타입: {', '.join([self.API_MAP[t]['name'] for t in api_types])}")
        print(f"{'='*60}\n")
        
        # 전체 수집 결과
        all_results = {}
        
        # 전체 작업 수 계산 (진행률 계산용)
        total_tasks = len(api_types) * len(date_range)
        completed_tasks = 0
        
        # 각 API 타입별로 수집
        for api_idx, api_type in enumerate(api_types, 1):
            api_info = self.API_MAP[api_type]
            api_instance = self.apis[api_type]
            
            print(f"\n[{api_info['name']}] 수집 시작...")
            print("-" * 60)
            
            # API 시작 콜백
            if progress_callback:
                progress_callback(
                    current_api=api_type,
                    api_index=api_idx,
                    total_apis=len(api_types),
                    current_month='',
                    month_index=0,
                    total_months=len(date_range),
                    overall_progress=completed_tasks / total_tasks if total_tasks > 0 else 0.0,
                    status_message=f"{api_info['name']} 수집 시작..."
                )
            
            api_results = []
            successful_count = 0
            failed_count = 0
            total_items = 0
            
            # 각 월별로 데이터 수집
            for month_idx, deal_ymd in enumerate(date_range, 1):
                # 월 시작 콜백
                if progress_callback:
                    progress_callback(
                        current_api=api_type,
                        api_index=api_idx,
                        total_apis=len(api_types),
                        current_month=deal_ymd,
                        month_index=month_idx,
                        total_months=len(date_range),
                        overall_progress=completed_tasks / total_tasks if total_tasks > 0 else 0.0,
                        status_message=f"{api_info['name']} - {deal_ymd} 수집 중..."
                    )
                
                print(f"  [{month_idx}/{len(date_range)}] {deal_ymd} 수집 중...", end=' ', flush=True)
                
                # API 호출 (재시도 로직 포함)
                result = None
                for attempt in range(max_retries):
                    try:
                        result = api_instance.get_trade_data_parsed(
                            lawd_cd=lawd_cd,
                            deal_ymd=deal_ymd,
                            num_of_rows=1000,  # 최대값으로 설정
                            page_no=1
                        )
                        
                        # 페이지네이션 처리
                        if not result.get('error') and result.get('total_count', 0) > result.get('num_of_rows', 0):
                            # 전체 데이터 수집을 위해 여러 페이지 처리
                            all_items = result.get('items', [])
                            total_count = result.get('total_count', 0)
                            num_of_rows = result.get('num_of_rows', 0)
                            
                            page_no = 2
                            while len(all_items) < total_count:
                                time.sleep(self.delay_seconds)
                                page_result = api_instance.get_trade_data_parsed(
                                    lawd_cd=lawd_cd,
                                    deal_ymd=deal_ymd,
                                    num_of_rows=1000,
                                    page_no=page_no
                                )
                                
                                if page_result.get('error'):
                                    break
                                
                                page_items = page_result.get('items', [])
                                if not page_items:
                                    break
                                
                                all_items.extend(page_items)
                                
                                if len(page_items) < num_of_rows:
                                    break
                                
                                page_no += 1
                            
                            # 전체 아이템으로 업데이트
                            result['items'] = all_items
                            result['item_count'] = len(all_items)
                        
                        break  # 성공하면 재시도 루프 종료
                        
                    except Exception as e:
                        if attempt < max_retries - 1:
                            time.sleep(self.delay_seconds * (attempt + 1))  # 점진적 딜레이
                            continue
                        else:
                            result = {
                                'error': True,
                                'message': f'API 호출 실패: {str(e)}'
                            }
                
                # 결과 저장
                test_result = {
                    'test_name': f'{api_info["name"]} - {lawd_cd} {deal_ymd}',
                    'description': f'{api_info["name"]} 데이터 수집',
                    'lawd_cd': lawd_cd,
                    'deal_ymd': deal_ymd,
                    'start_time': datetime.now().isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'duration_seconds': 0,
                    'success': not result.get('error', False),
                    'result': result
                }
                
                api_results.append(test_result)
                
                # 작업 완료 카운트 증가
                completed_tasks += 1
                
                # 결과 출력
                if result.get('error'):
                    failed_count += 1
                    error_msg = result.get('message') or result.get('result_msg', 'Unknown error')
                    print(f"❌ 실패: {error_msg}")
                    
                    # 실패 콜백
                    if progress_callback:
                        progress_callback(
                            current_api=api_type,
                            api_index=api_idx,
                            total_apis=len(api_types),
                            current_month=deal_ymd,
                            month_index=month_idx,
                            total_months=len(date_range),
                            overall_progress=completed_tasks / total_tasks if total_tasks > 0 else 0.0,
                            status_message=f"{api_info['name']} - {deal_ymd} 실패: {error_msg}"
                        )
                else:
                    successful_count += 1
                    item_count = result.get('item_count', 0)
                    total_items += item_count
                    print(f"✅ 성공: {item_count}건")
                    
                    # 성공 콜백
                    if progress_callback:
                        progress_callback(
                            current_api=api_type,
                            api_index=api_idx,
                            total_apis=len(api_types),
                            current_month=deal_ymd,
                            month_index=month_idx,
                            total_months=len(date_range),
                            overall_progress=completed_tasks / total_tasks if total_tasks > 0 else 0.0,
                            status_message=f"{api_info['name']} - {deal_ymd} 완료: {item_count}건"
                        )
                
                # API 호출 간 딜레이
                if month_idx < len(date_range):
                    time.sleep(self.delay_seconds)
            
            # API별 결과 저장
            all_results[api_type] = {
                'api_name': api_info['name'],
                'results': api_results,
                'successful_count': successful_count,
                'failed_count': failed_count,
                'total_items': total_items
            }
            
            # API 완료 콜백
            if progress_callback:
                progress_callback(
                    current_api=api_type,
                    api_index=api_idx,
                    total_apis=len(api_types),
                    current_month='',
                    month_index=len(date_range),
                    total_months=len(date_range),
                    overall_progress=completed_tasks / total_tasks if total_tasks > 0 else 0.0,
                    status_message=f"{api_info['name']} 수집 완료: 성공 {successful_count}건, 실패 {failed_count}건"
                )
            
            print(f"\n[{api_info['name']}] 수집 완료:")
            print(f"  - 성공: {successful_count}건")
            print(f"  - 실패: {failed_count}건")
            print(f"  - 총 데이터: {total_items}건")
        
        # 전체 요약
        print(f"\n{'='*60}")
        print(f"전체 수집 완료")
        print(f"{'='*60}")
        total_successful = sum(r['successful_count'] for r in all_results.values())
        total_failed = sum(r['failed_count'] for r in all_results.values())
        total_all_items = sum(r['total_items'] for r in all_results.values())
        print(f"전체 성공: {total_successful}건")
        print(f"전체 실패: {total_failed}건")
        print(f"전체 데이터: {total_all_items}건")
        
        return {
            'lawd_cd': lawd_cd,
            'start_ym': start_ym,
            'end_ym': end_ym,
            'date_range': date_range,
            'api_results': all_results,
            'summary': {
                'total_successful': total_successful,
                'total_failed': total_failed,
                'total_items': total_all_items
            }
        }

    async def collect_data_async(
        self,
        lawd_cd: str,
        start_ym: str,
        end_ym: str,
        api_types: Optional[List[str]] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        비동기 배치 데이터 수집 (5-10x 빠름)

        Args:
            lawd_cd: 법정동코드 (5자리)
            start_ym: 시작년월 (YYYYMM 형식)
            end_ym: 종료년월 (YYYYMM 형식)
            api_types: 수집할 API 타입 리스트 (None이면 모든 API)
            progress_callback: 진행 상황 콜백 함수 (선택사항)

        Returns:
            수집 결과 요약 딕셔너리

        Example:
            >>> collector = BatchCollector()
            >>> result = await collector.collect_data_async(
            ...     lawd_cd='11680',
            ...     start_ym='202301',
            ...     end_ym='202312'
            ... )
            >>> # 12개월 데이터를 병렬로 수집 (40초 → 4초)
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError(
                "비동기 모듈이 로드되지 않았습니다. "
                "aiohttp를 설치하세요: pip install aiohttp aiodns"
            )

        # 법정동코드 검증
        if not lawd_cd or len(lawd_cd) != 5 or not lawd_cd.isdigit():
            raise ValueError(f"법정동코드는 5자리 숫자여야 합니다. (입력값: {lawd_cd})")

        # 기간 범위 생성
        date_range = self.generate_date_range(start_ym, end_ym)

        # API 타입 설정
        if api_types is None:
            api_types = list(self.ASYNC_API_MAP.keys())
        else:
            invalid_types = [t for t in api_types if t not in self.ASYNC_API_MAP]
            if invalid_types:
                raise ValueError(f"유효하지 않은 API 타입: {invalid_types}")

        print(f"\n{'='*60}")
        print(f"⚡ 비동기 배치 데이터 수집 시작")
        print(f"{'='*60}")
        print(f"법정동코드: {lawd_cd}")
        print(f"기간: {start_ym} ~ {end_ym} ({len(date_range)}개월)")
        print(f"API 타입: {', '.join([self.ASYNC_API_MAP[t]['name'] for t in api_types])}")
        print(f"병렬 처리: {len(date_range)}개월 × {len(api_types)}개 API = {len(date_range) * len(api_types)}개 동시 요청")
        print(f"{'='*60}\n")

        overall_start_time = time.time()
        all_results = {}

        # 각 API 타입별로 수집
        for api_idx, api_type in enumerate(api_types, 1):
            api_info = self.ASYNC_API_MAP[api_type]
            api_class = api_info['class']

            print(f"\n[{api_info['name']}] 비동기 수집 시작...")
            print("-" * 60)

            api_start_time = time.time()

            try:
                # API 인스턴스 생성
                api_instance = api_class()

                # aiohttp 세션 생성
                async with aiohttp.ClientSession() as session:
                    # 모든 월의 데이터를 병렬로 요청
                    tasks = [
                        api_instance.get_all_pages_async(
                            session=session,
                            lawd_cd=lawd_cd,
                            deal_ymd=deal_ymd,
                            num_of_rows=1000
                        )
                        for deal_ymd in date_range
                    ]

                    print(f"  {len(tasks)}개 요청 병렬 실행 중...")

                    # asyncio.gather로 병렬 실행
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                api_elapsed = time.time() - api_start_time

                # 결과 처리
                api_results = []
                successful_count = 0
                failed_count = 0
                total_items = 0

                for idx, (deal_ymd, result) in enumerate(zip(date_range, results)):
                    if isinstance(result, Exception):
                        # 예외 발생
                        failed_count += 1
                        test_result = {
                            'test_name': f'{api_info["name"]} - {lawd_cd} {deal_ymd}',
                            'description': f'{api_info["name"]} 데이터 수집',
                            'lawd_cd': lawd_cd,
                            'deal_ymd': deal_ymd,
                            'start_time': datetime.now().isoformat(),
                            'end_time': datetime.now().isoformat(),
                            'duration_seconds': 0,
                            'success': False,
                            'result': {
                                'error': True,
                                'message': f'API 호출 실패: {str(result)}'
                            }
                        }
                        print(f"  [{idx+1}/{len(date_range)}] {deal_ymd} ❌ 실패: {str(result)}")

                    elif result.get('error'):
                        # API 에러 응답
                        failed_count += 1
                        test_result = {
                            'test_name': f'{api_info["name"]} - {lawd_cd} {deal_ymd}',
                            'description': f'{api_info["name"]} 데이터 수집',
                            'lawd_cd': lawd_cd,
                            'deal_ymd': deal_ymd,
                            'start_time': datetime.now().isoformat(),
                            'end_time': datetime.now().isoformat(),
                            'duration_seconds': 0,
                            'success': False,
                            'result': result
                        }
                        error_msg = result.get('message', 'Unknown error')
                        print(f"  [{idx+1}/{len(date_range)}] {deal_ymd} ❌ 실패: {error_msg}")

                    else:
                        # 성공
                        successful_count += 1
                        item_count = len(result.get('items', []))
                        total_items += item_count

                        test_result = {
                            'test_name': f'{api_info["name"]} - {lawd_cd} {deal_ymd}',
                            'description': f'{api_info["name"]} 데이터 수집',
                            'lawd_cd': lawd_cd,
                            'deal_ymd': deal_ymd,
                            'start_time': datetime.now().isoformat(),
                            'end_time': datetime.now().isoformat(),
                            'duration_seconds': 0,
                            'success': True,
                            'result': result
                        }
                        print(f"  [{idx+1}/{len(date_range)}] {deal_ymd} ✅ 성공: {item_count}건")

                    api_results.append(test_result)

                # API별 결과 저장
                all_results[api_type] = {
                    'api_name': api_info['name'],
                    'results': api_results,
                    'successful_count': successful_count,
                    'failed_count': failed_count,
                    'total_items': total_items
                }

                print(f"\n[{api_info['name']}] 수집 완료:")
                print(f"  - 성공: {successful_count}건")
                print(f"  - 실패: {failed_count}건")
                print(f"  - 총 데이터: {total_items}건")
                print(f"  - 소요 시간: {api_elapsed:.2f}초")
                print(f"  - 평균 처리 시간: {api_elapsed / len(date_range):.2f}초/월")

            except Exception as e:
                print(f"\n❌ [{api_info['name']}] 수집 실패: {str(e)}")
                import traceback
                traceback.print_exc()

                # 실패한 API 결과 저장
                all_results[api_type] = {
                    'api_name': api_info['name'],
                    'results': [],
                    'successful_count': 0,
                    'failed_count': len(date_range),
                    'total_items': 0,
                    'error': str(e)
                }

        overall_elapsed = time.time() - overall_start_time

        # 전체 요약
        print(f"\n{'='*60}")
        print(f"⚡ 전체 비동기 수집 완료")
        print(f"{'='*60}")
        total_successful = sum(r['successful_count'] for r in all_results.values())
        total_failed = sum(r['failed_count'] for r in all_results.values())
        total_all_items = sum(r['total_items'] for r in all_results.values())
        print(f"전체 성공: {total_successful}건")
        print(f"전체 실패: {total_failed}건")
        print(f"전체 데이터: {total_all_items}건")
        print(f"총 소요 시간: {overall_elapsed:.2f}초")
        print(f"추정 동기 방식 시간: ~{len(date_range) * len(api_types) * 3:.0f}초")
        print(f"⚡ 성능 향상: ~{(len(date_range) * len(api_types) * 3 / overall_elapsed):.1f}x 빠름")

        return {
            'lawd_cd': lawd_cd,
            'start_ym': start_ym,
            'end_ym': end_ym,
            'date_range': date_range,
            'api_results': all_results,
            'summary': {
                'total_successful': total_successful,
                'total_failed': total_failed,
                'total_items': total_all_items,
                'total_duration': overall_elapsed,
                'async_mode': True
            }
        }

    def save_results(
        self,
        collection_result: Dict,
        api_type: str,
        custom_output_dir: Optional[Path] = None
    ) -> Path:
        """
        수집 결과를 기존 JSON 형식으로 저장
        
        Args:
            collection_result: collect_data()의 반환값
            api_type: API 타입 (api_01, api_02, api_03, api_04)
            custom_output_dir: 사용자 지정 출력 디렉토리 (None이면 기본 디렉토리 사용)
        
        Returns:
            저장된 JSON 파일 경로
        """
        if api_type not in self.API_MAP:
            raise ValueError(f"유효하지 않은 API 타입: {api_type}")
        
        # 출력 디렉토리 결정
        if custom_output_dir:
            output_dir = Path(custom_output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = self.API_MAP[api_type]['output_dir']
        
        # API별 결과 가져오기
        api_result = collection_result['api_results'][api_type]
        api_results = api_result['results']
        
        # 모든 items 수집 및 중복 제거
        all_items = []
        for test_result in api_results:
            result = test_result.get('result', {})
            if not result.get('error', False):
                items = result.get('items', [])
                if items:
                    all_items.extend(items)
        
        # 중복 제거 전 건수
        before_count = len(all_items)
        
        # 중복 제거 수행 (통계용)
        if all_items:
            deduplicated_items = remove_duplicates(all_items)
            after_count = len(deduplicated_items)
            removed_count = before_count - after_count
            
            if removed_count > 0:
                print(f"  중복 제거: {before_count:,}건 → {after_count:,}건 ({removed_count:,}건 제거)")
        else:
            after_count = 0
            removed_count = 0
            deduplicated_items = []
        
        # 각 test_result의 items는 원본 유지 (월별 데이터 무결성 보장)
        # 중복 제거는 전체 통계에만 반영
        
        # 통계 계산 (중복 제거 후)
        total_tests = len(api_results)
        successful_tests = api_result['successful_count']
        failed_tests = api_result['failed_count']
        total_duration = sum(r.get('duration_seconds', 0) for r in api_results)
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        # JSON 데이터 구성 (기존 test_runner.py 형식 유지)
        json_data = {
            'test_summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': failed_tests,
                'success_rate': successful_tests / total_tests * 100 if total_tests > 0 else 0,
                'total_duration': total_duration,
                'avg_duration': avg_duration,
                'lawd_cd': collection_result['lawd_cd'],
                'start_ym': collection_result['start_ym'],
                'end_ym': collection_result['end_ym'],
                'date_range': collection_result['date_range'],
                'deduplication': {
                    'before_count': before_count,
                    'after_count': after_count,
                    'removed_count': removed_count
                } if removed_count > 0 else None
            },
            'test_results': api_results
        }
        
        # 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        lawd_cd = collection_result['lawd_cd']
        filename = f"test_results_{lawd_cd}_{timestamp}.json"
        filepath = output_dir / filename
        
        # JSON 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        return filepath
