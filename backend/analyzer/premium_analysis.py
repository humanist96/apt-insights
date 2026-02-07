"""
프리미엄 분석 모듈
평당가, 층수 프리미엄, 건물연식 프리미엄 등
"""
from typing import List, Dict
from collections import defaultdict
from datetime import datetime
import statistics


def calculate_price_per_area(items: List[Dict]) -> Dict:
    """
    평당가(㎡당 가격) 분석

    Args:
        items: 거래 데이터 리스트

    Returns:
        평당가 분석 데이터
    """
    # 면적과 가격이 모두 있는 데이터만 필터링
    valid_items = [
        item
        for item in items
        if item.get("_area_numeric") is not None
        and item.get("_deal_amount_numeric") is not None
        and item.get("_area_numeric") > 0
    ]

    if not valid_items:
        return {
            "stats": {},
            "by_region": [],
            "by_area_range": [],
            "by_build_year": [],
            "top_expensive": [],
            "top_affordable": [],
        }

    # 평당가 계산 추가
    for item in valid_items:
        item["_price_per_area"] = item["_deal_amount_numeric"] / item["_area_numeric"]

    # 전체 평당가 통계
    prices_per_area = [item["_price_per_area"] for item in valid_items]
    overall_stats = {
        "avg_price_per_area": statistics.mean(prices_per_area),
        "median_price_per_area": statistics.median(prices_per_area),
        "max_price_per_area": max(prices_per_area),
        "min_price_per_area": min(prices_per_area),
        "std_price_per_area": statistics.stdev(prices_per_area)
        if len(prices_per_area) > 1
        else 0,
        "total_count": len(valid_items),
    }

    # 지역별 평당가
    region_data = defaultdict(lambda: {"prices_per_area": [], "count": 0})
    for item in valid_items:
        region = item.get("_region_name", "미지정")
        region_data[region]["prices_per_area"].append(item["_price_per_area"])
        region_data[region]["count"] += 1

    by_region = []
    for region in sorted(region_data.keys()):
        stats = region_data[region]
        if stats["prices_per_area"]:
            by_region.append(
                {
                    "region": region,
                    "count": stats["count"],
                    "avg_price_per_area": statistics.mean(stats["prices_per_area"]),
                    "median_price_per_area": statistics.median(
                        stats["prices_per_area"]
                    ),
                    "max_price_per_area": max(stats["prices_per_area"]),
                    "min_price_per_area": min(stats["prices_per_area"]),
                }
            )

    # 면적대별 평당가 (소형/중형/대형)
    area_ranges = [
        ("소형 (60㎡ 미만)", 0, 60),
        ("중소형 (60-85㎡)", 60, 85),
        ("중형 (85-102㎡)", 85, 102),
        ("중대형 (102-135㎡)", 102, 135),
        ("대형 (135㎡ 이상)", 135, float("inf")),
    ]

    by_area_range = []
    for range_name, min_area, max_area in area_ranges:
        range_items = [
            item for item in valid_items if min_area <= item["_area_numeric"] < max_area
        ]
        if range_items:
            prices = [item["_price_per_area"] for item in range_items]
            by_area_range.append(
                {
                    "area_range": range_name,
                    "count": len(range_items),
                    "avg_price_per_area": statistics.mean(prices),
                    "median_price_per_area": statistics.median(prices),
                    "avg_total_price": statistics.mean(
                        [item["_deal_amount_numeric"] for item in range_items]
                    ),
                    "avg_area": statistics.mean(
                        [item["_area_numeric"] for item in range_items]
                    ),
                }
            )

    # 건축년도별 평당가 (신축 프리미엄 분석)
    current_year = datetime.now().year
    build_year_ranges = [
        ("신축 (5년 이내)", current_year - 5, current_year + 1),
        ("준신축 (6-10년)", current_year - 10, current_year - 5),
        ("중년 (11-20년)", current_year - 20, current_year - 10),
        ("구축 (21-30년)", current_year - 30, current_year - 20),
        ("노후 (30년 이상)", 1900, current_year - 30),
    ]

    by_build_year = []
    for range_name, min_year, max_year in build_year_ranges:
        range_items = [
            item
            for item in valid_items
            if item.get("_build_year_numeric") is not None
            and min_year <= item["_build_year_numeric"] < max_year
        ]
        if range_items:
            prices = [item["_price_per_area"] for item in range_items]
            by_build_year.append(
                {
                    "build_year_range": range_name,
                    "count": len(range_items),
                    "avg_price_per_area": statistics.mean(prices),
                    "median_price_per_area": statistics.median(prices),
                    "avg_build_year": int(
                        statistics.mean(
                            [item["_build_year_numeric"] for item in range_items]
                        )
                    ),
                }
            )

    # TOP 10 고가 (평당가 기준)
    sorted_by_price = sorted(
        valid_items, key=lambda x: x["_price_per_area"], reverse=True
    )
    top_expensive = []
    for item in sorted_by_price[:10]:
        top_expensive.append(
            {
                "apt_name": item.get("aptNm", "") or item.get("아파트", "N/A"),
                "region": item.get("_region_name", "N/A"),
                "price_per_area": item["_price_per_area"],
                "total_price": item["_deal_amount_numeric"],
                "area": item["_area_numeric"],
                "floor": item.get("_floor_numeric"),
                "build_year": item.get("_build_year_numeric"),
                "deal_date": item.get("_deal_date_str", "N/A"),
            }
        )

    # TOP 10 저가 (평당가 기준)
    top_affordable = []
    for item in sorted_by_price[-10:]:
        top_affordable.append(
            {
                "apt_name": item.get("aptNm", "") or item.get("아파트", "N/A"),
                "region": item.get("_region_name", "N/A"),
                "price_per_area": item["_price_per_area"],
                "total_price": item["_deal_amount_numeric"],
                "area": item["_area_numeric"],
                "floor": item.get("_floor_numeric"),
                "build_year": item.get("_build_year_numeric"),
                "deal_date": item.get("_deal_date_str", "N/A"),
            }
        )

    return {
        "stats": overall_stats,
        "by_region": sorted(
            by_region, key=lambda x: x["avg_price_per_area"], reverse=True
        ),
        "by_area_range": by_area_range,
        "by_build_year": by_build_year,
        "top_expensive": top_expensive,
        "top_affordable": list(reversed(top_affordable)),  # 낮은 순서대로
    }


