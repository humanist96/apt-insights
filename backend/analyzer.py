"""
데이터 분석 모듈
기본 통계 및 고급 분석 기능 제공
"""

from typing import List, Dict, Optional
from collections import defaultdict
from datetime import datetime, timedelta
import statistics


def calculate_basic_stats(items: List[Dict]) -> Dict:
    """
    기본 통계 계산

    Args:
        items: 거래 데이터 리스트

    Returns:
        기본 통계 정보 (거래건수, 평균가격, 최고가, 최저가 등)
    """
    if not items:
        return {
            "total_count": 0,
            "avg_price": 0,
            "max_price": 0,
            "min_price": 0,
            "median_price": 0,
            "avg_area": 0,
            "regions": {},
        }

    # 가격 데이터 추출 (None 제외)
    prices = [
        item.get("_deal_amount_numeric")
        for item in items
        if item.get("_deal_amount_numeric") is not None
    ]

    # 면적 데이터 추출
    areas = [
        item.get("_area_numeric")
        for item in items
        if item.get("_area_numeric") is not None
    ]

    # 지역별 통계
    region_stats = defaultdict(lambda: {"count": 0, "prices": []})

    for item in items:
        region = item.get("_region_name", "미지정")
        price = item.get("_deal_amount_numeric")

        region_stats[region]["count"] += 1
        if price is not None:
            region_stats[region]["prices"].append(price)

    # 지역별 평균 가격 계산
    region_avg_prices = {}
    for region, stats in region_stats.items():
        if stats["prices"]:
            region_avg_prices[region] = {
                "count": stats["count"],
                "avg_price": statistics.mean(stats["prices"]),
                "max_price": max(stats["prices"]),
                "min_price": min(stats["prices"]),
            }
        else:
            region_avg_prices[region] = {
                "count": stats["count"],
                "avg_price": 0,
                "max_price": 0,
                "min_price": 0,
            }

    return {
        "total_count": len(items),
        "avg_price": statistics.mean(prices) if prices else 0,
        "max_price": max(prices) if prices else 0,
        "min_price": min(prices) if prices else 0,
        "median_price": statistics.median(prices) if prices else 0,
        "avg_area": statistics.mean(areas) if areas else 0,
        "regions": region_avg_prices,
    }


def calculate_price_trend(items: List[Dict]) -> Dict:
    """
    월별 가격 추이 분석

    Args:
        items: 거래 데이터 리스트

    Returns:
        월별 가격 추이 데이터
    """
    # 월별 데이터 그룹화
    monthly_data = defaultdict(lambda: {"prices": [], "count": 0})

    for item in items:
        year_month = item.get("_deal_year_month")
        price = item.get("_deal_amount_numeric")

        if year_month and price is not None:
            monthly_data[year_month]["prices"].append(price)
            monthly_data[year_month]["count"] += 1

    # 월별 평균 가격 계산
    trend_data = {}
    for year_month in sorted(monthly_data.keys()):
        prices = monthly_data[year_month]["prices"]
        if prices:
            trend_data[year_month] = {
                "avg_price": statistics.mean(prices),
                "median_price": statistics.median(prices),
                "count": monthly_data[year_month]["count"],
                "max_price": max(prices),
                "min_price": min(prices),
            }

    return trend_data


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
        if item.get("_floor_numeric") is not None
        and item.get("_deal_amount_numeric") is not None
    ]

    if not valid_items:
        return {"data": []}

    # 층수별 데이터 그룹화
    floor_data = defaultdict(lambda: {"prices": [], "count": 0})

    for item in valid_items:
        floor = item.get("_floor_numeric")
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
        if item.get("_build_year_numeric") is not None
        and item.get("_deal_amount_numeric") is not None
    ]

    if not valid_items:
        return {"data": []}

    # 건축년도별 데이터 그룹화
    year_data = defaultdict(lambda: {"prices": [], "count": 0})

    for item in valid_items:
        build_year = item.get("_build_year_numeric")
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


def analyze_by_region(items: List[Dict]) -> Dict:
    """
    지역별 상세 분석

    Args:
        items: 거래 데이터 리스트

    Returns:
        지역별 분석 데이터
    """
    # 지역별 데이터 그룹화
    region_data = defaultdict(
        lambda: {"prices": [], "areas": [], "count": 0, "floors": [], "build_years": []}
    )

    for item in items:
        region = item.get("_region_name", "미지정")
        price = item.get("_deal_amount_numeric")
        area = item.get("_area_numeric")
        floor = item.get("_floor_numeric")
        build_year = item.get("_build_year_numeric")

        region_data[region]["count"] += 1

        if price is not None:
            region_data[region]["prices"].append(price)
        if area is not None:
            region_data[region]["areas"].append(area)
        if floor is not None:
            region_data[region]["floors"].append(floor)
        if build_year is not None:
            region_data[region]["build_years"].append(build_year)

    # 지역별 통계 계산
    result_data = []
    for region in sorted(region_data.keys()):
        stats = region_data[region]
        region_stats = {"region": region, "count": stats["count"]}

        if stats["prices"]:
            region_stats["avg_price"] = statistics.mean(stats["prices"])
            region_stats["median_price"] = statistics.median(stats["prices"])
            region_stats["max_price"] = max(stats["prices"])
            region_stats["min_price"] = min(stats["prices"])

        if stats["areas"]:
            region_stats["avg_area"] = statistics.mean(stats["areas"])

        if stats["prices"] and stats["areas"]:
            region_stats["price_per_area"] = statistics.mean(
                stats["prices"]
            ) / statistics.mean(stats["areas"])

        if stats["floors"]:
            region_stats["avg_floor"] = statistics.mean(stats["floors"])

        if stats["build_years"]:
            region_stats["avg_build_year"] = int(statistics.mean(stats["build_years"]))

        result_data.append(region_stats)

    return {"data": result_data}


def analyze_by_apartment(items: List[Dict]) -> Dict:
    """
    아파트별 분석

    Args:
        items: 거래 데이터 리스트

    Returns:
        아파트별 분석 데이터
    """
    # 아파트별 데이터 그룹화
    apt_data = defaultdict(
        lambda: {
            "prices": [],
            "areas": [],
            "count": 0,
            "floors": [],
            "build_year": None,
            "region": None,
            "deals": [],  # 개별 거래 내역
        }
    )

    for item in items:
        # 아파트 이름 추출
        apt_name = (
            item.get("aptNm", "") or item.get("아파트", "") or item.get("apt", "")
        )
        if not apt_name:
            continue

        region = item.get("_region_name", "미지정")
        # 아파트 고유 키: 아파트명 + 지역
        apt_key = f"{apt_name}|{region}"

        price = item.get("_deal_amount_numeric")
        area = item.get("_area_numeric")
        floor = item.get("_floor_numeric")
        build_year = item.get("_build_year_numeric")
        deal_date = item.get("_deal_date_str")

        apt_data[apt_key]["count"] += 1
        apt_data[apt_key]["region"] = region
        apt_data[apt_key]["apt_name"] = apt_name

        if price is not None:
            apt_data[apt_key]["prices"].append(price)
        if area is not None:
            apt_data[apt_key]["areas"].append(area)
        if floor is not None:
            apt_data[apt_key]["floors"].append(floor)
        if build_year is not None:
            apt_data[apt_key]["build_year"] = build_year

        # 개별 거래 내역 저장
        apt_data[apt_key]["deals"].append(
            {
                "price": price,
                "area": area,
                "floor": floor,
                "deal_date": deal_date,
                "price_per_area": price / area if price and area and area > 0 else None,
            }
        )

    # 아파트별 통계 계산
    result_data = []
    for apt_key, stats in apt_data.items():
        apt_stats = {
            "apt_name": stats["apt_name"],
            "region": stats["region"],
            "count": stats["count"],
        }

        if stats["prices"]:
            apt_stats["avg_price"] = statistics.mean(stats["prices"])
            apt_stats["median_price"] = statistics.median(stats["prices"])
            apt_stats["max_price"] = max(stats["prices"])
            apt_stats["min_price"] = min(stats["prices"])
            if len(stats["prices"]) > 1:
                apt_stats["price_std"] = statistics.stdev(stats["prices"])
            else:
                apt_stats["price_std"] = 0

        if stats["areas"]:
            apt_stats["avg_area"] = statistics.mean(stats["areas"])
            apt_stats["area_list"] = sorted(
                set(stats["areas"])
            )  # 해당 아파트의 면적대 리스트

        if stats["prices"] and stats["areas"]:
            prices_per_area = [
                p / a for p, a in zip(stats["prices"], stats["areas"]) if a > 0
            ]
            if prices_per_area:
                apt_stats["avg_price_per_area"] = statistics.mean(prices_per_area)

        if stats["floors"]:
            apt_stats["avg_floor"] = statistics.mean(stats["floors"])
            apt_stats["floor_range"] = f"{min(stats['floors'])}~{max(stats['floors'])}"

        if stats["build_year"]:
            apt_stats["build_year"] = stats["build_year"]

        # 거래 내역 (최신순 정렬)
        apt_stats["deals"] = sorted(
            stats["deals"],
            key=lambda x: x["deal_date"] if x["deal_date"] else "",
            reverse=True,
        )

        result_data.append(apt_stats)

    # 거래건수 순으로 정렬
    result_data = sorted(result_data, key=lambda x: x["count"], reverse=True)

    return {
        "data": result_data,
        "total_apartments": len(result_data),
        "total_deals": sum(apt["count"] for apt in result_data),
    }


