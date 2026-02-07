"""
Unit tests for backend/analyzer/utils.py
"""
import pytest
from datetime import datetime
from backend.analyzer.utils import (
    categorize_floor,
    calculate_price_per_sqm,
    get_field_value,
    filter_by_api_type,
    filter_by_date_range,
    extract_numeric_values,
    safe_divide,
    format_price,
    parse_year_month,
    calculate_percentage_change,
)


class TestCategorizeFloor:
    """Test floor categorization function"""
    
    def test_low_floor(self):
        assert categorize_floor(1) == '저층'
        assert categorize_floor(5) == '저층'
    
    def test_mid_floor(self):
        assert categorize_floor(6) == '중층'
        assert categorize_floor(10) == '중층'
        assert categorize_floor(15) == '중층'
    
    def test_high_floor(self):
        assert categorize_floor(16) == '고층'
        assert categorize_floor(20) == '고층'
        assert categorize_floor(30) == '고층'
    
    def test_edge_cases(self):
        assert categorize_floor(0) == '저층'
        assert categorize_floor(-1) == '저층'


class TestCalculatePricePerSqm:
    """Test price per area calculation"""
    
    def test_normal_calculation(self):
        # 1억원, 84㎡ → 평당가
        result = calculate_price_per_sqm(100000, 84)
        assert result is not None
        assert isinstance(result, float)
        assert result > 0
    
    def test_zero_area(self):
        result = calculate_price_per_sqm(100000, 0)
        assert result is None
    
    def test_negative_area(self):
        result = calculate_price_per_sqm(100000, -10)
        assert result is None
    
    def test_none_area(self):
        result = calculate_price_per_sqm(100000, None)
        assert result is None
    
    def test_known_value(self):
        # 1평 = 3.3058㎡
        # 330.58만원, 3.3058㎡ → 100만원/평
        result = calculate_price_per_sqm(330.58, 3.3058)
        assert abs(result - 100.0) < 0.1  # Allow small floating point error


class TestGetFieldValue:
    """Test flexible field value extraction"""
    
    def test_single_key_exists(self):
        item = {'name': 'Test', 'value': 123}
        assert get_field_value(item, 'name') == 'Test'
    
    def test_multiple_keys_first_exists(self):
        item = {'aptNm': '래미안', '아파트': '푸르지오'}
        assert get_field_value(item, 'aptNm', '아파트') == '래미안'
    
    def test_multiple_keys_second_exists(self):
        item = {'아파트': '푸르지오'}
        assert get_field_value(item, 'aptNm', '아파트') == '푸르지오'
    
    def test_no_keys_exist(self):
        item = {'other': 'value'}
        assert get_field_value(item, 'name', 'title') is None
    
    def test_empty_string_is_skipped(self):
        item = {'name': '', 'title': 'Real Title'}
        assert get_field_value(item, 'name', 'title') == 'Real Title'
    
    def test_default_value(self):
        item = {'other': 'value'}
        assert get_field_value(item, 'name', default='Default') == 'Default'


class TestFilterByApiType:
    """Test API type filtering"""
    
    def test_filter_single_type(self):
        items = [
            {'_api_type': 'api_01', 'data': 1},
            {'_api_type': 'api_02', 'data': 2},
            {'_api_type': 'api_01', 'data': 3},
        ]
        result = filter_by_api_type(items, 'api_01')
        assert len(result) == 2
        assert all(item['_api_type'] == 'api_01' for item in result)
    
    def test_no_matches(self):
        items = [{'_api_type': 'api_01', 'data': 1}]
        result = filter_by_api_type(items, 'api_99')
        assert len(result) == 0
    
    def test_empty_list(self):
        result = filter_by_api_type([], 'api_01')
        assert len(result) == 0