def analyze_price_per_area_trend(items: List[Dict]) -> Dict:
    """
    월별 평당가 추이 분석

    Args:
        items: 거래 데이터 리스트

    Returns:
        월별 평당가 추이 데이터
    """
    # 면적, 가격, 날짜가 모두 있는 데이터만 필터링
    valid_items = [
        item
        for item in items
        if item.get("_area_numeric") is not None
        and item.get("_deal_amount_numeric") is not None
        and item.get("_deal_year_month") is not None
        and item.get("_area_numeric") > 0
    ]

    if not valid_items:
        return {"trend": []}

    # 월별 데이터 그룹화
    monthly_data = defaultdict(lambda: {"prices_per_area": [], "count": 0})

    for item in valid_items:
        year_month = item["_deal_year_month"]
        price_per_area = item["_deal_amount_numeric"] / item["_area_numeric"]

        monthly_data[year_month]["prices_per_area"].append(price_per_area)
        monthly_data[year_month]["count"] += 1

    # 월별 평당가 통계
    trend_data = []
    for year_month in sorted(monthly_data.keys()):
        prices = monthly_data[year_month]["prices_per_area"]
        if prices:
            trend_data.append(
                {
                    "year_month": year_month,
                    "count": monthly_data[year_month]["count"],
                    "avg_price_per_area": statistics.mean(prices),
                    "median_price_per_area": statistics.median(prices),
                    "max_price_per_area": max(prices),
                    "min_price_per_area": min(prices),
                }
            )

    # 변동률 계산
    for i in range(1, len(trend_data)):
        prev_avg = trend_data[i - 1]["avg_price_per_area"]
        curr_avg = trend_data[i]["avg_price_per_area"]
        if prev_avg > 0:
            trend_data[i]["change_rate"] = ((curr_avg - prev_avg) / prev_avg) * 100
        else:
            trend_data[i]["change_rate"] = 0

    if trend_data:
        trend_data[0]["change_rate"] = 0

    return {"trend": trend_data}