def get_apartment_detail(items: List[Dict], apt_name: str, region: str = None) -> Dict:
    """
    특정 아파트의 상세 정보 조회

    Args:
        items: 거래 데이터 리스트
        apt_name: 아파트 이름
        region: 지역명 (선택, 동일 이름 아파트 구분용)

    Returns:
        아파트 상세 정보
    """
    # 해당 아파트 데이터 필터링
    filtered_items = []
    for item in items:
        item_apt = (
            item.get("aptNm", "") or item.get("아파트", "") or item.get("apt", "")
        )
        item_region = item.get("_region_name", "")

        if apt_name.lower() in item_apt.lower():
            if region is None or region.lower() in item_region.lower():
                filtered_items.append(item)

    if not filtered_items:
        return {"found": False, "apt_name": apt_name, "data": None}

    # 면적별 분석
    area_data = defaultdict(
        lambda: {"prices": [], "floors": [], "count": 0, "deals": []}
    )

    for item in filtered_items:
        area = item.get("_area_numeric")
        if area is None:
            continue

        # 면적을 소수점 첫째자리까지 반올림하여 그룹화
        area_key = round(area, 1)

        price = item.get("_deal_amount_numeric")
        floor = item.get("_floor_numeric")
        deal_date = item.get("_deal_date_str")

        area_data[area_key]["count"] += 1

        if price is not None:
            area_data[area_key]["prices"].append(price)
        if floor is not None:
            area_data[area_key]["floors"].append(floor)

        area_data[area_key]["deals"].append(
            {
                "price": price,
                "floor": floor,
                "deal_date": deal_date,
                "price_per_area": price / area if price and area > 0 else None,
            }
        )

    # 면적별 통계
    by_area = []
    for area_key in sorted(area_data.keys()):
        stats = area_data[area_key]
        area_stats = {"area": area_key, "count": stats["count"]}

        if stats["prices"]:
            area_stats["avg_price"] = statistics.mean(stats["prices"])
            area_stats["median_price"] = statistics.median(stats["prices"])
            area_stats["max_price"] = max(stats["prices"])
            area_stats["min_price"] = min(stats["prices"])
            area_stats["avg_price_per_area"] = (
                statistics.mean(stats["prices"]) / area_key if area_key > 0 else 0
            )

        if stats["floors"]:
            area_stats["avg_floor"] = statistics.mean(stats["floors"])

        # 최신 거래 내역 (최대 10건)
        area_stats["recent_deals"] = sorted(
            stats["deals"],
            key=lambda x: x["deal_date"] if x["deal_date"] else "",
            reverse=True,
        )[:10]

        by_area.append(area_stats)

    # 전체 통계
    all_prices = [
        item.get("_deal_amount_numeric")
        for item in filtered_items
        if item.get("_deal_amount_numeric")
    ]
    all_areas = [
        item.get("_area_numeric")
        for item in filtered_items
        if item.get("_area_numeric")
    ]

    overall_stats = {}
    if all_prices:
        overall_stats["total_count"] = len(filtered_items)
        overall_stats["avg_price"] = statistics.mean(all_prices)
        overall_stats["median_price"] = statistics.median(all_prices)
        overall_stats["max_price"] = max(all_prices)
        overall_stats["min_price"] = min(all_prices)

    if all_prices and all_areas:
        prices_per_area = [p / a for p, a in zip(all_prices, all_areas) if a > 0]
        if prices_per_area:
            overall_stats["avg_price_per_area"] = statistics.mean(prices_per_area)

    # 건축년도, 지역 정보
    build_years = [
        item.get("_build_year_numeric")
        for item in filtered_items
        if item.get("_build_year_numeric")
    ]
    regions = [
        item.get("_region_name") for item in filtered_items if item.get("_region_name")
    ]

    if build_years:
        overall_stats["build_year"] = build_years[
            0
        ]  # 동일 아파트이므로 첫 번째 값 사용
    if regions:
        overall_stats["region"] = regions[0]

    return {
        "found": True,
        "apt_name": apt_name,
        "overall": overall_stats,
        "by_area": by_area,
        "area_count": len(by_area),
    }


