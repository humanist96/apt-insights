"""
Unit tests for backend/analyzer/premium_analysis.py
"""
import pytest
from datetime import datetime
from backend.analyzer.premium_analysis import (
    calculate_price_per_area,
    analyze_price_per_area_trend,
    analyze_floor_premium,
    analyze_building_age_premium,
)


class TestCalculatePricePerArea:
    """Test price per area calculation"""

    def test_empty_items(self):
        result = calculate_price_per_area([])
        assert result['stats'] == {}
        assert result['by_region'] == []
        assert result['by_area_range'] == []

    def test_missing_values_filtered(self):
        """Test that items without area or price are filtered"""
        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 100000},
            {'_area_numeric': None, '_deal_amount_numeric': 100000},  # Filtered
            {'_area_numeric': 84, '_deal_amount_numeric': None},       # Filtered
            {'_area_numeric': 0, '_deal_amount_numeric': 100000},      # Filtered (zero area)
        ]
        result = calculate_price_per_area(items)
        assert result['stats']['total_count'] == 1

    def test_price_per_area_calculation(self):
        """Test ㎡당 가격 calculation"""
        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 84000}  # 1000 per ㎡
        ]
        result = calculate_price_per_area(items)
        assert result['stats']['avg_price_per_area'] == 1000.0

    def test_statistics_calculation(self):
        """Test overall statistics"""
        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 84000},   # 1000 per ㎡
            {'_area_numeric': 84, '_deal_amount_numeric': 168000},  # 2000 per ㎡
            {'_area_numeric': 84, '_deal_amount_numeric': 252000},  # 3000 per ㎡
        ]
        result = calculate_price_per_area(items)

        assert result['stats']['avg_price_per_area'] == 2000.0
        assert result['stats']['median_price_per_area'] == 2000.0
        assert result['stats']['max_price_per_area'] == 3000.0
        assert result['stats']['min_price_per_area'] == 1000.0
        assert result['stats']['total_count'] == 3

    def test_region_breakdown(self):
        """Test region-level statistics"""
        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 84000, '_region_name': '강남구'},
            {'_area_numeric': 84, '_deal_amount_numeric': 168000, '_region_name': '강남구'},
            {'_area_numeric': 84, '_deal_amount_numeric': 84000, '_region_name': '서초구'},
        ]
        result = calculate_price_per_area(items)

        assert len(result['by_region']) == 2
        regions = {r['region']: r for r in result['by_region']}

        assert '강남구' in regions
        assert regions['강남구']['count'] == 2
        assert regions['강남구']['avg_price_per_area'] == 1500.0  # (1000 + 2000) / 2

    def test_area_range_classification(self):
        """Test classification by area size"""
        items = [
            {'_area_numeric': 50, '_deal_amount_numeric': 50000},    # 소형
            {'_area_numeric': 70, '_deal_amount_numeric': 70000},    # 중소형
            {'_area_numeric': 90, '_deal_amount_numeric': 90000},    # 중형
            {'_area_numeric': 110, '_deal_amount_numeric': 110000},  # 중대형
            {'_area_numeric': 150, '_deal_amount_numeric': 150000},  # 대형
        ]
        result = calculate_price_per_area(items)

        assert len(result['by_area_range']) == 5
        ranges = {r['area_range']: r for r in result['by_area_range']}

        assert '소형 (60㎡ 미만)' in ranges
        assert '중소형 (60-85㎡)' in ranges
        assert '중형 (85-102㎡)' in ranges
        assert '중대형 (102-135㎡)' in ranges
        assert '대형 (135㎡ 이상)' in ranges

    def test_build_year_classification(self):
        """Test classification by building age"""
        current_year = datetime.now().year
        items = [
            # 신축 (5년 이내)
            {
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000,
                '_build_year_numeric': current_year - 2,
            },
            # 준신축 (6-10년)
            {
                '_area_numeric': 84,
                '_deal_amount_numeric': 90000,
                '_build_year_numeric': current_year - 8,
            },
        ]
        result = calculate_price_per_area(items)

        assert len(result['by_build_year']) >= 1

    def test_top_expensive_and_affordable(self):
        """Test identification of most/least expensive properties"""
        items = []
        for i in range(15):
            items.append({
                '_area_numeric': 84,
                '_deal_amount_numeric': (i + 1) * 10000,  # 10000, 20000, ... 150000
                'aptNm': f'아파트{i}',
                '_region_name': '강남구',
            })

        result = calculate_price_per_area(items)

        # Top 10 expensive
        assert len(result['top_expensive']) == 10
        assert result['top_expensive'][0]['price_per_area'] > result['top_expensive'][-1]['price_per_area']

        # Top 10 affordable
        assert len(result['top_affordable']) == 10
        assert result['top_affordable'][0]['price_per_area'] < result['top_affordable'][-1]['price_per_area']

    def test_region_sorted_by_price(self):
        """Test that regions are sorted by average price (descending)"""
        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 84000, '_region_name': '저가지역'},   # 1000
            {'_area_numeric': 84, '_deal_amount_numeric': 252000, '_region_name': '고가지역'},  # 3000
            {'_area_numeric': 84, '_deal_amount_numeric': 168000, '_region_name': '중가지역'},  # 2000
        ]
        result = calculate_price_per_area(items)

        # Should be sorted: 고가 → 중가 → 저가
        assert result['by_region'][0]['region'] == '고가지역'
        assert result['by_region'][1]['region'] == '중가지역'
        assert result['by_region'][2]['region'] == '저가지역'


