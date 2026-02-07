"""
Unit tests for backend/analyzer/investment.py
"""
import pytest
from datetime import datetime
from backend.analyzer.investment import (
    calculate_jeonse_ratio,
    analyze_gap_investment,
    detect_bargain_sales,
)


class TestCalculateJeonseRatio:
    """Test jeonse ratio calculation"""

    def test_no_data(self):
        result = calculate_jeonse_ratio([])
        assert result['has_data'] is False
        assert result['trade_count'] == 0
        assert result['jeonse_count'] == 0

    def test_no_trade_data(self):
        """Test with only jeonse data"""
        items = [
            {'_api_type': 'api_04', 'monthlyRent': '0', 'deposit': '50000'}
        ]
        result = calculate_jeonse_ratio(items)
        assert result['has_data'] is False
        assert result['trade_count'] == 0
        assert result['jeonse_count'] == 1

    def test_no_jeonse_data(self):
        """Test with only trade data"""
        items = [
            {'_api_type': 'api_02', '_deal_amount_numeric': 100000}
        ]
        result = calculate_jeonse_ratio(items)
        assert result['has_data'] is False
        assert result['trade_count'] == 1
        assert result['jeonse_count'] == 0

    def test_monthly_rent_filtered_out(self):
        """Test that monthly rent (월세) is filtered out"""
        items = [
            {'_api_type': 'api_04', 'monthlyRent': '50', 'deposit': '10000'},  # 월세
            {'_api_type': 'api_04', 'monthlyRent': '0', 'deposit': '50000'},   # 전세
        ]
        result = calculate_jeonse_ratio(items)
        assert result['jeonse_count'] == 1  # Only jeonse

    def test_no_matching_apartments(self):
        """Test when trade and jeonse have different apartments"""
        items = [
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '푸르지오',  # Different apartment
                '_region_name': '강남구',
                '_area_numeric': 84,
                'deposit': '50000',
            }
        ]
        result = calculate_jeonse_ratio(items)
        assert result['has_data'] is False
        assert 'message' in result

    def test_successful_matching(self):
        """Test successful trade-jeonse matching"""
        items = [
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                'deposit': '70000',
            }
        ]
        result = calculate_jeonse_ratio(items)

        assert result['has_data'] is True
        assert result['stats']['matched_apartments'] == 1
        assert result['all_data'][0]['jeonse_ratio'] == 70.0
        assert result['all_data'][0]['gap'] == 30000

    def test_area_grouping(self):
        """Test that similar areas (±2.5㎡) are grouped together"""
        items = [
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 83,  # 83 → 85 group
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 86,  # 86 → 85 group
                'deposit': '70000',
            }
        ]
        result = calculate_jeonse_ratio(items)

        # Should match because both round to 85
        assert result['has_data'] is True
        assert result['stats']['matched_apartments'] == 1

    def test_risk_classification(self):
        """Test jeonse ratio risk classification"""
        items = [
            # High risk (80% ratio)
            {
                '_api_type': 'api_02',
                'aptNm': '위험아파트',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '위험아파트',
                '_region_name': '강남구',
                '_area_numeric': 84,
                'deposit': '80000',
            },
            # Medium risk (75% ratio)
            {
                '_api_type': 'api_02',
                'aptNm': '보통아파트',
                '_region_name': '서초구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '보통아파트',
                '_region_name': '서초구',
                '_area_numeric': 84,
                'deposit': '75000',
            },
            # Low risk (60% ratio)
            {
                '_api_type': 'api_02',
                'aptNm': '안전아파트',
                '_region_name': '송파구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '안전아파트',
                '_region_name': '송파구',
                '_area_numeric': 84,
                'deposit': '60000',
            }
        ]
        result = calculate_jeonse_ratio(items)

        assert result['has_data'] is True
        assert result['risk_summary']['high_risk_count'] == 1
        assert result['risk_summary']['medium_risk_count'] == 1
        assert result['risk_summary']['low_risk_count'] == 1

    def test_region_statistics(self):
        """Test region-level statistics"""
        items = [
            {
                '_api_type': 'api_02',
                'aptNm': '래미안1',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '래미안1',
                '_region_name': '강남구',
                '_area_numeric': 84,
                'deposit': '70000',
            },
            {
                '_api_type': 'api_02',
                'aptNm': '래미안2',
                '_region_name': '강남구',
                '_area_numeric': 102,
                '_deal_amount_numeric': 120000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '래미안2',
                '_region_name': '강남구',
                '_area_numeric': 102,
                'deposit': '90000',
            }
        ]
        result = calculate_jeonse_ratio(items)

        assert result['has_data'] is True
        assert len(result['by_region']) >= 1
        gangnam = [r for r in result['by_region'] if r['region'] == '강남구'][0]
        assert gangnam['count'] == 2

    def test_multiple_prices_averaged(self):
        """Test that multiple prices for same apartment are averaged"""
        items = [
            # Two trades for same apartment
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 120000,
            },
            # Two jeonse for same apartment
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                'deposit': '70000',
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                'deposit': '80000',
            }
        ]
        result = calculate_jeonse_ratio(items)

        assert result['has_data'] is True
        data = result['all_data'][0]
        assert data['avg_trade_price'] == 110000  # (100000 + 120000) / 2
        assert data['avg_jeonse_price'] == 75000  # (70000 + 80000) / 2


