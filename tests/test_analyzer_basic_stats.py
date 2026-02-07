"""
Unit tests for backend/analyzer/basic_stats.py
"""
import pytest
from backend.analyzer.basic_stats import (
    calculate_basic_stats,
    calculate_price_trend,
)


class TestCalculateBasicStats:
    """Test basic statistics calculation"""
    
    def test_empty_items(self):
        """Test with empty dataset"""
        result = calculate_basic_stats([])
        assert result['total_count'] == 0
        assert result['avg_price'] == 0
        assert result['max_price'] == 0
        assert result['min_price'] == 0
        assert result['median_price'] == 0
        assert result['avg_area'] == 0
    
    def test_single_item(self):
        """Test with single item"""
        items = [{
            '_deal_amount_numeric': 50000,
            '_area_numeric': 84.5,
            '_region_name': '강남구'
        }]
        result = calculate_basic_stats(items)
        
        assert result['total_count'] == 1
        assert result['avg_price'] == 50000
        assert result['max_price'] == 50000
        assert result['min_price'] == 50000
        assert result['median_price'] == 50000
        assert result['avg_area'] == 84.5
    
    def test_multiple_items(self):
        """Test with multiple items"""
        items = [
            {'_deal_amount_numeric': 40000, '_area_numeric': 60, '_region_name': '강남구'},
            {'_deal_amount_numeric': 50000, '_area_numeric': 80, '_region_name': '강남구'},
            {'_deal_amount_numeric': 60000, '_area_numeric': 100, '_region_name': '서초구'},
        ]
        result = calculate_basic_stats(items)
        
        assert result['total_count'] == 3
        assert result['avg_price'] == 50000
        assert result['max_price'] == 60000
        assert result['min_price'] == 40000
        assert result['median_price'] == 50000
        assert result['avg_area'] == 80
    
    def test_region_statistics(self):
        """Test region-level statistics"""
        items = [
            {'_deal_amount_numeric': 40000, '_region_name': '강남구'},
            {'_deal_amount_numeric': 50000, '_region_name': '강남구'},
            {'_deal_amount_numeric': 30000, '_region_name': '서초구'},
        ]
        result = calculate_basic_stats(items)
        
        assert '강남구' in result['regions']
        assert '서초구' in result['regions']
        assert result['regions']['강남구']['count'] == 2
        assert result['regions']['강남구']['avg_price'] == 45000
        assert result['regions']['서초구']['count'] == 1
    
    def test_missing_region(self):
        """Test items without region name"""
        items = [
            {'_deal_amount_numeric': 50000},
        ]
        result = calculate_basic_stats(items)
        
        assert '미지정' in result['regions']
        assert result['regions']['미지정']['count'] == 1
    
    def test_none_prices_filtered(self):
        """Test that None prices are filtered out"""
        items = [
            {'_deal_amount_numeric': 50000, '_area_numeric': 80},
            {'_deal_amount_numeric': None, '_area_numeric': 80},
            {'_deal_amount_numeric': 60000, '_area_numeric': 90},
        ]
        result = calculate_basic_stats(items)
        
        # Should only count 2 valid prices
        assert result['avg_price'] == 55000
        assert result['max_price'] == 60000
        assert result['min_price'] == 50000


class TestCalculatePriceTrend:
    """Test monthly price trend calculation"""
    
    def test_empty_items(self):
        """Test with empty dataset"""
        result = calculate_price_trend([])
        assert result['total_months'] == 0
        assert len(result['monthly_trend']) == 0
    
    def test_single_month(self):
        """Test with single month data"""
        items = [
            {'_year_month': '202401', '_deal_amount_numeric': 50000},
            {'_year_month': '202401', '_deal_amount_numeric': 60000},
        ]
        result = calculate_price_trend(items)
        
        assert result['total_months'] == 1
        assert '202401' in result['monthly_trend']
        assert result['monthly_trend']['202401']['count'] == 2
        assert result['monthly_trend']['202401']['avg_price'] == 55000
    
    def test_multiple_months(self):
        """Test with multiple months"""
        items = [
            {'_year_month': '202401', '_deal_amount_numeric': 50000},
            {'_year_month': '202402', '_deal_amount_numeric': 60000},
            {'_year_month': '202403', '_deal_amount_numeric': 70000},
        ]
        result = calculate_price_trend(items)
        
        assert result['total_months'] == 3
        monthly = result['monthly_trend']
        
        # Should be sorted by year_month
        months = list(monthly.keys())
        assert months == ['202401', '202402', '202403']
    
    def test_monthly_statistics(self):
        """Test monthly statistics calculation"""
        items = [
            {'_year_month': '202401', '_deal_amount_numeric': 40000},
            {'_year_month': '202401', '_deal_amount_numeric': 50000},
            {'_year_month': '202401', '_deal_amount_numeric': 60000},
        ]
        result = calculate_price_trend(items)
        
        stats = result['monthly_trend']['202401']
        assert stats['count'] == 3
        assert stats['avg_price'] == 50000
        assert stats['max_price'] == 60000
        assert stats['min_price'] == 40000
        assert stats['median_price'] == 50000
    
    def test_missing_year_month_filtered(self):
        """Test that items without year_month are filtered"""
        items = [
            {'_year_month': '202401', '_deal_amount_numeric': 50000},
            {'_year_month': None, '_deal_amount_numeric': 60000},
            {'_deal_amount_numeric': 70000},  # No _year_month key
        ]
        result = calculate_price_trend(items)
        
        assert result['total_months'] == 1
        assert '202401' in result['monthly_trend']
    
    def test_none_prices_filtered(self):
        """Test that None prices are filtered"""
        items = [
            {'_year_month': '202401', '_deal_amount_numeric': 50000},
            {'_year_month': '202401', '_deal_amount_numeric': None},
        ]
        result = calculate_price_trend(items)
        
        stats = result['monthly_trend']['202401']
        assert stats['count'] == 1
        assert stats['avg_price'] == 50000


class TestIntegration:
    """Integration tests combining both functions"""
    
    def test_realistic_dataset(self):
        """Test with realistic apartment data"""
        items = [
            {
                '_deal_amount_numeric': 100000,
                '_area_numeric': 84.5,
                '_region_name': '강남구',
                '_year_month': '202401'
            },
            {
                '_deal_amount_numeric': 120000,
                '_area_numeric': 102.3,
                '_region_name': '강남구',
                '_year_month': '202401'
            },
            {
                '_deal_amount_numeric': 80000,
                '_area_numeric': 59.7,
                '_region_name': '서초구',
                '_year_month': '202402'
            },
        ]
        
        # Basic stats
        basic = calculate_basic_stats(items)
        assert basic['total_count'] == 3
        assert basic['avg_price'] == 100000
        
        # Trend
        trend = calculate_price_trend(items)
        assert trend['total_months'] == 2
        assert trend['monthly_trend']['202401']['count'] == 2
        assert trend['monthly_trend']['202402']['count'] == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
