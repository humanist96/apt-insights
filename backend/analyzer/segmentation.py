"""
세분화 분석 모듈
면적, 층수, 건축년도, 지역, 아파트별 분석
"""
from typing import List, Dict, Optional
from collections import defaultdict
import statistics


def analyze_by_area(items: List[Dict], bins: Optional[List[float]] = None) -> Dict:
    """
    면적별 가격 분석

    Args:
        items: 거래 데이터 리스트
        bins: 면적 구간 리스트 (None이면 자동 생성)

    Returns:
        면적별 분석 데이터
    """
    # 면적과 가격이 모두 있는 데이터만 필터링
    valid_items = [
        item
        for item in items
        if item.get("_area_numeric") is not None
        and item.get("_deal_amount_numeric") is not None
    ]

    if not valid_items:
        return {"bins": [], "data": []}

    # 면적 구간 설정
    if bins is None:
        areas = [item.get("_area_numeric") for item in valid_items]
        min_area = min(areas)
        max_area = max(areas)
        # 10개 구간으로 나누기
        bin_size = (max_area - min_area) / 10
        bins = [min_area + i * bin_size for i in range(11)]

    # 구간별 데이터 그룹화
    bin_data = defaultdict(lambda: {"prices": [], "count": 0, "areas": []})

    for item in valid_items:
        area = item.get("_area_numeric")
        price = item.get("_deal_amount_numeric")

        # 어느 구간에 속하는지 찾기
        bin_idx = 0
        for i in range(len(bins) - 1):
            if bins[i] <= area < bins[i + 1]:
                bin_idx = i
                break
        else:
            # 마지막 구간
            if area >= bins[-1]:
                bin_idx = len(bins) - 2

        bin_key = f"{bins[bin_idx]:.1f}~{bins[bin_idx + 1]:.1f}"
        bin_data[bin_key]["prices"].append(price)
        bin_data[bin_key]["areas"].append(area)
        bin_data[bin_key]["count"] += 1

    # 구간별 통계 계산
    result_data = []
    for bin_key in sorted(bin_data.keys(), key=lambda x: float(x.split("~")[0])):
        stats = bin_data[bin_key]
        if stats["prices"]:
            result_data.append(
                {
                    "area_range": bin_key,
                    "count": stats["count"],
                    "avg_price": statistics.mean(stats["prices"]),
                    "median_price": statistics.median(stats["prices"]),
                    "avg_area": statistics.mean(stats["areas"]),
                    "price_per_area": statistics.mean(stats["prices"])
                    / statistics.mean(stats["areas"])
                    if stats["areas"]
                    else 0,
                }
            )

    return {"bins": bins, "data": result_data}


def analyze_by_floor(items: List[Dict]) -> Dict:
    """
    층수별 평균가격 분석

    Args:
        items: 거래 데이터 리스트

    Returns:
        층수별 분석 데이터
    """
    # 층수와 가격이 모두 있는 데이터만 필터링
    valid_items = [
        item
        for item in items
        if item.get("_floor") is not None
        and item.get("_deal_amount_numeric") is not None
    ]

    if not valid_items:
        return {"data": []}

    # 층수별 데이터 그룹화
    floor_data = defaultdict(lambda: {"prices": [], "count": 0})

    for item in valid_items:
        floor = item.get("_floor")
        price = item.get("_deal_amount_numeric")

        floor_data[floor]["prices"].append(price)
        floor_data[floor]["count"] += 1

    # 층수별 통계 계산
    result_data = []
    for floor in sorted(floor_data.keys()):
        stats = floor_data[floor]
        if stats["prices"]:
            result_data.append(
                {
                    "floor": floor,
                    "count": stats["count"],
                    "avg_price": statistics.mean(stats["prices"]),
                    "median_price": statistics.median(stats["prices"]),
                    "max_price": max(stats["prices"]),
                    "min_price": min(stats["prices"]),
                }
            )

    return {"data": result_data}


def analyze_by_build_year(items: List[Dict]) -> Dict:
    """
    건축년도별 분석

    Args:
        items: 거래 데이터 리스트

    Returns:
        건축년도별 분석 데이터
    """
    # 건축년도와 가격이 모두 있는 데이터만 필터링
    valid_items = [
        item
        for item in items
        if item.get("_build_year") is not None
        and item.get("_deal_amount_numeric") is not None
    ]

    if not valid_items:
        return {"data": []}

    # 건축년도별 데이터 그룹화
    year_data = defaultdict(lambda: {"prices": [], "count": 0})

    for item in valid_items:
        build_year = item.get("_build_year")
        price = item.get("_deal_amount_numeric")

        year_data[build_year]["prices"].append(price)
        year_data[build_year]["count"] += 1

    # 건축년도별 통계 계산
    result_data = []
    for build_year in sorted(year_data.keys()):
        stats = year_data[build_year]
        if stats["prices"]:
            result_data.append(
                {
                    "build_year": build_year,
                    "count": stats["count"],
                    "avg_price": statistics.mean(stats["prices"]),
                    "median_price": statistics.median(stats["prices"]),
                    "max_price": max(stats["prices"]),
                    "min_price": min(stats["prices"]),
                }
            )

    return {"data": result_data}


