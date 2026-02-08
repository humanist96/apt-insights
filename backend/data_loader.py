"""
데이터 로더 모듈
output 디렉토리의 JSON 파일을 로드하거나 PostgreSQL에서 데이터를 가져옵니다.
USE_DATABASE 환경변수로 모드 전환 (True: DB, False: JSON)
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import re
import traceback
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 데이터베이스 사용 여부 (기본값: False, JSON 모드)
USE_DATABASE = os.getenv('USE_DATABASE', 'False').lower() == 'true'

# 데이터베이스 모드일 때만 import
if USE_DATABASE:
    try:
        from .db.repository import TransactionRepository
        from .db.session import get_session
        DATABASE_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️  데이터베이스 모듈 로드 실패: {e}")
        print("   JSON 모드로 폴백합니다.")
        DATABASE_AVAILABLE = False
        USE_DATABASE = False
else:
    DATABASE_AVAILABLE = False


def _get_field_value(item: Dict, *keys: str) -> str:
    for key in keys:
        value = item.get(key, '')
        if value:
            return value
    return ''


def load_all_json_data(base_path: Optional[Path] = None, debug: bool = False) -> Tuple[List[Dict], Dict]:
    """
    데이터 로드 (Dual-Mode: JSON 또는 PostgreSQL)

    USE_DATABASE 환경변수에 따라 데이터 소스 결정:
    - True: PostgreSQL에서 로드
    - False (기본값): JSON 파일에서 로드

    주의: 실제 JSON 파일에서만 데이터를 로드합니다. 목업 데이터를 사용하지 않습니다.

    Args:
        base_path: 프로젝트 루트 경로 (None이면 현재 파일 기준 상대 경로 사용)
        debug: 디버깅 정보 반환 여부

    Returns:
        (items 리스트, 디버깅 정보 딕셔너리)
        - items: 거래 데이터 리스트 (데이터가 없으면 빈 리스트)
        - debug_info: 디버깅 정보 (성공/실패 파일 목록, 오류 메시지 등)
    """
    # 데이터베이스 모드
    if USE_DATABASE and DATABASE_AVAILABLE:
        print("📊 데이터베이스 모드: PostgreSQL에서 데이터 로드")
        return _load_from_database()

    # JSON 모드 (기본값)
    print("📁 JSON 모드: 파일에서 데이터 로드")
    return _load_from_json(base_path, debug)


def _load_from_database() -> Tuple[List[Dict], Dict]:
    """
    PostgreSQL에서 데이터 로드

    Returns:
        (items 리스트, 디버깅 정보 딕셔너리)
    """
    try:
        with get_session() as session:
            repository = TransactionRepository(session)
            items, debug_info = repository.load_all_transactions()

            # 모드 표시
            debug_info['data_source'] = 'postgresql'
            debug_info['use_database'] = True

            return items, debug_info

    except Exception as e:
        print(f"⚠️  데이터베이스 로드 실패: {e}")
        print("   JSON 모드로 폴백합니다.")
        return _load_from_json(None, False)


def _load_from_json(base_path: Optional[Path] = None, debug: bool = False) -> Tuple[List[Dict], Dict]:
    """
    JSON 파일에서 데이터 로드 (기존 로직)

    Args:
        base_path: 프로젝트 루트 경로
        debug: 디버깅 정보 반환 여부

    Returns:
        (items 리스트, 디버깅 정보 딕셔너리)
    """
    if base_path is None:
        # 현재 파일 기준으로 프로젝트 루트 찾기
        current_file = Path(__file__)
        base_path = current_file.parent.parent
    
    all_items = []
    debug_info = {
        'successful_files': [],
        'failed_files': [],
        'total_files': 0,
        'total_items': 0,
        'errors': []
    }
    
    # 모든 api_XX/output 디렉토리에서 test_results JSON 파일 찾기
    json_files = []
    for api_dir in base_path.glob('api_*/output'):
        json_files.extend(list(api_dir.glob('*test_results*.json')))
    
    debug_info['total_files'] = len(json_files)
    
    for json_file in json_files:
        try:
            file_size_mb = json_file.stat().st_size / (1024 * 1024)
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_items_count = 0
            
            # test_results 배열에서 items 추출
            test_results = data.get('test_results', [])
            for test_result in test_results:
                result = test_result.get('result', {})
                if not result.get('error', False):
                    items = result.get('items', [])
                    if items:
                        # 각 item에 API 타입 정보 추가
                        api_type = json_file.parent.parent.name  # api_01, api_02 등
                        for item in items:
                            item['_api_type'] = api_type
                            item['_source_file'] = str(json_file)
                        all_items.extend(items)
                        file_items_count += len(items)
            
            debug_info['successful_files'].append({
                'file': str(json_file),
                'size_mb': round(file_size_mb, 2),
                'items_count': file_items_count
            })
            debug_info['total_items'] += file_items_count
            
        except json.JSONDecodeError as e:
            error_msg = f"JSON 파싱 오류: {str(e)}"
            debug_info['failed_files'].append({
                'file': str(json_file),
                'error': error_msg,
                'error_type': 'JSONDecodeError'
            })
            debug_info['errors'].append({
                'file': str(json_file),
                'error': error_msg,
                'traceback': traceback.format_exc() if debug else None
            })
            if debug:
                print(f"❌ JSON 파싱 오류 [{json_file.name}]: {e}")
            continue
        except MemoryError as e:
            error_msg = f"메모리 부족: {str(e)}"
            debug_info['failed_files'].append({
                'file': str(json_file),
                'error': error_msg,
                'error_type': 'MemoryError'
            })
            debug_info['errors'].append({
                'file': str(json_file),
                'error': error_msg,
                'traceback': traceback.format_exc() if debug else None
            })
            if debug:
                print(f"❌ 메모리 부족 [{json_file.name}]: {e}")
            continue
        except Exception as e:
            error_msg = f"예상치 못한 오류: {str(e)}"
            debug_info['failed_files'].append({
                'file': str(json_file),
                'error': error_msg,
                'error_type': type(e).__name__
            })
            debug_info['errors'].append({
                'file': str(json_file),
                'error': error_msg,
                'traceback': traceback.format_exc() if debug else None
            })
            if debug:
                print(f"❌ 오류 [{json_file.name}]: {e}")
            continue
    
    return all_items, debug_info


def remove_duplicates(items: List[Dict]) -> List[Dict]:
    """
    중복된 거래 데이터 제거
    
    중복 판단 기준:
    - aptSeq + dealYear + dealMonth + dealDay + dealAmount
    - 또는 aptNm + umdNm + dealYear + dealMonth + dealDay + dealAmount (aptSeq가 없는 경우)
    
    Args:
        items: 거래 데이터 리스트
    
    Returns:
        중복이 제거된 거래 데이터 리스트
    """
    seen = set()
    unique_items = []
    
    for item in items:
        # aptSeq가 있으면 우선 사용
        apt_seq = _get_field_value(item, 'aptSeq', 'apt')
        apt_nm = _get_field_value(item, 'aptNm', '아파트')
        umd_nm = _get_field_value(item, 'umdNm', '법정동', '법정동명')
        deal_year = _get_field_value(item, 'dealYear', '년')
        deal_month = _get_field_value(item, 'dealMonth', '월')
        deal_day = _get_field_value(item, 'dealDay', '일')
        deal_amount = _get_field_value(item, 'dealAmount', '거래금액')
        
        # 고유 키 생성
        if apt_seq:
            key = (
                str(apt_seq),
                str(deal_year),
                str(deal_month),
                str(deal_day),
                str(deal_amount)
            )
        else:
            # aptSeq가 없으면 aptNm + umdNm 조합 사용
            key = (
                str(apt_nm),
                str(umd_nm),
                str(deal_year),
                str(deal_month),
                str(deal_day),
                str(deal_amount)
            )
        
        if key not in seen:
            seen.add(key)
            unique_items.append(item)
    
    return unique_items


def normalize_data(items: List[Dict]) -> List[Dict]:
    """
    데이터 정규화
    
    - 거래금액: 문자열(쉼표 포함) → 숫자 (만원 단위)
    - 면적: 문자열 → float
    - 날짜: year, month, day → datetime 객체 및 YYYY-MM-DD 문자열
    - 지역명: sggNm, umdNm 조합
    
    Args:
        items: 원본 거래 데이터 리스트
    
    Returns:
        정규화된 거래 데이터 리스트
    """
    normalized = []
    
    for item in items:
        normalized_item = item.copy()
        
        # 거래금액 정규화 (만원 단위 숫자로 변환)
        deal_amount = _get_field_value(item, 'dealAmount', '거래금액')
        if deal_amount:
            try:
                # 쉼표 제거 후 숫자 변환
                amount_str = str(deal_amount).replace(',', '').strip()
                if amount_str:
                    normalized_item['_deal_amount_numeric'] = float(amount_str)
                else:
                    normalized_item['_deal_amount_numeric'] = None
            except (ValueError, AttributeError):
                normalized_item['_deal_amount_numeric'] = None
        else:
            normalized_item['_deal_amount_numeric'] = None
        
        # 면적 정규화
        area = _get_field_value(item, 'excluUseAr', '전용면적', '면적')
        if area:
            try:
                area_str = str(area).replace(',', '').strip()
                if area_str:
                    normalized_item['_area_numeric'] = float(area_str)
                else:
                    normalized_item['_area_numeric'] = None
            except (ValueError, AttributeError):
                normalized_item['_area_numeric'] = None
        else:
            normalized_item['_area_numeric'] = None
        
        # 날짜 정규화
        year = _get_field_value(item, 'dealYear', '년')
        month = _get_field_value(item, 'dealMonth', '월')
        day = _get_field_value(item, 'dealDay', '일')
        
        if year and month and day:
            try:
                year_int = int(str(year))
                month_int = int(str(month))
                day_int = int(str(day))
                
                # datetime 객체 생성
                deal_date = datetime(year_int, month_int, day_int)
                normalized_item['_deal_date'] = deal_date
                normalized_item['_deal_date_str'] = f"{year_int}-{month_int:02d}-{day_int:02d}"
                normalized_item['_deal_year_month'] = f"{year_int}-{month_int:02d}"
            except (ValueError, TypeError):
                normalized_item['_deal_date'] = None
                normalized_item['_deal_date_str'] = None
                normalized_item['_deal_year_month'] = None
        else:
            normalized_item['_deal_date'] = None
            normalized_item['_deal_date_str'] = None
            normalized_item['_deal_year_month'] = None
        
        # 지역명 정규화
        sgg_nm = _get_field_value(item, 'sggNm', '시군구')
        umd_nm = _get_field_value(item, 'umdNm', '법정동', '법정동명')
        
        if sgg_nm or umd_nm:
            normalized_item['_region_name'] = f"{sgg_nm} {umd_nm}".strip()
        else:
            normalized_item['_region_name'] = None
        
        # 층수 정규화
        floor = _get_field_value(item, 'floor', '층', '층수')
        if floor:
            try:
                # 층수 문자열에서 숫자만 추출
                floor_str = re.sub(r'[^0-9-]', '', str(floor))
                if floor_str:
                    normalized_item['_floor_numeric'] = int(floor_str)
                else:
                    normalized_item['_floor_numeric'] = None
            except (ValueError, TypeError):
                normalized_item['_floor_numeric'] = None
        else:
            normalized_item['_floor_numeric'] = None
        
        # 건축년도 정규화
        build_year = _get_field_value(item, 'buildYear', '건축년도', '건축연도')
        if build_year:
            try:
                normalized_item['_build_year_numeric'] = int(str(build_year))
            except (ValueError, TypeError):
                normalized_item['_build_year_numeric'] = None
        else:
            normalized_item['_build_year_numeric'] = None
        
        normalized.append(normalized_item)
    
    return normalized


def filter_by_region(items: List[Dict], region_name: Optional[str] = None) -> List[Dict]:
    """
    지역별로 데이터 필터링
    
    Args:
        items: 거래 데이터 리스트
        region_name: 지역명 (None이면 필터링 안 함)
    
    Returns:
        필터링된 거래 데이터 리스트
    """
    if not region_name:
        return items
    
    region_name_lower = region_name.lower()
    filtered = []
    
    for item in items:
        # _region_name이 있으면 사용, 없으면 원본 필드 확인
        region = item.get('_region_name', '')
        if not region:
            sgg_nm = item.get('sggNm', '') or item.get('시군구', '')
            umd_nm = item.get('umdNm', '') or item.get('법정동', '') or item.get('법정동명', '')
            region = f"{sgg_nm} {umd_nm}".strip()
        
        if region_name_lower in region.lower():
            filtered.append(item)
    
    return filtered


def load_and_process_data(
    base_path: Optional[Path] = None,
    region_filter: Optional[str] = None,
    remove_dup: bool = True,
    debug: bool = False
) -> Tuple[List[Dict], Optional[Dict]]:
    """
    JSON 데이터를 로드하고 중복 제거 및 정규화를 수행하는 통합 함수
    
    Args:
        base_path: 프로젝트 루트 경로
        region_filter: 지역 필터 (None이면 모든 지역)
        remove_dup: 중복 제거 여부
        debug: 디버깅 정보 반환 여부
    
    Returns:
        (처리된 거래 데이터 리스트, 디버깅 정보) 또는 (처리된 거래 데이터 리스트, None)
    """
    # 1. JSON 파일 로드
    items, debug_info = load_all_json_data(base_path, debug=debug)
    
    # 2. 중복 제거
    if remove_dup:
        before_count = len(items)
        items = remove_duplicates(items)
        after_count = len(items)
        if debug:
            debug_info['deduplication'] = {
                'before_count': before_count,
                'after_count': after_count,
                'removed_count': before_count - after_count
            }
    
    # 3. 지역 필터링
    if region_filter:
        before_count = len(items)
        items = filter_by_region(items, region_filter)
        after_count = len(items)
        if debug:
            debug_info['region_filtering'] = {
                'region': region_filter,
                'before_count': before_count,
                'after_count': after_count
            }
    
    # 4. 데이터 정규화
    items = normalize_data(items)
    
    if debug:
        return items, debug_info
    else:
        return items, None
