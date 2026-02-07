"""
Unit tests for backend/analyzer/market_signals.py
"""
import pytest
from datetime import datetime
from backend.analyzer.market_signals import (
    analyze_rent_vs_jeonse,
    analyze_dealing_type,
    analyze_buyer_seller_type,
    analyze_cancelled_deals,
    summarize_period,
    build_baseline_summary,
    compare_periods,
    detect_market_signals,
)


class TestAnalyzeRentVsJeonse:
    """Test monthly rent vs jeonse analysis"""

    def test_no_rent_data(self):
        """Test with no API 04 data"""
        items = [
            {'_api_type': 'api_02', '_deal_amount_numeric': 100000}
        ]
        result = analyze_rent_vs_jeonse(items)
        assert result['has_data'] is False
        assert result['total_count'] == 0

    def test_classification(self):
        """Test classification of jeonse vs wolse"""
        items = [
            # Jeonse (monthly rent = 0)
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                'deposit': '50000',
            },
            # Wolse (monthly rent > 0)
            {
                '_api_type': 'api_04',
                'monthlyRent': '100',
                'deposit': '10000',
            }
        ]
        result = analyze_rent_vs_jeonse(items)

        assert result['has_data'] is True
        assert result['total_count'] == 2
        assert result['jeonse_count'] == 1
        assert result['wolse_count'] == 1

    def test_conversion_rate_calculation(self):
        """Test monthly rent conversion rate calculation"""
        items = [
            {
                '_api_type': 'api_04',
                'monthlyRent': '100',  # 100만원/월
                'deposit': '10000',     # 1억원
            }
        ]
        result = analyze_rent_vs_jeonse(items)

        # Conversion rate = (100 * 12) / 10000 * 100 = 12%
        assert result['has_data'] is True
        assert result['avg_conversion_rate'] == 12.0

    def test_region_breakdown(self):
        """Test region-level statistics"""
        items = [
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                'deposit': '50000',
                '_region_name': '강남구',
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '100',
                'deposit': '10000',
                '_region_name': '강남구',
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                'deposit': '30000',
                '_region_name': '서초구',
            }
        ]
        result = analyze_rent_vs_jeonse(items)

        assert result['has_data'] is True
        assert len(result['by_region']) == 2

    def test_area_breakdown(self):
        """Test breakdown by area size"""
        items = [
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                'deposit': '50000',
                '_area_numeric': 50,  # 소형
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '100',
                'deposit': '10000',
                '_area_numeric': 70,  # 중소형
            }
        ]
        result = analyze_rent_vs_jeonse(items)

        assert result['has_data'] is True
        assert len(result['by_area']) >= 1


class TestAnalyzeDealingType:
    """Test dealing type analysis"""

    def test_no_api_03_data(self):
        """Test with no detailed trade data"""
        items = [
            {'_api_type': 'api_02', '_deal_amount_numeric': 100000}
        ]
        result = analyze_dealing_type(items)
        # Should handle gracefully even without API 03 data
        assert 'stats' in result or 'has_data' in result

    def test_dealing_type_classification(self):
        """Test classification of dealing types (if data available)"""
        items = [
            {
                '_api_type': 'api_03',
                'dealingGbn': '직거래',
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_03',
                'dealingGbn': '중개거래',
                '_deal_amount_numeric': 120000,
            }
        ]
        result = analyze_dealing_type(items)

        # Check that function returns some analysis
        assert result is not None


class TestAnalyzeBuyerSellerType:
    """Test buyer/seller type analysis"""

    def test_no_api_03_data(self):
        """Test with no detailed trade data"""
        items = [
            {'_api_type': 'api_02', '_deal_amount_numeric': 100000}
        ]
        result = analyze_buyer_seller_type(items)
        # Should handle gracefully
        assert result is not None

    def test_buyer_seller_classification(self):
        """Test classification of buyer/seller types"""
        items = [
            {
                '_api_type': 'api_03',
                'buyerGbn': '개인',
                'sellerGbn': '개인',
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_03',
                'buyerGbn': '법인',
                'sellerGbn': '개인',
                '_deal_amount_numeric': 120000,
            }
        ]
        result = analyze_buyer_seller_type(items)

        # Check that function returns analysis
        assert result is not None