def analyze_by_region(items: List[Dict]) -> Dict:
    """
    지역별 거래 분석

    Args:
        items: 거래 데이터 리스트

    Returns:
        지역별 분석 데이터
    """
    # 지역별 데이터 그룹화
    region_data = defaultdict(
        lambda: {"prices": [], "count": 0, "areas": [], "apartments": set()}
    )

    for item in items:
        region = item.get("_region_name", "미지정")
        price = item.get("_deal_amount_numeric")
        area = item.get("_area_numeric")
        apt_name = item.get("아파트", "")

        region_data[region]["count"] += 1
        if price is not None:
            region_data[region]["prices"].append(price)
        if area is not None:
            region_data[region]["areas"].append(area)
        if apt_name:
            region_data[region]["apartments"].add(apt_name)

    # 지역별 통계 계산
    result_data = []
    for region in sorted(region_data.keys()):
        stats = region_data[region]
        if stats["prices"]:
            result_data.append(
                {
                    "region": region,
                    "count": stats["count"],
                    "avg_price": statistics.mean(stats["prices"]),
                    "median_price": statistics.median(stats["prices"]),
                    "max_price": max(stats["prices"]),
                    "min_price": min(stats["prices"]),
                    "avg_area": statistics.mean(stats["areas"]) if stats["areas"] else 0,
                    "apartment_count": len(stats["apartments"]),
                }
            )

    return {"data": result_data}


def analyze_by_apartment(items: List[Dict]) -> Dict:
    """
    아파트별 거래 분석

    Args:
        items: 거래 데이터 리스트

    Returns:
        아파트별 분석 데이터
    """
    # 아파트별 데이터 그룹화
    apt_data = defaultdict(
        lambda: {
            "prices": [],
            "count": 0,
            "areas": [],
            "regions": set(),
            "build_years": set(),
        }
    )

    for item in items:
        apt_name = item.get("아파트", "미지정")
        price = item.get("_deal_amount_numeric")
        area = item.get("_area_numeric")
        region = item.get("_region_name", "")
        build_year = item.get("건축년도", "")

        apt_data[apt_name]["count"] += 1
        if price is not None:
            apt_data[apt_name]["prices"].append(price)
        if area is not None:
            apt_data[apt_name]["areas"].append(area)
        if region:
            apt_data[apt_name]["regions"].add(region)
        if build_year:
            apt_data[apt_name]["build_years"].add(build_year)

    # 아파트별 통계 계산
    result_data = []
    for apt_name in sorted(apt_data.keys()):
        stats = apt_data[apt_name]
        if stats["prices"]:
            result_data.append(
                {
                    "apartment": apt_name,
                    "count": stats["count"],
                    "avg_price": statistics.mean(stats["prices"]),
                    "median_price": statistics.median(stats["prices"]),
                    "max_price": max(stats["prices"]),
                    "min_price": min(stats["prices"]),
                    "avg_area": statistics.mean(stats["areas"]) if stats["areas"] else 0,
                    "regions": list(stats["regions"]),
                    "build_years": sorted(list(stats["build_years"])),
                }
            )

    return {"data": result_data}


def get_apartment_detail(items: List[Dict], apt_name: str, region: str = None) -> Dict:
    """
    특정 아파트의 상세 거래 정보

    Args:
        items: 거래 데이터 리스트
        apt_name: 아파트 이름
        region: 지역명 (선택)

    Returns:
        아파트 상세 정보
    """
    # 해당 아파트 데이터만 필터링
    apt_items = [item for item in items if item.get("아파트") == apt_name]

    if region:
        apt_items = [item for item in apt_items if item.get("_region_name") == region]

    if not apt_items:
        return {"found": False, "apartment": apt_name}

    # 가격 데이터
    prices = [
        item["_deal_amount_numeric"]
        for item in apt_items
        if item.get("_deal_amount_numeric") is not None
    ]

    # 면적별 분석
    area_data = defaultdict(lambda: {"prices": [], "count": 0})
    for item in apt_items:
        area = item.get("전용면적", "미지정")
        price = item.get("_deal_amount_numeric")
        if price is not None:
            area_data[area]["prices"].append(price)
            area_data[area]["count"] += 1

    by_area = []
    for area in sorted(area_data.keys()):
        stats = area_data[area]
        if stats["prices"]:
            by_area.append(
                {
                    "area": area,
                    "count": stats["count"],
                    "avg_price": statistics.mean(stats["prices"]),
                    "max_price": max(stats["prices"]),
                    "min_price": min(stats["prices"]),
                }
            )

    # 최근 거래 (최대 10개)
    recent_deals = sorted(
        apt_items, key=lambda x: x.get("_deal_date", ""), reverse=True
    )[:10]

    return {
        "found": True,
        "apartment": apt_name,
        "total_count": len(apt_items),
        "avg_price": statistics.mean(prices) if prices else 0,
        "max_price": max(prices) if prices else 0,
        "min_price": min(prices) if prices else 0,
        "by_area": by_area,
        "recent_deals": recent_deals,
    }