def calculate_jeonse_ratio(items: List[Dict]) -> Dict:
    """
    전세가율 분석 (매매가 대비 전세가 비율)

    전세가율 = 전세가 / 매매가 × 100

    Args:
        items: 전체 거래 데이터 리스트 (API 02 매매 + API 04 전월세 포함)

    Returns:
        전세가율 분석 데이터
    """
    # API 02 (매매) 데이터 분리
    trade_items = [item for item in items if item.get("_api_type") == "api_02"]

    # API 04 (전월세) 데이터 분리 - 전세만 (monthlyRent가 0 또는 없음)
    rent_items = [item for item in items if item.get("_api_type") == "api_04"]
    jeonse_items = []
    for item in rent_items:
        monthly_rent = item.get("monthlyRent", "") or item.get("월세금액", "")
        try:
            rent_val = int(str(monthly_rent).replace(",", "").strip() or "0")
        except:
            rent_val = 0
        if rent_val == 0:  # 전세만
            jeonse_items.append(item)

    if not trade_items or not jeonse_items:
        return {
            "has_data": False,
            "message": "매매 또는 전세 데이터가 부족합니다.",
            "trade_count": len(trade_items),
            "jeonse_count": len(jeonse_items),
        }

    # 아파트별로 매매가와 전세가 매칭
    # 키: (아파트명, 지역, 면적대)
    def get_match_key(item):
        apt_name = item.get("aptNm", "") or item.get("아파트", "")
        region = item.get("_region_name", "") or ""
        area = item.get("_area_numeric")
        if area:
            # 면적을 5㎡ 단위로 반올림하여 그룹화
            area_group = round(area / 5) * 5
        else:
            area_group = 0
        return (apt_name, region, area_group)

    # 매매 데이터 그룹화
    trade_by_key = defaultdict(list)
    for item in trade_items:
        key = get_match_key(item)
        if key[0] and item.get("_deal_amount_numeric"):  # 아파트명과 가격이 있는 경우만
            trade_by_key[key].append(item)

    # 전세 데이터 그룹화
    jeonse_by_key = defaultdict(list)
    for item in jeonse_items:
        key = get_match_key(item)
        # 전세 보증금 추출
        deposit = item.get("deposit", "") or item.get("보증금액", "")
        try:
            deposit_val = float(str(deposit).replace(",", "").strip() or "0")
        except:
            deposit_val = 0
        if key[0] and deposit_val > 0:
            item["_deposit_numeric"] = deposit_val
            jeonse_by_key[key].append(item)

    # 전세가율 계산
    jeonse_ratio_data = []
    matched_count = 0

    for key in trade_by_key:
        if key in jeonse_by_key:
            trade_list = trade_by_key[key]
            jeonse_list = jeonse_by_key[key]

            # 각 그룹의 평균 가격 계산
            avg_trade_price = statistics.mean(
                [t["_deal_amount_numeric"] for t in trade_list]
            )
            avg_jeonse_price = statistics.mean(
                [j["_deposit_numeric"] for j in jeonse_list]
            )

            if avg_trade_price > 0:
                ratio = (avg_jeonse_price / avg_trade_price) * 100
                matched_count += 1

                jeonse_ratio_data.append(
                    {
                        "apt_name": key[0],
                        "region": key[1],
                        "area_group": key[2],
                        "avg_trade_price": avg_trade_price,
                        "avg_jeonse_price": avg_jeonse_price,
                        "jeonse_ratio": ratio,
                        "gap": avg_trade_price - avg_jeonse_price,  # 갭 금액
                        "trade_count": len(trade_list),
                        "jeonse_count": len(jeonse_list),
                    }
                )

    if not jeonse_ratio_data:
        return {
            "has_data": False,
            "message": "매칭되는 매매/전세 데이터가 없습니다.",
            "trade_count": len(trade_items),
            "jeonse_count": len(jeonse_items),
        }

    # 전체 통계
    all_ratios = [d["jeonse_ratio"] for d in jeonse_ratio_data]
    all_gaps = [d["gap"] for d in jeonse_ratio_data]

    overall_stats = {
        "avg_jeonse_ratio": statistics.mean(all_ratios),
        "median_jeonse_ratio": statistics.median(all_ratios),
        "max_jeonse_ratio": max(all_ratios),
        "min_jeonse_ratio": min(all_ratios),
        "avg_gap": statistics.mean(all_gaps),
        "matched_apartments": matched_count,
        "total_trade_items": len(trade_items),
        "total_jeonse_items": len(jeonse_items),
    }

    # 전세가율 위험 분류
    high_risk = [d for d in jeonse_ratio_data if d["jeonse_ratio"] >= 80]
    medium_risk = [d for d in jeonse_ratio_data if 70 <= d["jeonse_ratio"] < 80]
    low_risk = [d for d in jeonse_ratio_data if d["jeonse_ratio"] < 70]

    risk_summary = {
        "high_risk_count": len(high_risk),  # 80% 이상 - 위험
        "medium_risk_count": len(medium_risk),  # 70-80% - 주의
        "low_risk_count": len(low_risk),  # 70% 미만 - 안전
        "high_risk_pct": len(high_risk) / len(jeonse_ratio_data) * 100
        if jeonse_ratio_data
        else 0,
    }

    # 지역별 전세가율
    region_data = defaultdict(lambda: {"ratios": [], "gaps": [], "count": 0})
    for d in jeonse_ratio_data:
        region = d["region"]
        region_data[region]["ratios"].append(d["jeonse_ratio"])
        region_data[region]["gaps"].append(d["gap"])
        region_data[region]["count"] += 1

    by_region = []
    for region in sorted(region_data.keys()):
        stats = region_data[region]
        by_region.append(
            {
                "region": region,
                "avg_jeonse_ratio": statistics.mean(stats["ratios"]),
                "avg_gap": statistics.mean(stats["gaps"]),
                "count": stats["count"],
            }
        )

    # 지역별 전세가율 높은순 정렬
    by_region = sorted(by_region, key=lambda x: x["avg_jeonse_ratio"], reverse=True)

    # 면적대별 전세가율
    area_data = defaultdict(lambda: {"ratios": [], "gaps": [], "count": 0})
    for d in jeonse_ratio_data:
        area = d["area_group"]
        area_data[area]["ratios"].append(d["jeonse_ratio"])
        area_data[area]["gaps"].append(d["gap"])
        area_data[area]["count"] += 1

    by_area = []
    for area in sorted(area_data.keys()):
        if area > 0:
            stats = area_data[area]
            by_area.append(
                {
                    "area_group": f"{area - 2.5:.0f}~{area + 2.5:.0f}㎡",
                    "area_value": area,
                    "avg_jeonse_ratio": statistics.mean(stats["ratios"]),
                    "avg_gap": statistics.mean(stats["gaps"]),
                    "count": stats["count"],
                }
            )

    # 고위험 아파트 TOP 10 (전세가율 높은 순)
    high_ratio_apts = sorted(
        jeonse_ratio_data, key=lambda x: x["jeonse_ratio"], reverse=True
    )[:10]

    # 갭투자 적합 아파트 TOP 10 (갭 금액 낮은 순)
    low_gap_apts = sorted(jeonse_ratio_data, key=lambda x: x["gap"])[:10]

    return {
        "has_data": True,
        "stats": overall_stats,
        "risk_summary": risk_summary,
        "by_region": by_region,
        "by_area": by_area,
        "high_ratio_apartments": high_ratio_apts,
        "low_gap_apartments": low_gap_apts,
        "all_data": sorted(
            jeonse_ratio_data, key=lambda x: x["jeonse_ratio"], reverse=True
        ),
    }


def analyze_gap_investment(items: List[Dict]) -> Dict:
    """
    갭투자 적합도 분석

    갭 = 매매가 - 전세가
    갭이 작을수록 적은 자본으로 투자 가능

    Args:
        items: 전체 거래 데이터 리스트

    Returns:
        갭투자 분석 데이터
    """
    # 전세가율 분석 결과 활용
    jeonse_analysis = calculate_jeonse_ratio(items)

    if not jeonse_analysis.get("has_data"):
        return {
            "has_data": False,
            "message": jeonse_analysis.get("message", "데이터 부족"),
        }

    all_data = jeonse_analysis.get("all_data", [])

    if not all_data:
        return {"has_data": False, "message": "갭투자 분석 데이터가 없습니다."}

    # 갭 금액 구간별 분류
    gap_ranges = [
        ("1억 이하", 0, 10000),
        ("1~2억", 10000, 20000),
        ("2~3억", 20000, 30000),
        ("3~5억", 30000, 50000),
        ("5억 이상", 50000, float("inf")),
    ]

    by_gap_range = []
    for range_name, min_gap, max_gap in gap_ranges:
        range_items = [d for d in all_data if min_gap <= d["gap"] < max_gap]
        if range_items:
            by_gap_range.append(
                {
                    "gap_range": range_name,
                    "count": len(range_items),
                    "avg_gap": statistics.mean([d["gap"] for d in range_items]),
                    "avg_trade_price": statistics.mean(
                        [d["avg_trade_price"] for d in range_items]
                    ),
                    "avg_jeonse_ratio": statistics.mean(
                        [d["jeonse_ratio"] for d in range_items]
                    ),
                }
            )

    # 갭 금액 통계
    all_gaps = [d["gap"] for d in all_data]
    gap_stats = {
        "avg_gap": statistics.mean(all_gaps),
        "median_gap": statistics.median(all_gaps),
        "min_gap": min(all_gaps),
        "max_gap": max(all_gaps),
        "total_count": len(all_data),
    }

    # 소액 투자 가능 물건 (갭 1억 이하)
    small_gap_items = [d for d in all_data if d["gap"] <= 10000]

    # 월세 수익률 시뮬레이션 (가정: 전세가의 4%를 월세로 전환 시)
    # 실제로는 API 04에서 월세 데이터가 있어야 정확하지만, 시뮬레이션용
    for item in all_data:
        # 가정: 전세가의 연 4% 수익률
        estimated_annual_rent = item["avg_jeonse_price"] * 0.04
        if item["gap"] > 0:
            item["estimated_roi"] = (estimated_annual_rent / item["gap"]) * 100
        else:
            item["estimated_roi"] = 0

    # ROI 높은 순 TOP 10
    high_roi_items = sorted(
        [d for d in all_data if d["gap"] > 0],
        key=lambda x: x.get("estimated_roi", 0),
        reverse=True,
    )[:10]

    return {
        "has_data": True,
        "gap_stats": gap_stats,
        "by_gap_range": by_gap_range,
        "small_gap_items": small_gap_items[:20],  # 상위 20개
        "high_roi_items": high_roi_items,
        "low_gap_apartments": jeonse_analysis.get("low_gap_apartments", []),
    }


