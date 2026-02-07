"""
시장 신호 분석 모듈
전월세, 거래유형, 매수자/매도자 유형, 취소거래, 기간 비교 등
"""
from typing import List, Dict
from collections import defaultdict
from datetime import datetime, timedelta
import statistics


# Import basic stats functions for use in summarize_period
from .basic_stats import calculate_basic_stats


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
