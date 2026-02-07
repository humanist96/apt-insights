"""
Unit tests for backend/analyzer/segmentation.py
"""
import pytest
from backend.analyzer.segmentation import (
    analyze_by_area,
    analyze_by_floor,
    analyze_by_build_year,
    analyze_by_region,
    analyze_by_apartment,
    get_apartment_detail,
)


class TestAnalyzeByArea:
    """Test area-based analysis"""
    
    def test_empty_items(self):
        result = analyze_by_area([])
        assert result['bins'] == []
        assert result['data'] == []
    
    def test_auto_bins(self):
        """Test automatic bin generation"""
        items = [
            {'_area_numeric': 60, '_deal_amount_numeric': 40000},
            {'_area_numeric': 80, '_deal_amount_numeric': 50000},
            {'_area_numeric': 100, '_deal_amount_numeric': 60000},
        ]
        result = analyze_by_area(items)
        
        assert len(result['bins']) > 0
        assert len(result['data']) > 0
    
    def test_custom_bins(self):
        """Test with custom bins"""
        items = [
            {'_area_numeric': 60, '_deal_amount_numeric': 40000},
            {'_area_numeric': 85, '_deal_amount_numeric': 50000},
        ]
        bins = [0, 70, 90, 120]
        result = analyze_by_area(items, bins=bins)
        
        assert result['bins'] == bins
        assert len(result['data']) > 0
    
    def test_missing_values_filtered(self):
        """Test that items without area/price are filtered"""
        items = [
            {'_area_numeric': 80, '_deal_amount_numeric': 50000},
            {'_area_numeric': None, '_deal_amount_numeric': 50000},
            {'_area_numeric': 80, '_deal_amount_numeric': None},
        ]
        result = analyze_by_area(items)
        
        # Should only process 1 valid item
        total_count = sum(d['count'] for d in result['data'])
        assert total_count == 1


class TestAnalyzeByFloor:
    """Test floor-level analysis"""
    
    def test_empty_items(self):
        result = analyze_by_floor([])
        assert result['data'] == []
    
    def test_multiple_floors(self):
        """Test with multiple floor levels"""
        items = [
            {'_floor': 5, '_deal_amount_numeric': 40000},
            {'_floor': 10, '_deal_amount_numeric': 50000},
            {'_floor': 15, '_deal_amount_numeric': 60000},
        ]
        result = analyze_by_floor(items)
        
        assert len(result['data']) == 3
        floors = [d['floor'] for d in result['data']]
        assert floors == [5, 10, 15]  # Should be sorted
    
    def test_floor_statistics(self):
        """Test statistics calculation per floor"""
        items = [
            {'_floor': 10, '_deal_amount_numeric': 40000},
            {'_floor': 10, '_deal_amount_numeric': 50000},
            {'_floor': 10, '_deal_amount_numeric': 60000},
        ]
        result = analyze_by_floor(items)
        
        floor_10 = result['data'][0]
        assert floor_10['floor'] == 10
        assert floor_10['count'] == 3
        assert floor_10['avg_price'] == 50000
        assert floor_10['median_price'] == 50000
        assert floor_10['max_price'] == 60000
        assert floor_10['min_price'] == 40000


class TestAnalyzeByBuildYear:
    """Test building year analysis"""
    
    def test_empty_items(self):
        result = analyze_by_build_year([])
        assert result['data'] == []
    
    def test_multiple_years(self):
        """Test with multiple building years"""
        items = [
            {'_build_year': 2010, '_deal_amount_numeric': 40000},
            {'_build_year': 2015, '_deal_amount_numeric': 50000},
            {'_build_year': 2020, '_deal_amount_numeric': 60000},
        ]
        result = analyze_by_build_year(items)
        
        assert len(result['data']) == 3
        years = [d['build_year'] for d in result['data']]
        assert years == [2010, 2015, 2020]  # Should be sorted