def detect_bargain_sales(items: List[Dict], threshold_pct: float = 10.0) -> Dict:
    """
    급매물 탐지

    정의: 동일 아파트+면적대의 최근 3개월 평균가 대비 threshold_pct% 이상 낮은 거래

    Args:
        items: 거래 데이터 리스트
        threshold_pct: 급매 판단 기준 (기본 10%)

    Returns:
        급매물 탐지 결과
    """
    # 매매 데이터만 필터링 (API 02)
    trade_items = [
        item
        for item in items
        if item.get("_api_type") == "api_02"
        and item.get("_deal_amount_numeric")
        and item.get("_area_numeric")
        and item.get("_deal_date")
    ]

    if len(trade_items) < 10:
        return {
            "has_data": False,
            "message": f"급매물 탐지를 위한 데이터가 부족합니다. (현재 {len(trade_items)}건)",
            "bargain_count": 0,
        }

    # 아파트+면적대별 그룹화
    def get_apt_key(item):
        apt_name = item.get("aptNm", "") or item.get("아파트", "")
        region = item.get("_region_name", "") or ""
        area = item.get("_area_numeric", 0)
        area_group = round(area / 5) * 5 if area else 0
        return (apt_name, region, area_group)

    # 거래일 기준 정렬
    sorted_items = sorted(
        trade_items, key=lambda x: x.get("_deal_date") or datetime.min
    )

    # 아파트별 거래 내역
    apt_trades = defaultdict(list)
    for item in sorted_items:
        key = get_apt_key(item)
        if key[0]:  # 아파트명이 있는 경우만
            apt_trades[key].append(item)

    bargain_items = []
    normal_items = []

    for apt_key, trades in apt_trades.items():
        if len(trades) < 2:
            continue

        # 각 거래에 대해 이전 거래들의 평균과 비교
        for i, current_trade in enumerate(trades):
            # 현재 거래 이전의 거래들 (최대 3개월 또는 최근 5건)
            previous_trades = trades[:i]
            if not previous_trades:
                continue

            # 최근 5건만 사용
            recent_trades = previous_trades[-5:]
            avg_price = statistics.mean(
                [t["_deal_amount_numeric"] for t in recent_trades]
            )

            current_price = current_trade["_deal_amount_numeric"]

            if avg_price > 0:
                discount_pct = ((avg_price - current_price) / avg_price) * 100

                trade_info = {
                    "apt_name": apt_key[0],
                    "region": apt_key[1],
                    "area_group": apt_key[2],
                    "current_price": current_price,
                    "avg_price": avg_price,
                    "discount_pct": discount_pct,
                    "deal_date": current_trade.get("_deal_date_str", "N/A"),
                    "floor": current_trade.get("_floor_numeric"),
                    "area": current_trade.get("_area_numeric"),
                    "is_bargain": discount_pct >= threshold_pct,
                }

                if discount_pct >= threshold_pct:
                    bargain_items.append(trade_info)
                else:
                    normal_items.append(trade_info)

    if not bargain_items and not normal_items:
        return {
            "has_data": False,
            "message": "비교 가능한 거래 데이터가 부족합니다.",
            "bargain_count": 0,
        }

    # 급매율 계산
    total_compared = len(bargain_items) + len(normal_items)
    bargain_rate = (
        (len(bargain_items) / total_compared * 100) if total_compared > 0 else 0
    )

    # 지역별 급매율
    region_bargains = defaultdict(lambda: {"bargain": 0, "total": 0})
    for item in bargain_items:
        region_bargains[item["region"]]["bargain"] += 1
        region_bargains[item["region"]]["total"] += 1
    for item in normal_items:
        region_bargains[item["region"]]["total"] += 1

    by_region = []
    for region, counts in region_bargains.items():
        if counts["total"] > 0:
            by_region.append(
                {
                    "region": region,
                    "bargain_count": counts["bargain"],
                    "total_count": counts["total"],
                    "bargain_rate": (counts["bargain"] / counts["total"]) * 100,
                }
            )

    by_region = sorted(by_region, key=lambda x: x["bargain_rate"], reverse=True)

    # 급매물 리스트 (할인율 높은 순)
    bargain_items = sorted(bargain_items, key=lambda x: x["discount_pct"], reverse=True)

    # 통계
    if bargain_items:
        discount_pcts = [b["discount_pct"] for b in bargain_items]
        stats = {
            "total_trades": len(trade_items),
            "compared_trades": total_compared,
            "bargain_count": len(bargain_items),
            "bargain_rate": bargain_rate,
            "avg_discount": statistics.mean(discount_pcts),
            "max_discount": max(discount_pcts),
            "threshold_pct": threshold_pct,
        }
    else:
        stats = {
            "total_trades": len(trade_items),
            "compared_trades": total_compared,
            "bargain_count": 0,
            "bargain_rate": 0,
            "avg_discount": 0,
            "max_discount": 0,
            "threshold_pct": threshold_pct,
        }

    return {
        "has_data": True,
        "stats": stats,
        "by_region": by_region,
        "bargain_items": bargain_items[:50],  # 상위 50개
        "recent_bargains": [
            b for b in bargain_items if b.get("deal_date", "") >= "2024-01"
        ][:20],
    }


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


