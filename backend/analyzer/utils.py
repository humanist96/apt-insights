"""
분석 유틸리티 모듈
공통으로 사용되는 헬퍼 함수들
"""
from typing import List, Dict, Optional
from datetime import datetime


def categorize_floor(floor: int) -> str:
    """
    층수를 카테고리로 분류

    Args:
        floor: 층수

    Returns:
        층 카테고리 ('저층', '중층', '고층')
    """
    if floor <= 5:
        return '저층'
    elif floor <= 15:
        return '중층'
    else:
        return '고층'


def calculate_price_per_sqm(deal_amount: float, area: float) -> Optional[float]:
    """
    평당 가격 계산

    Args:
        deal_amount: 거래금액
        area: 면적 (제곱미터)

    Returns:
        평당 가격 (만원/평) 또는 None
    """
    if not area or area <= 0:
        return None

    # 제곱미터를 평으로 변환 (1평 = 3.3058제곱미터)
    pyeong = area / 3.3058

    if pyeong <= 0:
        return None

    # 만원 단위로 변환
    return (deal_amount / pyeong) / 10000


def get_field_value(item: Dict, *keys: str, default=None):
    """
    딕셔너리에서 여러 키를 시도하여 값 추출

    Args:
        item: 데이터 딕셔너리
        *keys: 시도할 키 목록
        default: 기본값

    Returns:
        찾은 값 또는 기본값
    """
    for key in keys:
        value = item.get(key)
        if value is not None and value != '':
            return value
    return default


def filter_by_api_type(items: List[Dict], api_type: str) -> List[Dict]:
    """
    API 타입으로 필터링

    Args:
        items: 거래 데이터 리스트
        api_type: API 타입 (api_01, api_02, api_03, api_04)

    Returns:
        필터링된 데이터 리스트
    """
    return [item for item in items if item.get('_api_type') == api_type]


def filter_by_date_range(
    items: List[Dict],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Dict]:
    """
    날짜 범위로 필터링

    Args:
        items: 거래 데이터 리스트
        start_date: 시작 날짜
        end_date: 종료 날짜

    Returns:
        필터링된 데이터 리스트
    """
    filtered = items

    if start_date:
        filtered = [
            item for item in filtered
            if item.get('_deal_date') and
            datetime.strptime(item['_deal_date'], '%Y-%m-%d') >= start_date
        ]

    if end_date:
        filtered = [
            item for item in filtered
            if item.get('_deal_date') and
            datetime.strptime(item['_deal_date'], '%Y-%m-%d') <= end_date
        ]

    return filtered


def extract_numeric_values(items: List[Dict], field: str) -> List[float]:
    """
    딕셔너리 리스트에서 숫자 값 추출

    Args:
        items: 데이터 리스트
        field: 필드명

    Returns:
        None이 아닌 숫자 값 리스트
    """
    return [
        item[field]
        for item in items
        if item.get(field) is not None
    ]


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    안전한 나눗셈 (0으로 나누기 방지)

    Args:
        numerator: 분자
        denominator: 분모
        default: 분모가 0일 때 반환값

    Returns:
        나눗셈 결과 또는 기본값
    """
    if denominator == 0 or denominator is None:
        return default
    return numerator / denominator


def format_price(price: float) -> str:
    """
    가격을 읽기 좋은 형식으로 포맷

    Args:
        price: 가격 (만원 단위)

    Returns:
        포맷된 문자열 (예: "15억 3,000만원")
    """
    if price >= 10000:
        eok = int(price / 10000)
        remain = int(price % 10000)
        if remain > 0:
            return f"{eok}억 {remain:,}만원"
        else:
            return f"{eok}억원"
    else:
        return f"{int(price):,}만원"


def parse_year_month(year_month: str) -> Optional[datetime]:
    """
    YYYYMM 형식의 문자열을 datetime으로 변환

    Args:
        year_month: YYYYMM 형식 문자열

    Returns:
        datetime 객체 또는 None
    """
    try:
        return datetime.strptime(year_month, '%Y%m')
    except (ValueError, TypeError):
        return None


def calculate_percentage_change(old_value: float, new_value: float) -> Optional[float]:
    """
    변화율 계산

    Args:
        old_value: 이전 값
        new_value: 새로운 값

    Returns:
        변화율 (%) 또는 None
    """
    if old_value == 0 or old_value is None:
        return None

    return ((new_value - old_value) / old_value) * 100