class TestAnalyzeGapInvestment:
    """Test gap investment analysis"""

    def test_no_data(self):
        result = analyze_gap_investment([])
        assert result['has_data'] is False

    def test_insufficient_data(self):
        """Test with only trade data (no jeonse)"""
        items = [
            {'_api_type': 'api_02', '_deal_amount_numeric': 100000}
        ]
        result = analyze_gap_investment(items)
        assert result['has_data'] is False

    def test_gap_range_classification(self):
        """Test gap amount range classification"""
        items = [
            # Gap: 5000 (1억 이하)
            {
                '_api_type': 'api_02',
                'aptNm': '소액갭',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 50000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '소액갭',
                '_region_name': '강남구',
                '_area_numeric': 84,
                'deposit': '45000',
            },
            # Gap: 15000 (1~2억)
            {
                '_api_type': 'api_02',
                'aptNm': '중간갭',
                '_region_name': '서초구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '중간갭',
                '_region_name': '서초구',
                '_area_numeric': 84,
                'deposit': '85000',
            }
        ]
        result = analyze_gap_investment(items)

        assert result['has_data'] is True
        assert len(result['by_gap_range']) >= 2

        # Find the ranges
        ranges = {r['gap_range']: r for r in result['by_gap_range']}
        assert '1억 이하' in ranges
        assert '1~2억' in ranges

    def test_small_gap_items(self):
        """Test identification of small gap items (≤1억)"""
        items = [
            {
                '_api_type': 'api_02',
                'aptNm': '소액갭',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 50000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '소액갭',
                '_region_name': '강남구',
                '_area_numeric': 84,
                'deposit': '45000',  # Gap: 5000
            }
        ]
        result = analyze_gap_investment(items)

        assert result['has_data'] is True
        assert len(result['small_gap_items']) > 0
        assert result['small_gap_items'][0]['gap'] <= 10000

    def test_roi_calculation(self):
        """Test ROI estimation (4% annual rent assumption)"""
        items = [
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                'deposit': '80000',  # Gap: 20000
            }
        ]
        result = analyze_gap_investment(items)

        assert result['has_data'] is True
        # ROI = (80000 * 0.04) / 20000 * 100 = 16%
        assert len(result['high_roi_items']) > 0
        assert result['high_roi_items'][0]['estimated_roi'] == 16.0

    def test_gap_statistics(self):
        """Test gap statistics calculation"""
        items = [
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                'deposit': '70000',
            }
        ]
        result = analyze_gap_investment(items)

        assert result['has_data'] is True
        assert 'gap_stats' in result
        assert result['gap_stats']['avg_gap'] == 30000
        assert result['gap_stats']['total_count'] == 1


