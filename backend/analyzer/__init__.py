"""
Analyzer Module - Facade Pattern

This module provides a unified interface to all analyzer functions.
All imports are re-exported to maintain backward compatibility.

Zero Breaking Changes: All existing code using `from backend.analyzer import func` 
will continue to work exactly as before.
"""

# Basic Statistics (2 functions)
from .basic_stats import (
    calculate_basic_stats,
    calculate_price_trend,
)

# Segmentation Analysis (6 functions)
from .segmentation import (
    analyze_by_area,
    analyze_by_floor,
    analyze_by_build_year,
    analyze_by_region,
    analyze_by_apartment,
    get_apartment_detail,
)

# Investment Analysis (3 functions)
from .investment import (
    calculate_jeonse_ratio,
    analyze_gap_investment,
    detect_bargain_sales,
)

# Premium Analysis (4 functions)
from .premium_analysis import (
    calculate_price_per_area,
    analyze_price_per_area_trend,
    analyze_floor_premium,
    analyze_building_age_premium,
)

# Market Signals (8 functions)
from .market_signals import (
    analyze_rent_vs_jeonse,
    analyze_dealing_type,
    analyze_buyer_seller_type,
    analyze_cancelled_deals,
    summarize_period,
    build_baseline_summary,
    compare_periods,
    detect_market_signals,
)

# Export all functions for easy import
__all__ = [
    # Basic Statistics
    "calculate_basic_stats",
    "calculate_price_trend",
    # Segmentation
    "analyze_by_area",
    "analyze_by_floor",
    "analyze_by_build_year",
    "analyze_by_region",
    "analyze_by_apartment",
    "get_apartment_detail",
    # Investment
    "calculate_jeonse_ratio",
    "analyze_gap_investment",
    "detect_bargain_sales",
    # Premium
    "calculate_price_per_area",
    "analyze_price_per_area_trend",
    "analyze_floor_premium",
    "analyze_building_age_premium",
    # Market Signals
    "analyze_rent_vs_jeonse",
    "analyze_dealing_type",
    "analyze_buyer_seller_type",
    "analyze_cancelled_deals",
    "summarize_period",
    "build_baseline_summary",
    "compare_periods",
    "detect_market_signals",
]