class TestAnalyzeByRegion:
    """Test regional analysis"""
    
    def test_empty_items(self):
        result = analyze_by_region([])
        assert result['data'] == []
    
    def test_multiple_regions(self):
        """Test with multiple regions"""
        items = [
            {'_region_name': '강남구', '_deal_amount_numeric': 100000, '_area_numeric': 84},
            {'_region_name': '서초구', '_deal_amount_numeric': 90000, '_area_numeric': 80},
            {'_region_name': '강남구', '_deal_amount_numeric': 110000, '_area_numeric': 100},
        ]
        result = analyze_by_region(items)
        
        assert len(result['data']) == 2
        regions = {d['region'] for d in result['data']}
        assert regions == {'강남구', '서초구'}
    
    def test_region_statistics(self):
        """Test region statistics calculation"""
        items = [
            {
                '_region_name': '강남구',
                '_deal_amount_numeric': 100000,
                '_area_numeric': 80,
                '아파트': '래미안'
            },
            {
                '_region_name': '강남구',
                '_deal_amount_numeric': 120000,
                '_area_numeric': 100,
                '아파트': '푸르지오'
            },
        ]
        result = analyze_by_region(items)
        
        gangnam = [d for d in result['data'] if d['region'] == '강남구'][0]
        assert gangnam['count'] == 2
        assert gangnam['avg_price'] == 110000
        assert gangnam['apartment_count'] == 2


class TestAnalyzeByApartment:
    """Test apartment-level analysis"""
    
    def test_empty_items(self):
        result = analyze_by_apartment([])
        assert result['data'] == []
        assert result['total_apartments'] == 0
        assert result['total_deals'] == 0
    
    def test_multiple_apartments(self):
        """Test with multiple apartments"""
        items = [
            {'아파트': '래미안', '_region_name': '강남구', '_deal_amount_numeric': 100000, '_area_numeric': 84},
            {'아파트': '푸르지오', '_region_name': '서초구', '_deal_amount_numeric': 90000, '_area_numeric': 80},
        ]
        result = analyze_by_apartment(items)
        
        assert len(result['data']) == 2
        assert result['total_apartments'] == 2
        assert result['total_deals'] == 2
    
    def test_sorted_by_count(self):
        """Test that results are sorted by deal count (descending)"""
        items = [
            {'아파트': '래미안', '_region_name': '강남구', '_deal_amount_numeric': 100000},
            {'아파트': '푸르지오', '_region_name': '서초구', '_deal_amount_numeric': 90000},
            {'아파트': '푸르지오', '_region_name': '서초구', '_deal_amount_numeric': 95000},
        ]
        result = analyze_by_apartment(items)
        
        # First should be 푸르지오 (2 deals)
        assert result['data'][0]['apt_name'] == '푸르지오'
        assert result['data'][0]['count'] == 2


class TestGetApartmentDetail:
    """Test apartment detail retrieval"""
    
    def test_apartment_not_found(self):
        """Test when apartment doesn't exist"""
        result = get_apartment_detail([], '래미안')
        assert result['found'] is False
        assert result['apartment'] == '래미안'
    
    def test_apartment_found(self):
        """Test when apartment exists"""
        items = [
            {
                '아파트': '래미안',
                '_region_name': '강남구',
                '_deal_amount_numeric': 100000,
                '전용면적': '84㎡',
                '_deal_date': '2024-01-15'
            }
        ]
        result = get_apartment_detail(items, '래미안')
        
        assert result['found'] is True
        assert result['apartment'] == '래미안'
        assert result['total_count'] == 1
    
    def test_with_region_filter(self):
        """Test filtering by region"""
        items = [
            {'아파트': '래미안', '_region_name': '강남구', '_deal_amount_numeric': 100000},
            {'아파트': '래미안', '_region_name': '서초구', '_deal_amount_numeric': 90000},
        ]
        result = get_apartment_detail(items, '래미안', region='강남구')
        
        assert result['found'] is True
        assert result['total_count'] == 1
    
    def test_by_area_breakdown(self):
        """Test area breakdown in results"""
        items = [
            {'아파트': '래미안', '_deal_amount_numeric': 100000, '전용면적': '84㎡'},
            {'아파트': '래미안', '_deal_amount_numeric': 105000, '전용면적': '84㎡'},
            {'아파트': '래미안', '_deal_amount_numeric': 120000, '전용면적': '102㎡'},
        ]
        result = get_apartment_detail(items, '래미안')
        
        assert result['area_count'] == 2
        assert len(result['by_area']) == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