def analyze_rent_vs_jeonse(items: List[Dict]) -> Dict:
    """
    월세 전환율 & 월세/전세 선호도 분석 (DA.md #2)

    분석 항목:
    - 월세 vs 전세 거래 비율 (지역별, 면적별)
    - 월세 전환율: 월세(만원) × 12 / 보증금(만원) × 100 (연 환산)
    - 층수별 월세/전세 선호도 패턴

    Args:
        items: 거래 데이터 리스트 (API 04 전월세 데이터 포함)

    Returns:
        월세/전세 분석 데이터
    """
    # API 04 (전월세) 데이터만 필터링
    rent_items = [item for item in items if item.get("_api_type") == "api_04"]

    if not rent_items:
        return {
            "has_data": False,
            "message": "전월세 데이터가 없습니다.",
            "total_count": 0,
        }

    # 월세/전세 분류
    jeonse_items = []  # 전세 (월세 = 0)
    wolse_items = []  # 월세 (월세 > 0)

    for item in rent_items:
        monthly_rent = item.get("monthlyRent", "") or item.get("월세금액", "") or "0"
        try:
            rent_val = int(str(monthly_rent).replace(",", "").strip() or "0")
        except (ValueError, TypeError):
            rent_val = 0

        # 보증금 추출
        deposit = item.get("deposit", "") or item.get("보증금액", "") or "0"
        try:
            deposit_val = float(str(deposit).replace(",", "").strip() or "0")
        except (ValueError, TypeError):
            deposit_val = 0

        item["_monthly_rent_numeric"] = rent_val
        item["_deposit_numeric"] = deposit_val

        if rent_val == 0:
            jeonse_items.append(item)
        else:
            wolse_items.append(item)

    total_count = len(rent_items)
    jeonse_count = len(jeonse_items)
    wolse_count = len(wolse_items)

    # 기본 비율 통계
    overall_stats = {
        "total_count": total_count,
        "jeonse_count": jeonse_count,
        "wolse_count": wolse_count,
        "jeonse_ratio": (jeonse_count / total_count * 100) if total_count > 0 else 0,
        "wolse_ratio": (wolse_count / total_count * 100) if total_count > 0 else 0,
    }

    # 월세 전환율 계산 (월세 데이터에 대해서만)
    # 연 환산 월세 전환율 = (월세 × 12) / 보증금 × 100
    conversion_rates = []
    for item in wolse_items:
        monthly = item["_monthly_rent_numeric"]
        deposit = item["_deposit_numeric"]
        if deposit > 0 and monthly > 0:
            annual_rate = (monthly * 12) / deposit * 100
            item["_conversion_rate"] = annual_rate
            conversion_rates.append(annual_rate)

    if conversion_rates:
        overall_stats["avg_conversion_rate"] = statistics.mean(conversion_rates)
        overall_stats["median_conversion_rate"] = statistics.median(conversion_rates)
        overall_stats["min_conversion_rate"] = min(conversion_rates)
        overall_stats["max_conversion_rate"] = max(conversion_rates)
    else:
        overall_stats["avg_conversion_rate"] = 0
        overall_stats["median_conversion_rate"] = 0
        overall_stats["min_conversion_rate"] = 0
        overall_stats["max_conversion_rate"] = 0

    # 지역별 월세/전세 비율
    region_data = defaultdict(lambda: {"jeonse": 0, "wolse": 0, "conversion_rates": []})

    for item in jeonse_items:
        region = item.get("_region_name") or item.get("umdNm", "") or "미지정"
        region_data[region]["jeonse"] += 1

    for item in wolse_items:
        region = item.get("_region_name") or item.get("umdNm", "") or "미지정"
        region_data[region]["wolse"] += 1
        if item.get("_conversion_rate"):
            region_data[region]["conversion_rates"].append(item["_conversion_rate"])

    by_region = []
    for region in sorted(region_data.keys()):
        data = region_data[region]
        total = data["jeonse"] + data["wolse"]
        by_region.append(
            {
                "region": region,
                "jeonse_count": data["jeonse"],
                "wolse_count": data["wolse"],
                "total_count": total,
                "jeonse_ratio": (data["jeonse"] / total * 100) if total > 0 else 0,
                "wolse_ratio": (data["wolse"] / total * 100) if total > 0 else 0,
                "avg_conversion_rate": statistics.mean(data["conversion_rates"])
                if data["conversion_rates"]
                else 0,
            }
        )

    # 월세 비율 높은 순 정렬
    by_region = sorted(by_region, key=lambda x: x["wolse_ratio"], reverse=True)

    # 면적대별 월세/전세 비율
    area_ranges = [
        ("소형 (60㎡ 미만)", 0, 60),
        ("중소형 (60-85㎡)", 60, 85),
        ("중형 (85-102㎡)", 85, 102),
        ("중대형 (102-135㎡)", 102, 135),
        ("대형 (135㎡ 이상)", 135, float("inf")),
    ]

    by_area = []
    for range_name, min_area, max_area in area_ranges:
        jeonse_in_range = [
            item
            for item in jeonse_items
            if item.get("_area_numeric") is not None
            and min_area <= item["_area_numeric"] < max_area
        ]
        wolse_in_range = [
            item
            for item in wolse_items
            if item.get("_area_numeric") is not None
            and min_area <= item["_area_numeric"] < max_area
        ]
        total = len(jeonse_in_range) + len(wolse_in_range)
        if total > 0:
            conv_rates = [
                item["_conversion_rate"]
                for item in wolse_in_range
                if item.get("_conversion_rate")
            ]
            by_area.append(
                {
                    "area_range": range_name,
                    "jeonse_count": len(jeonse_in_range),
                    "wolse_count": len(wolse_in_range),
                    "total_count": total,
                    "jeonse_ratio": len(jeonse_in_range) / total * 100,
                    "wolse_ratio": len(wolse_in_range) / total * 100,
                    "avg_conversion_rate": statistics.mean(conv_rates)
                    if conv_rates
                    else 0,
                }
            )

    # 층수별 월세/전세 선호도
    floor_data = defaultdict(lambda: {"jeonse": 0, "wolse": 0})

    def get_floor_category(floor):
        if floor is None:
            return None
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

    for item in jeonse_items:
        floor_cat = get_floor_category(item.get("_floor_numeric"))
        if floor_cat:
            floor_data[floor_cat]["jeonse"] += 1

    for item in wolse_items:
        floor_cat = get_floor_category(item.get("_floor_numeric"))
        if floor_cat:
            floor_data[floor_cat]["wolse"] += 1

    floor_order = [
        "지하/반지하",
        "저층 (1-5층)",
        "중저층 (6-10층)",
        "중층 (11-15층)",
        "중고층 (16-20층)",
        "고층 (21층+)",
    ]
    by_floor = []
    for floor_cat in floor_order:
        if floor_cat in floor_data:
            data = floor_data[floor_cat]
            total = data["jeonse"] + data["wolse"]
            if total > 0:
                by_floor.append(
                    {
                        "floor_category": floor_cat,
                        "jeonse_count": data["jeonse"],
                        "wolse_count": data["wolse"],
                        "total_count": total,
                        "jeonse_ratio": data["jeonse"] / total * 100,
                        "wolse_ratio": data["wolse"] / total * 100,
                    }
                )

    # 보증금 구간별 월세 전환율
    deposit_ranges = [
        ("5천만원 이하", 0, 5000),
        ("5천~1억", 5000, 10000),
        ("1억~2억", 10000, 20000),
        ("2억~3억", 20000, 30000),
        ("3억 이상", 30000, float("inf")),
    ]

    by_deposit = []
    for range_name, min_dep, max_dep in deposit_ranges:
        wolse_in_range = [
            item
            for item in wolse_items
            if item.get("_deposit_numeric") is not None
            and min_dep <= item["_deposit_numeric"] < max_dep
            and item.get("_conversion_rate")
        ]
        if wolse_in_range:
            conv_rates = [item["_conversion_rate"] for item in wolse_in_range]
            by_deposit.append(
                {
                    "deposit_range": range_name,
                    "count": len(wolse_in_range),
                    "avg_conversion_rate": statistics.mean(conv_rates),
                    "median_conversion_rate": statistics.median(conv_rates),
                    "avg_monthly_rent": statistics.mean(
                        [item["_monthly_rent_numeric"] for item in wolse_in_range]
                    ),
                    "avg_deposit": statistics.mean(
                        [item["_deposit_numeric"] for item in wolse_in_range]
                    ),
                }
            )

    # 고전환율 물건 TOP 10 (투자 수익률 높은 월세 물건)
    high_conversion_items = sorted(
        [item for item in wolse_items if item.get("_conversion_rate")],
        key=lambda x: x["_conversion_rate"],
        reverse=True,
    )[:10]

    high_conversion_list = []
    for item in high_conversion_items:
        high_conversion_list.append(
            {
                "apt_name": item.get("aptNm", "") or item.get("아파트", "N/A"),
                "region": item.get("_region_name") or item.get("umdNm", "N/A"),
                "deposit": item["_deposit_numeric"],
                "monthly_rent": item["_monthly_rent_numeric"],
                "conversion_rate": item["_conversion_rate"],
                "area": item.get("_area_numeric"),
                "floor": item.get("_floor_numeric"),
            }
        )

    return {
        "has_data": True,
        "stats": overall_stats,
        "by_region": by_region,
        "by_area": by_area,
        "by_floor": by_floor,
        "by_deposit": by_deposit,
        "high_conversion_items": high_conversion_list,
    }