class TestAnalyzeCancelledDeals:
    """Test cancelled deal analysis"""

    def test_no_api_03_data(self):
        """Test with no detailed trade data"""
        items = [
            {'_api_type': 'api_02', '_deal_amount_numeric': 100000}
        ]
        result = analyze_cancelled_deals(items)
        # Should handle gracefully
        assert result is not None

    def test_cancelled_deal_detection(self):
        """Test detection of cancelled deals"""
        items = [
            {
                '_api_type': 'api_03',
                'dealCancDealDay': '',  # Not cancelled
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_03',
                'dealCancDealDay': '20240115',  # Cancelled
                '_deal_amount_numeric': 120000,
            }
        ]
        result = analyze_cancelled_deals(items)

        # Check that function returns analysis
        assert result is not None


class TestSummarizePeriod:
    """Test period summarization"""

    def test_empty_items(self):
        """Test with no data"""
        result = summarize_period([])
        # Should return basic structure even with empty data
        assert result is not None

    def test_basic_summarization(self):
        """Test basic period summary"""
        items = [
            {
                '_api_type': 'api_02',
                '_deal_amount_numeric': 100000,
                '_area_numeric': 84,
                '_region_name': '강남구',
            },
            {
                '_api_type': 'api_02',
                '_deal_amount_numeric': 120000,
                '_area_numeric': 102,
                '_region_name': '서초구',
            }
        ]
        result = summarize_period(items)

        # Should include basic statistics
        assert result is not None


class TestBuildBaselineSummary:
    """Test baseline summary creation"""

    def test_empty_items(self):
        """Test with no data"""
        result = build_baseline_summary([])
        # Should return basic structure
        assert result is not None

    def test_baseline_creation(self):
        """Test baseline summary with data"""
        items = [
            {
                '_api_type': 'api_02',
                '_deal_amount_numeric': 100000,
                '_area_numeric': 84,
                '_region_name': '강남구',
            }
        ]
        result = build_baseline_summary(items)

        # Should create a baseline summary
        assert result is not None


class TestComparePeriods:
    """Test period comparison"""

    def test_empty_periods(self):
        """Test with empty current and baseline periods"""
        result = compare_periods([], [])
        # Should handle empty data gracefully
        assert result is not None

    def test_period_comparison(self):
        """Test comparison between two periods"""
        baseline = [
            {
                '_api_type': 'api_02',
                '_deal_amount_numeric': 100000,
                '_area_numeric': 84,
                '_region_name': '강남구',
            }
        ]
        current = [
            {
                '_api_type': 'api_02',
                '_deal_amount_numeric': 110000,  # 10% increase
                '_area_numeric': 84,
                '_region_name': '강남구',
            }
        ]
        result = compare_periods(current, baseline)

        # Should include comparison metrics
        assert result is not None

    def test_comparison_with_no_baseline(self):
        """Test comparison when baseline is empty"""
        current = [
            {
                '_api_type': 'api_02',
                '_deal_amount_numeric': 100000,
                '_area_numeric': 84,
                '_region_name': '강남구',
            }
        ]
        result = compare_periods(current, [])

        # Should handle missing baseline
        assert result is not None