class TestAnalyzePricePerAreaTrend:
    """Test monthly price per area trend analysis"""

    def test_empty_items(self):
        result = analyze_price_per_area_trend([])
        assert result['trend'] == []

    def test_missing_required_fields(self):
        """Test that items without required fields are filtered"""
        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 100000, '_deal_year_month': '202401'},
            {'_area_numeric': None, '_deal_amount_numeric': 100000, '_deal_year_month': '202401'},  # Filtered
            {'_area_numeric': 84, '_deal_amount_numeric': None, '_deal_year_month': '202401'},      # Filtered
            {'_area_numeric': 84, '_deal_amount_numeric': 100000, '_deal_year_month': None},        # Filtered
        ]
        result = analyze_price_per_area_trend(items)

        assert len(result['trend']) == 1
        assert result['trend'][0]['count'] == 1

    def test_monthly_grouping(self):
        """Test that data is grouped by month"""
        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 84000, '_deal_year_month': '202401'},
            {'_area_numeric': 84, '_deal_amount_numeric': 84000, '_deal_year_month': '202401'},
            {'_area_numeric': 84, '_deal_amount_numeric': 84000, '_deal_year_month': '202402'},
        ]
        result = analyze_price_per_area_trend(items)

        assert len(result['trend']) == 2
        assert result['trend'][0]['year_month'] == '202401'
        assert result['trend'][1]['year_month'] == '202402'

    def test_monthly_statistics(self):
        """Test monthly price per area statistics"""
        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 84000, '_deal_year_month': '202401'},   # 1000
            {'_area_numeric': 84, '_deal_amount_numeric': 168000, '_deal_year_month': '202401'},  # 2000
            {'_area_numeric': 84, '_deal_amount_numeric': 252000, '_deal_year_month': '202401'},  # 3000
        ]
        result = analyze_price_per_area_trend(items)

        month_data = result['trend'][0]
        assert month_data['count'] == 3
        assert month_data['avg_price_per_area'] == 2000.0
        assert month_data['median_price_per_area'] == 2000.0
        assert month_data['max_price_per_area'] == 3000.0
        assert month_data['min_price_per_area'] == 1000.0

    def test_change_rate_calculation(self):
        """Test month-over-month change rate calculation"""
        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 84000, '_deal_year_month': '202401'},   # 1000
            {'_area_numeric': 84, '_deal_amount_numeric': 105000, '_deal_year_month': '202402'},  # 1250 (+25%)
            {'_area_numeric': 84, '_deal_amount_numeric': 126000, '_deal_year_month': '202403'},  # 1500 (+20%)
        ]
        result = analyze_price_per_area_trend(items)

        assert result['trend'][0]['change_rate'] == 0  # First month has no change
        assert result['trend'][1]['change_rate'] == 25.0  # (1250 - 1000) / 1000 * 100
        assert result['trend'][2]['change_rate'] == 20.0  # (1500 - 1250) / 1250 * 100

    def test_sorted_by_month(self):
        """Test that trend is sorted by year_month"""
        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 84000, '_deal_year_month': '202403'},
            {'_area_numeric': 84, '_deal_amount_numeric': 84000, '_deal_year_month': '202401'},
            {'_area_numeric': 84, '_deal_amount_numeric': 84000, '_deal_year_month': '202402'},
        ]
        result = analyze_price_per_area_trend(items)

        months = [t['year_month'] for t in result['trend']]
        assert months == ['202401', '202402', '202403']