class TestFilterByDateRange:
    """Test date range filtering"""
    
    def test_filter_within_range(self):
        items = [
            {'_deal_date': datetime(2024, 1, 15)},
            {'_deal_date': datetime(2024, 2, 15)},
            {'_deal_date': datetime(2024, 3, 15)},
        ]
        result = filter_by_date_range(
            items,
            start_date=datetime(2024, 2, 1),
            end_date=datetime(2024, 2, 28)
        )
        assert len(result) == 1
        assert result[0]['_deal_date'].month == 2
    
    def test_only_start_date(self):
        items = [
            {'_deal_date': datetime(2024, 1, 15)},
            {'_deal_date': datetime(2024, 2, 15)},
        ]
        result = filter_by_date_range(items, start_date=datetime(2024, 2, 1))
        assert len(result) == 1
    
    def test_only_end_date(self):
        items = [
            {'_deal_date': datetime(2024, 1, 15)},
            {'_deal_date': datetime(2024, 2, 15)},
        ]
        result = filter_by_date_range(items, end_date=datetime(2024, 1, 31))
        assert len(result) == 1
    
    def test_no_date_filters(self):
        items = [{'_deal_date': datetime(2024, 1, 15)}]
        result = filter_by_date_range(items)
        assert len(result) == 1


class TestExtractNumericValues:
    """Test numeric value extraction"""
    
    def test_extract_all_values(self):
        items = [
            {'price': 100},
            {'price': 200},
            {'price': 300},
        ]
        result = extract_numeric_values(items, 'price')
        assert result == [100, 200, 300]
    
    def test_skip_none_values(self):
        items = [
            {'price': 100},
            {'price': None},
            {'price': 200},
        ]
        result = extract_numeric_values(items, 'price')
        assert result == [100, 200]
    
    def test_empty_list(self):
        result = extract_numeric_values([], 'price')
        assert result == []


class TestSafeDivide:
    """Test safe division function"""
    
    def test_normal_division(self):
        assert safe_divide(10, 2) == 5.0
        assert safe_divide(7, 2) == 3.5
    
    def test_zero_denominator(self):
        assert safe_divide(10, 0) == 0.0
        assert safe_divide(10, 0, default=999) == 999
    
    def test_none_denominator(self):
        assert safe_divide(10, None) == 0.0
        assert safe_divide(10, None, default=-1) == -1
    
    def test_custom_default(self):
        assert safe_divide(10, 0, default=100) == 100


class TestFormatPrice:
    """Test price formatting function"""
    
    def test_under_1_eok(self):
        assert format_price(5000) == "5,000만원"
        assert format_price(9999) == "9,999만원"
    
    def test_exact_1_eok(self):
        assert format_price(10000) == "1억원"
    
    def test_over_1_eok_with_remainder(self):
        assert format_price(15000) == "1억 5,000만원"
        assert format_price(153000) == "15억 3,000만원"
    
    def test_over_1_eok_no_remainder(self):
        assert format_price(20000) == "2억원"
        assert format_price(100000) == "10억원"


class TestParseYearMonth:
    """Test year-month parsing"""
    
    def test_valid_format(self):
        result = parse_year_month('202401')
        assert result is not None
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 1
    
    def test_invalid_format(self):
        assert parse_year_month('2024-01') is None
        assert parse_year_month('invalid') is None
        assert parse_year_month('') is None
    
    def test_none_input(self):
        assert parse_year_month(None) is None


class TestCalculatePercentageChange:
    """Test percentage change calculation"""
    
    def test_positive_change(self):
        result = calculate_percentage_change(100, 150)
        assert result == 50.0
    
    def test_negative_change(self):
        result = calculate_percentage_change(100, 80)
        assert result == -20.0
    
    def test_no_change(self):
        result = calculate_percentage_change(100, 100)
        assert result == 0.0
    
    def test_zero_old_value(self):
        result = calculate_percentage_change(0, 100)
        assert result is None
    
    def test_none_old_value(self):
        result = calculate_percentage_change(None, 100)
        assert result is None
    
    def test_large_change(self):
        result = calculate_percentage_change(100, 300)
        assert result == 200.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