def analyze_dealing_type(items: List[Dict]) -> Dict:
    """
    거래유형(dealingGbn) 분석 (DA.md #6)

    분석 항목:
    - 중개거래 vs 직거래 비율
    - 거래유형별 평균가격 차이
    - 지역별 직거래 비율
    - 가격대별 거래유형 분포

    Args:
        items: 거래 데이터 리스트 (API 02 매매 데이터)

    Returns:
        거래유형 분석 데이터
    """
    trade_items = [
        item
        for item in items
        if item.get("_api_type") == "api_02"
        and item.get("dealingGbn")
        and str(item.get("dealingGbn", "")).strip()
    ]

    if not trade_items:
        return {
            "has_data": False,
            "message": "거래유형 데이터가 없습니다. API 02(매매) 데이터가 필요합니다.",
            "total_count": 0,
        }

    broker_items = []
    direct_items = []
    other_items = []

    for item in trade_items:
        dealing_type = str(item.get("dealingGbn", "")).strip()
        if "중개" in dealing_type:
            item["_dealing_category"] = "중개거래"
            broker_items.append(item)
        elif "직거래" in dealing_type:
            item["_dealing_category"] = "직거래"
            direct_items.append(item)
        else:
            item["_dealing_category"] = dealing_type or "기타"
            other_items.append(item)

    total_count = len(trade_items)
    broker_count = len(broker_items)
    direct_count = len(direct_items)

    overall_stats = {
        "total_count": total_count,
        "broker_count": broker_count,
        "direct_count": direct_count,
        "other_count": len(other_items),
        "broker_ratio": (broker_count / total_count * 100) if total_count > 0 else 0,
        "direct_ratio": (direct_count / total_count * 100) if total_count > 0 else 0,
    }

    broker_prices = [
        item["_deal_amount_numeric"]
        for item in broker_items
        if item.get("_deal_amount_numeric")
    ]
    direct_prices = [
        item["_deal_amount_numeric"]
        for item in direct_items
        if item.get("_deal_amount_numeric")
    ]

    if broker_prices:
        overall_stats["broker_avg_price"] = statistics.mean(broker_prices)
        overall_stats["broker_median_price"] = statistics.median(broker_prices)
    else:
        overall_stats["broker_avg_price"] = 0
        overall_stats["broker_median_price"] = 0

    if direct_prices:
        overall_stats["direct_avg_price"] = statistics.mean(direct_prices)
        overall_stats["direct_median_price"] = statistics.median(direct_prices)
    else:
        overall_stats["direct_avg_price"] = 0
        overall_stats["direct_median_price"] = 0

    if broker_prices and direct_prices:
        price_diff = (
            overall_stats["broker_avg_price"] - overall_stats["direct_avg_price"]
        )
        price_diff_pct = (
            (price_diff / overall_stats["broker_avg_price"] * 100)
            if overall_stats["broker_avg_price"] > 0
            else 0
        )
        overall_stats["price_diff"] = price_diff
        overall_stats["price_diff_pct"] = price_diff_pct
    else:
        overall_stats["price_diff"] = 0
        overall_stats["price_diff_pct"] = 0

    region_data = defaultdict(
        lambda: {"broker": 0, "direct": 0, "broker_prices": [], "direct_prices": []}
    )

    for item in broker_items:
        region = item.get("_region_name") or item.get("umdNm", "") or "미지정"
        region_data[region]["broker"] += 1
        if item.get("_deal_amount_numeric"):
            region_data[region]["broker_prices"].append(item["_deal_amount_numeric"])

    for item in direct_items:
        region = item.get("_region_name") or item.get("umdNm", "") or "미지정"
        region_data[region]["direct"] += 1
        if item.get("_deal_amount_numeric"):
            region_data[region]["direct_prices"].append(item["_deal_amount_numeric"])

    by_region = []
    for region in sorted(region_data.keys()):
        data = region_data[region]
        total = data["broker"] + data["direct"]
        if total > 0:
            by_region.append(
                {
                    "region": region,
                    "broker_count": data["broker"],
                    "direct_count": data["direct"],
                    "total_count": total,
                    "direct_ratio": (data["direct"] / total * 100),
                    "broker_avg_price": statistics.mean(data["broker_prices"])
                    if data["broker_prices"]
                    else 0,
                    "direct_avg_price": statistics.mean(data["direct_prices"])
                    if data["direct_prices"]
                    else 0,
                }
            )

    by_region = sorted(by_region, key=lambda x: x["direct_ratio"], reverse=True)

    price_ranges = [
        ("3억 이하", 0, 30000),
        ("3~5억", 30000, 50000),
        ("5~10억", 50000, 100000),
        ("10~15억", 100000, 150000),
        ("15억 이상", 150000, float("inf")),
    ]

    by_price_range = []
    for range_name, min_price, max_price in price_ranges:
        broker_in_range = [
            item
            for item in broker_items
            if item.get("_deal_amount_numeric")
            and min_price <= item["_deal_amount_numeric"] < max_price
        ]
        direct_in_range = [
            item
            for item in direct_items
            if item.get("_deal_amount_numeric")
            and min_price <= item["_deal_amount_numeric"] < max_price
        ]
        total = len(broker_in_range) + len(direct_in_range)
        if total > 0:
            by_price_range.append(
                {
                    "price_range": range_name,
                    "broker_count": len(broker_in_range),
                    "direct_count": len(direct_in_range),
                    "total_count": total,
                    "broker_ratio": len(broker_in_range) / total * 100,
                    "direct_ratio": len(direct_in_range) / total * 100,
                }
            )

    monthly_data = defaultdict(lambda: {"broker": 0, "direct": 0})

    for item in broker_items:
        ym = item.get("_deal_year_month")
        if ym:
            monthly_data[ym]["broker"] += 1

    for item in direct_items:
        ym = item.get("_deal_year_month")
        if ym:
            monthly_data[ym]["direct"] += 1

    by_month = []
    for ym in sorted(monthly_data.keys()):
        data = monthly_data[ym]
        total = data["broker"] + data["direct"]
        if total > 0:
            by_month.append(
                {
                    "year_month": ym,
                    "broker_count": data["broker"],
                    "direct_count": data["direct"],
                    "total_count": total,
                    "direct_ratio": data["direct"] / total * 100,
                }
            )

    return {
        "has_data": True,
        "stats": overall_stats,
        "by_region": by_region,
        "by_price_range": by_price_range,
        "by_month": by_month,
    }


def analyze_buyer_seller_type(items: List[Dict]) -> Dict:
    """
    매수자/매도자 유형(buyerGbn/slerGbn) 분석 (DA.md #7)

    분석 항목:
    - 개인 vs 법인 거래 비율
    - 법인 매수/매도 추이
    - 지역별 법인 거래 비율
    - 법인 거래 평균가 vs 개인 거래 평균가

    Args:
        items: 거래 데이터 리스트 (API 02 매매 데이터)

    Returns:
        매수자/매도자 유형 분석 데이터
    """
    trade_items = [item for item in items if item.get("_api_type") == "api_02"]

    if not trade_items:
        return {
            "has_data": False,
            "message": "매매 데이터가 없습니다. API 02(매매) 데이터가 필요합니다.",
            "total_count": 0,
        }

    def categorize_type(type_str):
        if not type_str or str(type_str).strip() == "":
            return "미공개"
        type_str = str(type_str).strip()
        if "법인" in type_str:
            return "법인"
        elif "개인" in type_str:
            return "개인"
        else:
            return "미공개"

    buyer_stats = defaultdict(int)
    seller_stats = defaultdict(int)
    buyer_prices = defaultdict(list)
    seller_prices = defaultdict(list)

    for item in trade_items:
        buyer_type = categorize_type(item.get("buyerGbn", ""))
        seller_type = categorize_type(item.get("slerGbn", ""))

        buyer_stats[buyer_type] += 1
        seller_stats[seller_type] += 1

        price = item.get("_deal_amount_numeric")
        if price:
            buyer_prices[buyer_type].append(price)
            seller_prices[seller_type].append(price)

    total_count = len(trade_items)

    overall_stats = {
        "total_count": total_count,
        "buyer_types": dict(buyer_stats),
        "seller_types": dict(seller_stats),
    }

    for buyer_type in ["법인", "개인", "미공개"]:
        count = buyer_stats.get(buyer_type, 0)
        overall_stats[f"buyer_{buyer_type}_count"] = count
        overall_stats[f"buyer_{buyer_type}_ratio"] = (
            (count / total_count * 100) if total_count > 0 else 0
        )
        prices = buyer_prices.get(buyer_type, [])
        overall_stats[f"buyer_{buyer_type}_avg_price"] = (
            statistics.mean(prices) if prices else 0
        )

    for seller_type in ["법인", "개인", "미공개"]:
        count = seller_stats.get(seller_type, 0)
        overall_stats[f"seller_{seller_type}_count"] = count
        overall_stats[f"seller_{seller_type}_ratio"] = (
            (count / total_count * 100) if total_count > 0 else 0
        )
        prices = seller_prices.get(seller_type, [])
        overall_stats[f"seller_{seller_type}_avg_price"] = (
            statistics.mean(prices) if prices else 0
        )

    region_data = defaultdict(
        lambda: {
            "buyer_법인": 0,
            "buyer_개인": 0,
            "buyer_미공개": 0,
            "seller_법인": 0,
            "seller_개인": 0,
            "seller_미공개": 0,
            "total": 0,
        }
    )

    for item in trade_items:
        region = item.get("_region_name") or item.get("umdNm", "") or "미지정"
        buyer_type = categorize_type(item.get("buyerGbn", ""))
        seller_type = categorize_type(item.get("slerGbn", ""))

        region_data[region][f"buyer_{buyer_type}"] += 1
        region_data[region][f"seller_{seller_type}"] += 1
        region_data[region]["total"] += 1

    by_region = []
    for region in sorted(region_data.keys()):
        data = region_data[region]
        if data["total"] > 0:
            by_region.append(
                {
                    "region": region,
                    "total_count": data["total"],
                    "buyer_법인_count": data["buyer_법인"],
                    "buyer_법인_ratio": data["buyer_법인"] / data["total"] * 100,
                    "seller_법인_count": data["seller_법인"],
                    "seller_법인_ratio": data["seller_법인"] / data["total"] * 100,
                }
            )

    by_region = sorted(by_region, key=lambda x: x["buyer_법인_ratio"], reverse=True)

    monthly_data = defaultdict(
        lambda: {
            "buyer_법인": 0,
            "buyer_개인": 0,
            "buyer_미공개": 0,
            "seller_법인": 0,
            "seller_개인": 0,
            "seller_미공개": 0,
            "total": 0,
        }
    )

    for item in trade_items:
        ym = item.get("_deal_year_month")
        if ym:
            buyer_type = categorize_type(item.get("buyerGbn", ""))
            seller_type = categorize_type(item.get("slerGbn", ""))
            monthly_data[ym][f"buyer_{buyer_type}"] += 1
            monthly_data[ym][f"seller_{seller_type}"] += 1
            monthly_data[ym]["total"] += 1

    by_month = []
    for ym in sorted(monthly_data.keys()):
        data = monthly_data[ym]
        if data["total"] > 0:
            by_month.append(
                {
                    "year_month": ym,
                    "total_count": data["total"],
                    "buyer_법인_count": data["buyer_법인"],
                    "buyer_법인_ratio": data["buyer_법인"] / data["total"] * 100,
                    "seller_법인_count": data["seller_법인"],
                    "seller_법인_ratio": data["seller_법인"] / data["total"] * 100,
                }
            )

    return {
        "has_data": True,
        "stats": overall_stats,
        "by_region": by_region,
        "by_month": by_month,
    }


