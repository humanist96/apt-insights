"""
Analyzer Service
Wraps backend.analyzer functions and provides API-friendly data processing
"""
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import structlog

# Add parent directory to sys.path to import backend modules
backend_path = Path(__file__).parent.parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from backend.data_loader import load_all_json_data
from backend import analyzer

logger = structlog.get_logger(__name__)


class AnalyzerService:
    """
    Service class for apartment transaction analysis
    Provides methods that wrap backend.analyzer functions
    """

    def __init__(self):
        """Initialize the analyzer service"""
        self._data_cache: Optional[List[Dict]] = None
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl_seconds = 300  # 5 minutes cache TTL

    def _load_data(self, force_reload: bool = False) -> Tuple[List[Dict], Dict]:
        """
        Load transaction data with caching

        Args:
            force_reload: If True, bypass cache and reload from source

        Returns:
            Tuple of (data items, debug info)
        """
        now = datetime.now()

        # Check if cache is valid
        if (not force_reload and
            self._data_cache is not None and
            self._cache_timestamp is not None):
            age_seconds = (now - self._cache_timestamp).total_seconds()
            if age_seconds < self._cache_ttl_seconds:
                logger.info(
                    "data_cache_hit",
                    cache_age_seconds=age_seconds,
                    record_count=len(self._data_cache)
                )
                return self._data_cache, {
                    'data_source': 'cache',
                    'cache_age_seconds': age_seconds,
                    'total_items': len(self._data_cache)
                }

        # Load fresh data
        logger.info("loading_data", force_reload=force_reload)
        items, debug_info = load_all_json_data(base_path=backend_path, debug=True)

        # Update cache
        self._data_cache = items
        self._cache_timestamp = now

        logger.info(
            "data_loaded",
            record_count=len(items),
            data_source=debug_info.get('data_source', 'unknown')
        )

        return items, debug_info

    def _filter_by_date_range(
        self,
        items: List[Dict],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Filter items by date range

        Args:
            items: Transaction data items
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            Filtered items
        """
        if not start_date and not end_date:
            return items

        filtered = []
        start_dt = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_dt = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

        for item in items:
            deal_date = item.get('_deal_date')
            if deal_date is None:
                continue

            # Convert string to datetime if needed
            if isinstance(deal_date, str):
                try:
                    deal_date = datetime.fromisoformat(deal_date)
                except (ValueError, TypeError):
                    continue

            # Apply date filters
            if start_dt and deal_date < start_dt:
                continue
            if end_dt and deal_date > end_dt:
                continue

            filtered.append(item)

        logger.info(
            "date_filter_applied",
            original_count=len(items),
            filtered_count=len(filtered),
            start_date=start_date,
            end_date=end_date
        )

        return filtered

    def _filter_by_region(
        self,
        items: List[Dict],
        region_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Filter items by region

        Args:
            items: Transaction data items
            region_filter: Region name to filter by

        Returns:
            Filtered items
        """
        if not region_filter:
            return items

        region_lower = region_filter.lower()
        filtered = [
            item for item in items
            if region_lower in item.get('_region_name', '').lower()
        ]

        logger.info(
            "region_filter_applied",
            original_count=len(items),
            filtered_count=len(filtered),
            region_filter=region_filter
        )

        return filtered

    def get_basic_stats(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """
        Get basic statistics

        Args:
            region_filter: Filter by region name
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            Tuple of (stats data, metadata)
        """
        # Load data
        items, debug_info = self._load_data()
        original_count = len(items)

        # Apply filters
        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        # Calculate statistics
        stats = analyzer.calculate_basic_stats(items)

        # Prepare metadata
        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return stats, metadata

    def get_price_trend(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """
        Get price trend analysis

        Args:
            region_filter: Filter by region name
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            Tuple of (trend data, metadata)
        """
        # Load data
        items, debug_info = self._load_data()
        original_count = len(items)

        # Apply filters
        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        # Calculate price trend
        trend = analyzer.calculate_price_trend(items)

        # Prepare metadata
        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return trend, metadata

    def get_regional_analysis(
        self,
        regions: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        top_n: int = 10
    ) -> Tuple[Dict, Dict]:
        """
        Get regional analysis

        Args:
            regions: List of regions to analyze (None = all regions)
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            top_n: Number of top regions to return

        Returns:
            Tuple of (regional data, metadata)
        """
        # Load data
        items, debug_info = self._load_data()
        original_count = len(items)

        # Apply date filter
        items = self._filter_by_date_range(items, start_date, end_date)

        # Filter by specific regions if provided
        if regions:
            filtered_items = []
            for region in regions:
                filtered_items.extend(self._filter_by_region(items, region))
            items = filtered_items

        # Calculate regional analysis
        regional_stats = analyzer.analyze_by_region(items)

        # Limit to top_n regions if specified
        if 'regions' in regional_stats and top_n > 0:
            regions_list = regional_stats['regions'][:top_n]
            regional_stats['regions'] = regions_list

        # Prepare metadata
        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return regional_stats, metadata

    def clear_cache(self):
        """Clear the data cache"""
        self._data_cache = None
        self._cache_timestamp = None
        logger.info("cache_cleared")

    # ========== Segmentation Methods ==========

    def get_area_analysis(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        bins: Optional[List[float]] = None
    ) -> Tuple[Dict, Dict]:
        """Get area-based analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_by_area(items, bins=bins)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_floor_analysis(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get floor-based analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_by_floor(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_build_year_analysis(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get build year analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_by_build_year(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_apartment_analysis(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_count: int = 5
    ) -> Tuple[Dict, Dict]:
        """Get apartment-based analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_by_apartment(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_apartment_detail(
        self,
        apt_name: str,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get specific apartment detail"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)

        result = analyzer.get_apartment_detail(items, apt_name, region=region_filter)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    # ========== Premium Methods ==========

    def get_price_per_area(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get price per area statistics"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.calculate_price_per_area(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_price_per_area_trend(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get price per area trend"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_price_per_area_trend(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_floor_premium(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get floor premium analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_floor_premium(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_building_age_premium(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get building age premium analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_building_age_premium(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    # ========== Investment Methods ==========

    def get_jeonse_ratio(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get jeonse ratio analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.calculate_jeonse_ratio(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_gap_investment(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_gap_ratio: float = 0.7
    ) -> Tuple[Dict, Dict]:
        """Get gap investment analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_gap_investment(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_bargain_sales(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        threshold_pct: float = 10.0
    ) -> Tuple[Dict, Dict]:
        """Get bargain sales detection"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.detect_bargain_sales(items, threshold_pct=threshold_pct)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    # ========== Market Methods ==========

    def get_rent_vs_jeonse(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get rent vs jeonse analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_rent_vs_jeonse(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_dealing_type(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get dealing type analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_dealing_type(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_buyer_seller_type(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get buyer/seller type analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_buyer_seller_type(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_cancelled_deals(
        self,
        region_filter: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get cancelled deals analysis"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_date_range(items, start_date, end_date)
        items = self._filter_by_region(items, region_filter)

        result = analyzer.analyze_cancelled_deals(items)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_period_summary(
        self,
        start_date: str,
        end_date: str,
        region_filter: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get period summary"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_region(items, region_filter)

        # Convert string dates to datetime
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')

        result = analyzer.summarize_period(items, start_dt, end_dt)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_baseline_summary(
        self,
        start_date: str,
        end_date: str,
        region_filter: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get baseline summary (previous period)"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_region(items, region_filter)

        # Convert string dates to datetime
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')

        result = analyzer.build_baseline_summary(items, start_dt, end_dt)

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_period_comparison(
        self,
        current_start_date: str,
        current_end_date: str,
        previous_start_date: str,
        previous_end_date: str,
        region_filter: Optional[str] = None,
        current_label: str = "Current",
        previous_label: str = "Previous"
    ) -> Tuple[Dict, Dict]:
        """Get period comparison"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_region(items, region_filter)

        # Convert string dates to datetime
        current_start_dt = datetime.strptime(current_start_date, '%Y-%m-%d')
        current_end_dt = datetime.strptime(current_end_date, '%Y-%m-%d')
        previous_start_dt = datetime.strptime(previous_start_date, '%Y-%m-%d')
        previous_end_dt = datetime.strptime(previous_end_date, '%Y-%m-%d')

        # Get summaries for both periods
        current_summary = analyzer.summarize_period(items, current_start_dt, current_end_dt)
        previous_summary = analyzer.summarize_period(items, previous_start_dt, previous_end_dt)

        # Compare periods
        result = analyzer.compare_periods(current_summary, previous_summary)

        # Add labels and summaries
        result['current_period'] = current_summary
        result['previous_period'] = previous_summary
        result['current_label'] = current_label
        result['previous_label'] = previous_label

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata

    def get_market_signals(
        self,
        start_date: str,
        end_date: str,
        region_filter: Optional[str] = None
    ) -> Tuple[Dict, Dict]:
        """Get market signals detection"""
        items, debug_info = self._load_data()
        original_count = len(items)

        items = self._filter_by_region(items, region_filter)

        # Convert string dates to datetime
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')

        # Get current period summary
        current_summary = analyzer.summarize_period(items, start_dt, end_dt)

        # Get baseline summary (previous period)
        baseline_summary = analyzer.build_baseline_summary(items, start_dt, end_dt)

        # Compare periods
        comparison = analyzer.compare_periods(current_summary, baseline_summary)

        # Detect signals
        signals = analyzer.detect_market_signals(current_summary, baseline_summary, comparison)

        result = {
            'signals': signals,
            'current_period': current_summary,
            'baseline_period': baseline_summary,
            'comparison': comparison
        }

        metadata = {
            'total_records': original_count,
            'filtered_records': len(items),
            'data_source': debug_info.get('data_source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        return result, metadata