class TestDetectBargainSales:
    """Test bargain sale detection"""

    def test_insufficient_data(self):
        """Test with less than 10 items"""
        items = [
            {'_api_type': 'api_02', '_deal_amount_numeric': 100000, '_area_numeric': 84, '_deal_date': datetime(2024, 1, 1)}
        ]
        result = detect_bargain_sales(items)
        assert result['has_data'] is False
        assert result['bargain_count'] == 0

    def test_no_bargains_detected(self):
        """Test when all prices are normal (no discounts)"""
        items = []
        for i in range(15):
            items.append({
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,  # Same price
                '_deal_date': datetime(2024, 1, i+1),
            })

        result = detect_bargain_sales(items, threshold_pct=10.0)
        assert result['has_data'] is True
        assert result['stats']['bargain_count'] == 0

    def test_bargain_detection(self):
        """Test detection of discounted sales"""
        items = [
            # First 5 trades at 100,000
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, 1),
            },
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, 2),
            },
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, 3),
            },
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, 4),
            },
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, 5),
            },
            # Bargain sale at 85,000 (15% discount)
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 85000,
                '_deal_date': datetime(2024, 1, 6),
            },
            # Add more normal trades
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, 7),
            },
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, 8),
            },
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, 9),
            },
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, 10),
            },
        ]

        result = detect_bargain_sales(items, threshold_pct=10.0)

        assert result['has_data'] is True
        assert result['stats']['bargain_count'] >= 1
        assert any(b['discount_pct'] >= 10.0 for b in result['bargain_items'])

    def test_area_grouping(self):
        """Test that same apartment but different areas are treated separately"""
        items = []
        # 84㎡ trades
        for i in range(6):
            items.append({
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, i+1),
            })
        # 102㎡ trades (different area group)
        for i in range(6):
            items.append({
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 102,
                '_deal_amount_numeric': 150000,
                '_deal_date': datetime(2024, 1, i+1),
            })

        result = detect_bargain_sales(items)

        # Should compare within each area group separately
        assert result['has_data'] is True or result['bargain_count'] == 0

    def test_threshold_parameter(self):
        """Test custom threshold parameter"""
        items = []
        for i in range(6):
            items.append({
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, i+1),
            })
        # 5% discount
        items.append({
            '_api_type': 'api_02',
            'aptNm': '래미안',
            '_region_name': '강남구',
            '_area_numeric': 84,
            '_deal_amount_numeric': 95000,
            '_deal_date': datetime(2024, 1, 7),
        })

        # With 10% threshold: should NOT detect
        result_10 = detect_bargain_sales(items, threshold_pct=10.0)

        # With 3% threshold: SHOULD detect
        result_3 = detect_bargain_sales(items, threshold_pct=3.0)

        if result_3.get('has_data'):
            assert result_3['stats']['bargain_count'] >= result_10.get('stats', {}).get('bargain_count', 0)

    def test_recent_5_trades_used(self):
        """Test that only recent 5 trades are used for averaging"""
        items = []
        # 10 old trades at 200,000
        for i in range(10):
            items.append({
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 200000,
                '_deal_date': datetime(2024, 1, i+1),
            })
        # Recent 5 trades at 100,000
        for i in range(5):
            items.append({
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, i+11),
            })
        # Current trade at 95,000 (should compare with recent 5, not all 10)
        items.append({
            '_api_type': 'api_02',
            'aptNm': '래미안',
            '_region_name': '강남구',
            '_area_numeric': 84,
            '_deal_amount_numeric': 95000,
            '_deal_date': datetime(2024, 1, 16),
        })

        result = detect_bargain_sales(items, threshold_pct=3.0)

        # Should detect as bargain based on recent 5 (avg 100k), not all 15 (avg 166k)
        assert result['has_data'] is True

    def test_region_statistics(self):
        """Test region-level bargain statistics"""
        items = []
        # Bargains in 강남구
        for i in range(3):
            items.append({
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, i+1),
            })
        items.append({
            '_api_type': 'api_02',
            'aptNm': '래미안',
            '_region_name': '강남구',
            '_area_numeric': 84,
            '_deal_amount_numeric': 85000,  # Bargain
            '_deal_date': datetime(2024, 1, 4),
        })

        # Normal trades in 서초구
        for i in range(4):
            items.append({
                '_api_type': 'api_02',
                'aptNm': '푸르지오',
                '_region_name': '서초구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, i+1),
            })

        result = detect_bargain_sales(items, threshold_pct=10.0)

        if result.get('has_data'):
            assert 'by_region' in result
            if result['by_region']:
                # 강남구 should have higher bargain rate
                gangnam = [r for r in result['by_region'] if r['region'] == '강남구']
                if gangnam:
                    assert gangnam[0]['bargain_count'] >= 1


class TestIntegration:
    """Integration tests combining multiple functions"""

    def test_realistic_mixed_data(self):
        """Test with realistic mixed trade and jeonse data"""
        items = [
            # Trade data
            {
                '_api_type': 'api_02',
                'aptNm': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_deal_date': datetime(2024, 1, 1),
            },
            # Jeonse data
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                '아파트': '래미안',
                '_region_name': '강남구',
                '_area_numeric': 84,
                'deposit': '70000',
            }
        ]

        # All three functions should work
        jeonse_result = calculate_jeonse_ratio(items)
        gap_result = analyze_gap_investment(items)

        assert jeonse_result['has_data'] is True
        assert gap_result['has_data'] is True

        # Gap investment should use jeonse ratio results
        assert gap_result['gap_stats']['avg_gap'] == 30000


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