class TestAnalyzeFloorPremium:
    """Test floor premium analysis"""

    def test_insufficient_data(self):
        """Test with less than 10 items"""
        items = [
            {'_floor_numeric': 5, '_deal_amount_numeric': 100000, '_area_numeric': 84}
        ]
        result = analyze_floor_premium(items)
        assert result['has_data'] is False

    def test_floor_category_classification(self):
        """Test floor categorization"""
        items = []
        # Generate 20 items across different floors
        for floor in [0, 3, 8, 13, 18, 25]:
            for _ in range(2):
                items.append({
                    '_floor_numeric': floor,
                    '_deal_amount_numeric': 100000,
                    '_area_numeric': 84,
                })

        result = analyze_floor_premium(items)

        assert result['has_data'] is True
        categories = {c['floor_category'] for c in result['by_floor_category']}

        # Check that categories exist (depending on data)
        assert len(categories) >= 1

    def test_floor_premium_calculation(self):
        """Test premium calculation relative to base floor"""
        items = []
        # 저층 (1-5): 100만원/㎡
        for _ in range(3):
            items.append({'_floor_numeric': 3, '_deal_amount_numeric': 84000, '_area_numeric': 84})

        # 중층 (11-15): 120만원/㎡ (base)
        for _ in range(3):
            items.append({'_floor_numeric': 13, '_deal_amount_numeric': 100800, '_area_numeric': 84})

        # 고층 (21+): 140만원/㎡
        for _ in range(4):
            items.append({'_floor_numeric': 25, '_deal_amount_numeric': 117600, '_area_numeric': 84})

        result = analyze_floor_premium(items)

        assert result['has_data'] is True
        assert 'by_floor_category' in result

        # Check that premium_pct is calculated
        for cat in result['by_floor_category']:
            assert 'premium_pct' in cat

    def test_individual_floor_analysis(self):
        """Test individual floor (1-30) analysis"""
        items = []
        for floor in range(1, 21):  # 1-20층
            items.append({
                '_floor_numeric': floor,
                '_deal_amount_numeric': 100000 + floor * 1000,  # Higher floors cost more
                '_area_numeric': 84,
            })

        result = analyze_floor_premium(items)

        assert result['has_data'] is True
        assert len(result['by_individual_floor']) >= 15  # Should have many floors

    def test_royal_floor_detection(self):
        """Test detection of the most expensive floor (royal floor)"""
        items = []
        # Most floors at 100만원/㎡
        for floor in [5, 10, 20, 25]:
            items.append({'_floor_numeric': floor, '_deal_amount_numeric': 84000, '_area_numeric': 84})

        # Floor 15 at 150만원/㎡ (royal floor)
        for _ in range(5):
            items.append({'_floor_numeric': 15, '_deal_amount_numeric': 126000, '_area_numeric': 84})

        result = analyze_floor_premium(items)

        assert result['has_data'] is True
        if result['stats']['royal_floor']:
            assert result['stats']['royal_floor'] == 15

    def test_basement_floor(self):
        """Test basement/semi-basement classification"""
        items = []
        # Basement
        for _ in range(3):
            items.append({'_floor_numeric': 0, '_deal_amount_numeric': 50000, '_area_numeric': 84})

        # Regular floors
        for floor in range(1, 11):
            items.append({'_floor_numeric': floor, '_deal_amount_numeric': 100000, '_area_numeric': 84})

        result = analyze_floor_premium(items)

        assert result['has_data'] is True
        categories = [c['floor_category'] for c in result['by_floor_category']]
        assert '지하/반지하' in categories