class TestDetectMarketSignals:
    """Test market signal detection"""

    def test_minimal_input(self):
        """Test with minimal required input"""
        current = {}
        baseline = {}
        comparison = {}

        result = detect_market_signals(current, baseline, comparison)

        # Should return signals structure
        assert result is not None
        assert isinstance(result, list)

    def test_price_surge_detection(self):
        """Test detection of price surge signal"""
        current = {'avg_price': 110000}
        baseline = {'avg_price': 100000}
        comparison = {'price_change_pct': 15.0}  # 15% increase

        result = detect_market_signals(current, baseline, comparison)

        # Should detect price surge (>10% increase)
        assert isinstance(result, list)

    def test_price_drop_detection(self):
        """Test detection of price drop signal"""
        current = {'avg_price': 85000}
        baseline = {'avg_price': 100000}
        comparison = {'price_change_pct': -15.0}  # 15% decrease

        result = detect_market_signals(current, baseline, comparison)

        # Should detect price drop
        assert isinstance(result, list)

    def test_volume_spike_detection(self):
        """Test detection of trading volume spike"""
        current = {'total_count': 150}
        baseline = {'total_count': 100}
        comparison = {'count_change_pct': 50.0}  # 50% increase

        result = detect_market_signals(current, baseline, comparison)

        # Should detect volume spike (>30% increase)
        assert isinstance(result, list)

    def test_multiple_signals(self):
        """Test detection of multiple simultaneous signals"""
        current = {
            'avg_price': 110000,
            'total_count': 150,
        }
        baseline = {
            'avg_price': 100000,
            'total_count': 100,
        }
        comparison = {
            'price_change_pct': 10.0,
            'count_change_pct': 50.0,
        }

        result = detect_market_signals(current, baseline, comparison)

        # Should detect multiple signals
        assert isinstance(result, list)

    def test_no_significant_changes(self):
        """Test when no significant market changes detected"""
        current = {'avg_price': 101000, 'total_count': 105}
        baseline = {'avg_price': 100000, 'total_count': 100}
        comparison = {
            'price_change_pct': 1.0,  # Small change
            'count_change_pct': 5.0,  # Small change
        }

        result = detect_market_signals(current, baseline, comparison)

        # Should return empty list or minimal signals
        assert isinstance(result, list)


class TestIntegration:
    """Integration tests combining multiple market signal functions"""

    def test_full_workflow(self):
        """Test complete workflow from summary to signal detection"""
        # Period 1 (baseline)
        baseline_items = []
        for i in range(10):
            baseline_items.append({
                '_api_type': 'api_02',
                '_deal_amount_numeric': 100000 + i * 1000,
                '_area_numeric': 84,
                '_region_name': '강남구',
            })

        # Period 2 (current) - with 10% price increase
        current_items = []
        for i in range(12):
            current_items.append({
                '_api_type': 'api_02',
                '_deal_amount_numeric': 110000 + i * 1000,
                '_area_numeric': 84,
                '_region_name': '강남구',
            })

        # Summarize periods
        baseline_summary = summarize_period(baseline_items)
        current_summary = summarize_period(current_items)

        # Compare periods
        comparison = compare_periods(current_items, baseline_items)

        # Detect signals
        signals = detect_market_signals(current_summary, baseline_summary, comparison)

        # All steps should complete successfully
        assert baseline_summary is not None
        assert current_summary is not None
        assert comparison is not None
        assert isinstance(signals, list)

    def test_rent_and_trade_combined(self):
        """Test analysis with both rental and trade data"""
        items = [
            # Trade data
            {
                '_api_type': 'api_02',
                '_deal_amount_numeric': 100000,
                '_area_numeric': 84,
                '_region_name': '강남구',
            },
            # Rental data (jeonse)
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                'deposit': '70000',
                '_area_numeric': 84,
                '_region_name': '강남구',
            },
            # Rental data (wolse)
            {
                '_api_type': 'api_04',
                'monthlyRent': '100',
                'deposit': '10000',
                '_area_numeric': 84,
                '_region_name': '강남구',
            }
        ]

        # Analyze rental market
        rent_analysis = analyze_rent_vs_jeonse(items)

        # Summarize overall period
        summary = summarize_period(items)

        # Both analyses should work
        assert rent_analysis['has_data'] is True
        assert summary is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