def analyze_floor_premium(items: List[Dict]) -> Dict:
    """
    층수 프리미엄 분석

    저층/중층/고층별 가격 차이 및 프리미엄 정량화

    Args:
        items: 거래 데이터 리스트

    Returns:
        층수 프리미엄 분석 결과
    """
    # 층수, 가격, 면적이 모두 있는 데이터만 필터링
    valid_items = [
        item
        for item in items
        if item.get("_floor_numeric") is not None
        and item.get("_deal_amount_numeric") is not None
        and item.get("_area_numeric") is not None
        and item.get("_area_numeric") > 0
    ]

    if len(valid_items) < 10:
        return {
            "has_data": False,
            "message": f"층수 프리미엄 분석을 위한 데이터가 부족합니다. (현재 {len(valid_items)}건)",
        }

    # 평당가 계산
    for item in valid_items:
        item["_price_per_area"] = item["_deal_amount_numeric"] / item["_area_numeric"]

    # 층수 구간 분류
    def get_floor_category(floor):
        if floor <= 0:
            return "지하/반지하"
        elif floor <= 5:
            return "저층 (1-5층)"
        elif floor <= 10:
            return "중저층 (6-10층)"
        elif floor <= 15:
            return "중층 (11-15층)"
        elif floor <= 20:
            return "중고층 (16-20층)"
        else:
            return "고층 (21층+)"

    # 층수 구간별 데이터
    floor_data = defaultdict(lambda: {"prices": [], "prices_per_area": [], "count": 0})

    for item in valid_items:
        floor = item["_floor_numeric"]
        category = get_floor_category(floor)

        floor_data[category]["prices"].append(item["_deal_amount_numeric"])
        floor_data[category]["prices_per_area"].append(item["_price_per_area"])
        floor_data[category]["count"] += 1

    # 층수 구간별 통계
    floor_order = [
        "지하/반지하",
        "저층 (1-5층)",
        "중저층 (6-10층)",
        "중층 (11-15층)",
        "중고층 (16-20층)",
        "고층 (21층+)",
    ]

    by_floor_category = []
    for category in floor_order:
        if category in floor_data:
            data = floor_data[category]
            if data["prices"]:
                by_floor_category.append(
                    {
                        "floor_category": category,
                        "count": data["count"],
                        "avg_price": statistics.mean(data["prices"]),
                        "median_price": statistics.median(data["prices"]),
                        "avg_price_per_area": statistics.mean(data["prices_per_area"]),
                        "median_price_per_area": statistics.median(
                            data["prices_per_area"]
                        ),
                    }
                )

    # 기준층(중층) 대비 프리미엄 계산
    base_category = "중층 (11-15층)"
    base_price_per_area = None

    for cat in by_floor_category:
        if cat["floor_category"] == base_category:
            base_price_per_area = cat["avg_price_per_area"]
            break

    # 기준층이 없으면 전체 평균 사용
    if base_price_per_area is None:
        all_prices_per_area = [item["_price_per_area"] for item in valid_items]
        base_price_per_area = statistics.mean(all_prices_per_area)

    # 프리미엄 계산
    for cat in by_floor_category:
        if base_price_per_area > 0:
            cat["premium_pct"] = (
                (cat["avg_price_per_area"] - base_price_per_area) / base_price_per_area
            ) * 100
        else:
            cat["premium_pct"] = 0

    # 개별 층수별 분석
    floor_detail = defaultdict(lambda: {"prices_per_area": [], "count": 0})
    for item in valid_items:
        floor = item["_floor_numeric"]
        if 1 <= floor <= 30:  # 1-30층만
            floor_detail[floor]["prices_per_area"].append(item["_price_per_area"])
            floor_detail[floor]["count"] += 1

    by_individual_floor = []
    for floor in sorted(floor_detail.keys()):
        data = floor_detail[floor]
        if data["prices_per_area"]:
            avg_ppa = statistics.mean(data["prices_per_area"])
            by_individual_floor.append(
                {
                    "floor": floor,
                    "count": data["count"],
                    "avg_price_per_area": avg_ppa,
                    "premium_pct": (
                        (avg_ppa - base_price_per_area) / base_price_per_area
                    )
                    * 100
                    if base_price_per_area > 0
                    else 0,
                }
            )

    # 로열층 분석 (가장 높은 평당가 층수)
    if by_individual_floor:
        royal_floor = max(by_individual_floor, key=lambda x: x["avg_price_per_area"])
    else:
        royal_floor = None

    # 전체 통계
    all_prices_per_area = [item["_price_per_area"] for item in valid_items]
    stats = {
        "total_count": len(valid_items),
        "avg_price_per_area": statistics.mean(all_prices_per_area),
        "base_floor_category": base_category,
        "base_price_per_area": base_price_per_area,
        "royal_floor": royal_floor["floor"] if royal_floor else None,
        "royal_premium_pct": royal_floor["premium_pct"] if royal_floor else 0,
    }

    return {
        "has_data": True,
        "stats": stats,
        "by_floor_category": by_floor_category,
        "by_individual_floor": by_individual_floor,
        "royal_floor_info": royal_floor,
    }


