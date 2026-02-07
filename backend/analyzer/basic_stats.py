"""
기본 통계 분석 모듈
거래 데이터의 기본 통계 및 가격 추이 분석
"""
from typing import List, Dict
from collections import defaultdict
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
        year_month = item.get("_year_month")
        price = item.get("_deal_amount_numeric")

        if year_month and price is not None:
            monthly_data[year_month]["prices"].append(price)
            monthly_data[year_month]["count"] += 1

    # 월별 평균 가격 계산
    trend_data = {}
    for year_month in sorted(monthly_data.keys()):
        prices = monthly_data[year_month]["prices"]
        trend_data[year_month] = {
            "count": monthly_data[year_month]["count"],
            "avg_price": statistics.mean(prices) if prices else 0,
            "max_price": max(prices) if prices else 0,
            "min_price": min(prices) if prices else 0,
            "median_price": statistics.median(prices) if prices else 0,
        }

    return {
        "monthly_trend": trend_data,
        "total_months": len(trend_data),
    }