class TestAnalyzeBuildingAgePremium:
    """Test building age premium analysis"""

    def test_insufficient_data(self):
        """Test with less than 10 items"""
        items = [
            {'_build_year_numeric': 2020, '_deal_amount_numeric': 100000, '_area_numeric': 84}
        ]
        result = analyze_building_age_premium(items)
        assert result['has_data'] is False

    def test_invalid_build_years_filtered(self):
        """Test that invalid build years are filtered out"""
        current_year = datetime.now().year
        items = []
        # Valid years
        for _ in range(8):
            items.append({
                '_build_year_numeric': 2020,
                '_deal_amount_numeric': 100000,
                '_area_numeric': 84,
            })
        # Invalid years (too old)
        items.append({'_build_year_numeric': 1950, '_deal_amount_numeric': 100000, '_area_numeric': 84})
        # Invalid years (future)
        items.append({'_build_year_numeric': current_year + 5, '_deal_amount_numeric': 100000, '_area_numeric': 84})

        result = analyze_building_age_premium(items)

        # Should only process the 8 valid items
        assert result['stats']['total_count'] == 8

    def test_age_range_classification(self):
        """Test classification by building age"""
        current_year = datetime.now().year
        items = []

        # 신축 (0-5년)
        for _ in range(3):
            items.append({
                '_build_year_numeric': current_year - 2,
                '_deal_amount_numeric': 100000,
                '_area_numeric': 84,
            })

        # 준신축 (6-10년)
        for _ in range(3):
            items.append({
                '_build_year_numeric': current_year - 8,
                '_deal_amount_numeric': 90000,
                '_area_numeric': 84,
            })

        # 구축 (21-30년)
        for _ in range(4):
            items.append({
                '_build_year_numeric': current_year - 25,
                '_deal_amount_numeric': 70000,
                '_area_numeric': 84,
            })

        result = analyze_building_age_premium(items)

        assert result['has_data'] is True
        assert len(result['by_age_range']) >= 2

    def test_new_building_premium(self):
        """Test premium calculation vs new buildings"""
        current_year = datetime.now().year
        items = []

        # New buildings: 1200 per ㎡
        for _ in range(5):
            items.append({
                '_build_year_numeric': current_year - 2,
                '_deal_amount_numeric': 100800,
                '_area_numeric': 84,
            })

        # Old buildings: 1000 per ㎡ (16.67% discount)
        for _ in range(5):
            items.append({
                '_build_year_numeric': current_year - 25,
                '_deal_amount_numeric': 84000,
                '_area_numeric': 84,
            })

        result = analyze_building_age_premium(items)

        assert result['has_data'] is True

        # Old buildings should have negative premium
        old_range = [r for r in result['by_age_range'] if '구축' in r['age_range']]
        if old_range:
            assert old_range[0]['vs_new_pct'] < 0

    def test_annual_depreciation_calculation(self):
        """Test annual depreciation rate calculation"""
        current_year = datetime.now().year
        items = []

        # New buildings
        for _ in range(5):
            items.append({
                '_build_year_numeric': current_year - 2,
                '_deal_amount_numeric': 100000,
                '_area_numeric': 84,
            })

        # Old buildings
        for _ in range(5):
            items.append({
                '_build_year_numeric': current_year - 30,
                '_deal_amount_numeric': 70000,
                '_area_numeric': 84,
            })

        result = analyze_building_age_premium(items)

        assert result['has_data'] is True
        assert 'annual_depreciation_pct' in result['stats']

    def test_rebuild_candidates(self):
        """Test identification of rebuild candidates (30+ years)"""
        current_year = datetime.now().year
        items = []

        # Buildings 30+ years old
        for i in range(8):
            items.append({
                '_build_year_numeric': current_year - 35,
                '_deal_amount_numeric': 50000,
                '_area_numeric': 84,
                'aptNm': f'재건축대상{i}',
                '_region_name': '강남구',
            })

        # Recent buildings
        for _ in range(5):
            items.append({
                '_build_year_numeric': current_year - 10,
                '_deal_amount_numeric': 100000,
                '_area_numeric': 84,
                'aptNm': '신축아파트',
                '_region_name': '서초구',
            })

        result = analyze_building_age_premium(items)

        assert result['has_data'] is True
        assert result['stats']['rebuild_candidate_count'] == 8
        assert len(result['rebuild_candidates']) >= 1  # Unique apartments

    def test_year_detail_sorted(self):
        """Test that year details are sorted (newest first)"""
        current_year = datetime.now().year
        items = []

        for year_offset in [5, 10, 15, 20]:
            for _ in range(3):
                items.append({
                    '_build_year_numeric': current_year - year_offset,
                    '_deal_amount_numeric': 100000,
                    '_area_numeric': 84,
                })

        result = analyze_building_age_premium(items)

        assert result['has_data'] is True
        if len(result['by_build_year']) >= 2:
            # Should be sorted newest first
            years = [y['build_year'] for y in result['by_build_year']]
            assert years == sorted(years, reverse=True)


class TestIntegration:
    """Integration tests combining multiple functions"""

    def test_realistic_data_all_functions(self):
        """Test all premium functions with realistic data"""
        current_year = datetime.now().year
        items = []

        # Generate realistic mixed data
        for i in range(20):
            items.append({
                '_area_numeric': 84,
                '_deal_amount_numeric': 100000 + i * 1000,
                '_region_name': '강남구' if i % 2 == 0 else '서초구',
                '_floor_numeric': (i % 20) + 1,
                '_build_year_numeric': current_year - (i % 30),
                '_deal_year_month': f'2024{(i % 12 + 1):02d}',
            })

        # All functions should work
        price_per_area = calculate_price_per_area(items)
        trend = analyze_price_per_area_trend(items)
        floor_premium = analyze_floor_premium(items)
        age_premium = analyze_building_age_premium(items)

        assert price_per_area['stats']['total_count'] == 20
        assert len(trend['trend']) >= 1
        assert floor_premium['has_data'] is True
        assert age_premium['has_data'] is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