def analyze_building_age_premium(items: List[Dict]) -> Dict:
    """
    건축년도별 프리미엄 분석 (신축 프리미엄, 감가상각률)

    Args:
        items: 거래 데이터 리스트

    Returns:
        건축년도별 프리미엄 분석 결과
    """
    current_year = datetime.now().year

    # 건축년도, 가격, 면적이 모두 있는 데이터만 필터링
    valid_items = [
        item
        for item in items
        if item.get("_build_year_numeric") is not None
        and item.get("_deal_amount_numeric") is not None
        and item.get("_area_numeric") is not None
        and item.get("_area_numeric") > 0
        and 1970 <= item.get("_build_year_numeric") <= current_year
    ]

    if len(valid_items) < 10:
        return {
            "has_data": False,
            "message": f"건축년도 프리미엄 분석을 위한 데이터가 부족합니다. (현재 {len(valid_items)}건)",
        }

    # 평당가 및 건물 연식 계산
    for item in valid_items:
        item["_price_per_area"] = item["_deal_amount_numeric"] / item["_area_numeric"]
        item["_building_age"] = current_year - item["_build_year_numeric"]

    # 연식 구간 분류
    age_ranges = [
        ("신축 (0-5년)", 0, 5),
        ("준신축 (6-10년)", 6, 10),
        ("중년 (11-15년)", 11, 15),
        ("노후화 (16-20년)", 16, 20),
        ("구축 (21-30년)", 21, 30),
        ("재건축 대상 (30년+)", 31, 100),
    ]

    by_age_range = []
    for range_name, min_age, max_age in age_ranges:
        range_items = [
            item for item in valid_items if min_age <= item["_building_age"] <= max_age
        ]
        if range_items:
            prices_per_area = [item["_price_per_area"] for item in range_items]
            by_age_range.append(
                {
                    "age_range": range_name,
                    "min_age": min_age,
                    "max_age": max_age,
                    "count": len(range_items),
                    "avg_price_per_area": statistics.mean(prices_per_area),
                    "median_price_per_area": statistics.median(prices_per_area),
                    "avg_building_age": statistics.mean(
                        [item["_building_age"] for item in range_items]
                    ),
                }
            )

    # 신축 대비 프리미엄 계산
    base_price = None
    for age_data in by_age_range:
        if age_data["age_range"] == "신축 (0-5년)":
            base_price = age_data["avg_price_per_area"]
            break

    if base_price is None and by_age_range:
        base_price = by_age_range[0]["avg_price_per_area"]

    for age_data in by_age_range:
        if base_price and base_price > 0:
            age_data["vs_new_pct"] = (
                (age_data["avg_price_per_area"] - base_price) / base_price
            ) * 100
        else:
            age_data["vs_new_pct"] = 0

    # 연도별 상세 분석 (최근 20년)
    by_build_year = defaultdict(lambda: {"prices_per_area": [], "count": 0})
    for item in valid_items:
        year = item["_build_year_numeric"]
        if year >= current_year - 30:  # 최근 30년
            by_build_year[year]["prices_per_area"].append(item["_price_per_area"])
            by_build_year[year]["count"] += 1

    year_detail = []
    for year in sorted(by_build_year.keys(), reverse=True):
        data = by_build_year[year]
        if data["prices_per_area"]:
            avg_ppa = statistics.mean(data["prices_per_area"])
            year_detail.append(
                {
                    "build_year": year,
                    "building_age": current_year - year,
                    "count": data["count"],
                    "avg_price_per_area": avg_ppa,
                    "vs_new_pct": ((avg_ppa - base_price) / base_price * 100)
                    if base_price and base_price > 0
                    else 0,
                }
            )

    # 감가상각률 계산 (연간 평균)
    if len(by_age_range) >= 2:
        newest = by_age_range[0]
        oldest = by_age_range[-1]
        age_diff = oldest["avg_building_age"] - newest["avg_building_age"]
        price_diff_pct = oldest["vs_new_pct"]
        annual_depreciation = price_diff_pct / age_diff if age_diff > 0 else 0
    else:
        annual_depreciation = 0

    # 재건축 대상 (30년 이상)
    rebuild_candidates = [
        {
            "apt_name": item.get("aptNm", "") or item.get("아파트", ""),
            "region": item.get("_region_name", ""),
            "build_year": item["_build_year_numeric"],
            "building_age": item["_building_age"],
            "price_per_area": item["_price_per_area"],
            "total_price": item["_deal_amount_numeric"],
        }
        for item in valid_items
        if item["_building_age"] >= 30
    ]

    # 중복 제거 및 정렬
    seen = set()
    unique_rebuild = []
    for item in rebuild_candidates:
        key = (item["apt_name"], item["region"])
        if key not in seen and item["apt_name"]:
            seen.add(key)
            unique_rebuild.append(item)

    unique_rebuild = sorted(
        unique_rebuild, key=lambda x: x["building_age"], reverse=True
    )[:20]

    # 통계
    all_prices_per_area = [item["_price_per_area"] for item in valid_items]
    stats = {
        "total_count": len(valid_items),
        "avg_price_per_area": statistics.mean(all_prices_per_area),
        "new_building_price": base_price,
        "annual_depreciation_pct": annual_depreciation,
        "rebuild_candidate_count": len(rebuild_candidates),
    }

    return {
        "has_data": True,
        "stats": stats,
        "by_age_range": by_age_range,
        "by_build_year": year_detail[:20],  # 최근 20개 연도
        "rebuild_candidates": unique_rebuild,
    }