def analyze_cancelled_deals(items: List[Dict]) -> Dict:
    """
    취소거래(cdealDay/cdealType) 분석 (DA.md #8)

    분석 항목:
    - 취소거래 비율 추이
    - 취소유형별 분석
    - 지역별 취소율
    - 가격대별 취소율

    Args:
        items: 거래 데이터 리스트 (API 02 매매 데이터)

    Returns:
        취소거래 분석 데이터
    """
    trade_items = [item for item in items if item.get("_api_type") == "api_02"]

    if not trade_items:
        return {
            "has_data": False,
            "message": "매매 데이터가 없습니다. API 02(매매) 데이터가 필요합니다.",
            "total_count": 0,
        }

    cancelled_items = []
    normal_items = []

    for item in trade_items:
        cdeal_day = item.get("cdealDay", "")
        cdeal_type = item.get("cdealType", "")

        is_cancelled = bool(cdeal_day and str(cdeal_day).strip())

        if is_cancelled:
            item["_cancel_type"] = (
                str(cdeal_type).strip()
                if cdeal_type and str(cdeal_type).strip()
                else "유형미상"
            )
            item["_cancel_day"] = str(cdeal_day).strip()
            cancelled_items.append(item)
        else:
            normal_items.append(item)

    total_count = len(trade_items)
    cancelled_count = len(cancelled_items)
    normal_count = len(normal_items)

    overall_stats = {
        "total_count": total_count,
        "cancelled_count": cancelled_count,
        "normal_count": normal_count,
        "cancel_ratio": (cancelled_count / total_count * 100) if total_count > 0 else 0,
    }

    cancel_types = defaultdict(int)
    for item in cancelled_items:
        cancel_types[item["_cancel_type"]] += 1

    overall_stats["cancel_types"] = dict(cancel_types)

    cancelled_prices = [
        item["_deal_amount_numeric"]
        for item in cancelled_items
        if item.get("_deal_amount_numeric")
    ]
    normal_prices = [
        item["_deal_amount_numeric"]
        for item in normal_items
        if item.get("_deal_amount_numeric")
    ]

    if cancelled_prices:
        overall_stats["cancelled_avg_price"] = statistics.mean(cancelled_prices)
    else:
        overall_stats["cancelled_avg_price"] = 0

    if normal_prices:
        overall_stats["normal_avg_price"] = statistics.mean(normal_prices)
    else:
        overall_stats["normal_avg_price"] = 0

    region_data = defaultdict(lambda: {"cancelled": 0, "normal": 0})

    for item in cancelled_items:
        region = item.get("_region_name") or item.get("umdNm", "") or "미지정"
        region_data[region]["cancelled"] += 1

    for item in normal_items:
        region = item.get("_region_name") or item.get("umdNm", "") or "미지정"
        region_data[region]["normal"] += 1

    by_region = []
    for region in sorted(region_data.keys()):
        data = region_data[region]
        total = data["cancelled"] + data["normal"]
        if total > 0:
            by_region.append(
                {
                    "region": region,
                    "cancelled_count": data["cancelled"],
                    "normal_count": data["normal"],
                    "total_count": total,
                    "cancel_ratio": data["cancelled"] / total * 100,
                }
            )

    by_region = sorted(by_region, key=lambda x: x["cancel_ratio"], reverse=True)

    price_ranges = [
        ("3억 이하", 0, 30000),
        ("3~5억", 30000, 50000),
        ("5~10억", 50000, 100000),
        ("10~15억", 100000, 150000),
        ("15억 이상", 150000, float("inf")),
    ]

    by_price_range = []
    for range_name, min_price, max_price in price_ranges:
        cancelled_in_range = [
            item
            for item in cancelled_items
            if item.get("_deal_amount_numeric")
            and min_price <= item["_deal_amount_numeric"] < max_price
        ]
        normal_in_range = [
            item
            for item in normal_items
            if item.get("_deal_amount_numeric")
            and min_price <= item["_deal_amount_numeric"] < max_price
        ]
        total = len(cancelled_in_range) + len(normal_in_range)
        if total > 0:
            by_price_range.append(
                {
                    "price_range": range_name,
                    "cancelled_count": len(cancelled_in_range),
                    "normal_count": len(normal_in_range),
                    "total_count": total,
                    "cancel_ratio": len(cancelled_in_range) / total * 100,
                }
            )

    monthly_data = defaultdict(lambda: {"cancelled": 0, "normal": 0})

    for item in cancelled_items:
        ym = item.get("_deal_year_month")
        if ym:
            monthly_data[ym]["cancelled"] += 1

    for item in normal_items:
        ym = item.get("_deal_year_month")
        if ym:
            monthly_data[ym]["normal"] += 1

    by_month = []
    for ym in sorted(monthly_data.keys()):
        data = monthly_data[ym]
        total = data["cancelled"] + data["normal"]
        if total > 0:
            by_month.append(
                {
                    "year_month": ym,
                    "cancelled_count": data["cancelled"],
                    "normal_count": data["normal"],
                    "total_count": total,
                    "cancel_ratio": data["cancelled"] / total * 100,
                }
            )

    return {
        "has_data": True,
        "stats": overall_stats,
        "by_region": by_region,
        "by_price_range": by_price_range,
        "by_month": by_month,
        "cancelled_items": [
            {
                "apt_name": item.get("aptNm", "") or item.get("아파트", "N/A"),
                "region": item.get("_region_name") or item.get("umdNm", "N/A"),
                "price": item.get("_deal_amount_numeric"),
                "cancel_type": item["_cancel_type"],
                "cancel_day": item["_cancel_day"],
                "deal_date": item.get("_deal_date_str", "N/A"),
            }
            for item in cancelled_items[:50]
        ],
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


def summarize_period(items: List[Dict], start_date: datetime, end_date: datetime) -> Dict:
    """
    선택한 기간의 핵심 지표 요약

    Args:
        items: 거래 데이터 리스트
        start_date: 시작일 (datetime)
        end_date: 종료일 (datetime)

    Returns:
        기간 요약 정보
    """
    if start_date > end_date:
        return {"has_data": False, "items": []}

    period_items = []
    for item in items:
        deal_date = item.get("_deal_date")
        if deal_date is None:
            continue
        if start_date <= deal_date <= end_date:
            period_items.append(item)

    if not period_items:
        return {"has_data": False, "items": []}

    basic_stats = calculate_basic_stats(period_items)

    prices = [
        item.get("_deal_amount_numeric")
        for item in period_items
        if item.get("_deal_amount_numeric") is not None
    ]

    price_std = statistics.stdev(prices) if len(prices) > 1 else 0

    ppa_values = []
    for item in period_items:
        price = item.get("_deal_amount_numeric")
        area = item.get("_area_numeric")
        if price is not None and area and area > 0:
            ppa_values.append(price / area)

    ppa_avg = statistics.mean(ppa_values) if ppa_values else 0
    ppa_median = statistics.median(ppa_values) if ppa_values else 0
    ppa_std = statistics.stdev(ppa_values) if len(ppa_values) > 1 else 0

    region_data = defaultdict(lambda: {"count": 0, "prices": []})
    api_counts = defaultdict(int)
    months = set()

    for item in period_items:
        region = item.get("_region_name", "미지정")
        region_data[region]["count"] += 1
        price = item.get("_deal_amount_numeric")
        if price is not None:
            region_data[region]["prices"].append(price)

        api_type = item.get("_api_type") or "unknown"
        api_counts[api_type] += 1

        ym = item.get("_deal_year_month")
        if ym:
            months.add(ym)

    top_regions = []
    for region, data in region_data.items():
        top_regions.append(
            {
                "region": region,
                "count": data["count"],
                "avg_price": statistics.mean(data["prices"])
                if data["prices"]
                else 0,
            }
        )

    top_regions = sorted(top_regions, key=lambda x: x["count"], reverse=True)

    api_mix = [
        {"api_type": api_type, "count": count}
        for api_type, count in sorted(api_counts.items(), key=lambda x: x[1], reverse=True)
    ]

    return {
        "has_data": True,
        "start_date": start_date,
        "end_date": end_date,
        "items": period_items,
        "count": len(period_items),
        "avg_price": basic_stats["avg_price"],
        "median_price": basic_stats["median_price"],
        "max_price": basic_stats["max_price"],
        "min_price": basic_stats["min_price"],
        "avg_area": basic_stats["avg_area"],
        "price_std": price_std,
        "avg_price_per_area": ppa_avg,
        "median_price_per_area": ppa_median,
        "price_per_area_std": ppa_std,
        "months": sorted(months),
        "top_regions": top_regions[:5],
        "api_mix": api_mix,
    }


def build_baseline_summary(
    items: List[Dict], start_date: datetime, end_date: datetime
) -> Dict:
    """
    선택 구간과 동일 길이의 직전 기간을 기준선으로 요약
    """
    if start_date > end_date:
        return {"has_data": False, "items": []}

    delta = end_date - start_date
    baseline_end = start_date - timedelta(days=1)
    baseline_start = baseline_end - delta

    summary = summarize_period(items, baseline_start, baseline_end)
    if summary.get("has_data"):
        summary["baseline_start"] = baseline_start
        summary["baseline_end"] = baseline_end
    return summary


def compare_periods(current: Dict, baseline: Dict) -> Dict:
    """
    기간 비교 지표 계산
    """
    if not current.get("has_data") or not baseline.get("has_data"):
        return {"has_data": False}

    def safe_pct_change(curr: float, prev: float):
        if prev is None or prev == 0:
            return None
        return ((curr - prev) / prev) * 100

    return {
        "has_data": True,
        "price_change_pct": safe_pct_change(
            current.get("avg_price"), baseline.get("avg_price")
        ),
        "median_change_pct": safe_pct_change(
            current.get("median_price"), baseline.get("median_price")
        ),
        "count_change_pct": safe_pct_change(
            current.get("count"), baseline.get("count")
        ),
        "ppa_change_pct": safe_pct_change(
            current.get("avg_price_per_area"), baseline.get("avg_price_per_area")
        ),
    }


def detect_market_signals(current: Dict, baseline: Dict, comparison: Dict) -> List[Dict]:
    """
    단순 휴리스틱으로 시장 이벤트 신호 도출
    """
    if not current.get("has_data"):
        return []

    signals = []

    price_change = comparison.get("price_change_pct") if comparison else None
    count_change = comparison.get("count_change_pct") if comparison else None
    ppa_change = comparison.get("ppa_change_pct") if comparison else None

    if price_change is not None:
        if price_change >= 10:
            signals.append(
                {
                    "level": "strong",
                    "title": "가격 급등 신호",
                    "detail": f"평균 거래가격이 기준선 대비 {price_change:+.1f}% 상승.",
                }
            )
        elif price_change <= -10:
            signals.append(
                {
                    "level": "strong",
                    "title": "가격 급락 신호",
                    "detail": f"평균 거래가격이 기준선 대비 {price_change:+.1f}% 하락.",
                }
            )
        elif abs(price_change) >= 5:
            signals.append(
                {
                    "level": "moderate",
                    "title": "가격 변동 확대",
                    "detail": f"평균 거래가격이 기준선 대비 {price_change:+.1f}% 변화.",
                }
            )

    if count_change is not None:
        if count_change >= 50:
            signals.append(
                {
                    "level": "strong",
                    "title": "거래 급증",
                    "detail": f"거래건수가 기준선 대비 {count_change:+.1f}% 증가.",
                }
            )
        elif count_change <= -50:
            signals.append(
                {
                    "level": "strong",
                    "title": "거래 급감",
                    "detail": f"거래건수가 기준선 대비 {count_change:+.1f}% 감소.",
                }
            )
        elif abs(count_change) >= 20:
            signals.append(
                {
                    "level": "moderate",
                    "title": "거래량 변동",
                    "detail": f"거래건수가 기준선 대비 {count_change:+.1f}% 변화.",
                }
            )

    if price_change is not None and count_change is not None:
        if price_change >= 5 and count_change >= 20:
            signals.append(
                {
                    "level": "strong",
                    "title": "상승 + 거래 확대",
                    "detail": "가격 상승과 거래 증가가 동시에 나타남 (활황 국면 가능).",
                }
            )
        elif price_change <= -5 and count_change <= -20:
            signals.append(
                {
                    "level": "strong",
                    "title": "하락 + 거래 위축",
                    "detail": "가격 하락과 거래 감소가 동시에 나타남 (거래절벽 신호).",
                }
            )

    if ppa_change is not None and abs(ppa_change) >= 8:
        signals.append(
            {
                "level": "moderate",
                "title": "평당가 변화",
                "detail": f"㎡당 가격이 기준선 대비 {ppa_change:+.1f}% 변화.",
            }
        )

    avg_price = current.get("avg_price") or 0
    price_std = current.get("price_std") or 0
    if avg_price > 0 and (price_std / avg_price) >= 0.25:
        signals.append(
            {
                "level": "moderate",
                "title": "가격 변동성 확대",
                "detail": "기간 내 가격 분산이 높아 변동성이 큼.",
            }
        )

    top_regions = current.get("top_regions") or []
    if top_regions and current.get("count"):
        share = top_regions[0]["count"] / current["count"]
        if share >= 0.5:
            signals.append(
                {
                    "level": "moderate",
                    "title": "특정 지역 쏠림",
                    "detail": f"거래의 {share:.0%}가 상위 1개 지역에 집중.",
                }
            )

    return signals
