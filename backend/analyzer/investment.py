"""
투자 분석 모듈
전세가율, 갭투자, 급매물 탐지 등
"""
from typing import List, Dict
from collections import defaultdict
from datetime import datetime
import statistics


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
