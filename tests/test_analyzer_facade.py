"""
Unit tests for backend/analyzer/__init__.py (Facade Pattern)

This test file verifies that the facade pattern works correctly and
all 23 functions from 5 modules are properly exported and accessible.
"""
import pytest


class TestFacadeImports:
    """Test that all functions are importable from backend.analyzer"""

    def test_all_functions_importable(self):
        """Test that all 23 functions can be imported from the facade"""
        # This should not raise any ImportError
        from backend.analyzer import (
            # basic_stats.py (2 functions)
            calculate_basic_stats,
            calculate_price_trend,
            # segmentation.py (6 functions)
            analyze_by_area,
            analyze_by_floor,
            analyze_by_build_year,
            analyze_by_region,
            analyze_by_apartment,
            get_apartment_detail,
            # investment.py (3 functions)
            calculate_jeonse_ratio,
            analyze_gap_investment,
            detect_bargain_sales,
            # premium_analysis.py (4 functions)
            calculate_price_per_area,
            analyze_price_per_area_trend,
            analyze_floor_premium,
            analyze_building_age_premium,
            # market_signals.py (8 functions)
            analyze_rent_vs_jeonse,
            analyze_dealing_type,
            analyze_buyer_seller_type,
            analyze_cancelled_deals,
            summarize_period,
            build_baseline_summary,
            compare_periods,
            detect_market_signals,
        )

        # If we got here, all imports succeeded
        assert True

    def test_function_count(self):
        """Test that exactly 23 functions are exported"""
        import backend.analyzer as analyzer

        # Get all exported items (those in __all__)
        exported = getattr(analyzer, '__all__', [])

        # Should have exactly 23 functions
        assert len(exported) == 23

    def test_no_extra_exports(self):
        """Test that only intended functions are exported"""
        import backend.analyzer as analyzer

        expected_functions = {
            # basic_stats.py (2)
            'calculate_basic_stats',
            'calculate_price_trend',
            # segmentation.py (6)
            'analyze_by_area',
            'analyze_by_floor',
            'analyze_by_build_year',
            'analyze_by_region',
            'analyze_by_apartment',
            'get_apartment_detail',
            # investment.py (3)
            'calculate_jeonse_ratio',
            'analyze_gap_investment',
            'detect_bargain_sales',
            # premium_analysis.py (4)
            'calculate_price_per_area',
            'analyze_price_per_area_trend',
            'analyze_floor_premium',
            'analyze_building_age_premium',
            # market_signals.py (8)
            'analyze_rent_vs_jeonse',
            'analyze_dealing_type',
            'analyze_buyer_seller_type',
            'analyze_cancelled_deals',
            'summarize_period',
            'build_baseline_summary',
            'compare_periods',
            'detect_market_signals',
        }

        exported = set(getattr(analyzer, '__all__', []))

        # Check that exported set matches expected set
        assert exported == expected_functions

    def test_functions_are_callable(self):
        """Test that all exported functions are actually callable"""
        from backend.analyzer import (
            calculate_basic_stats,
            calculate_price_trend,
            analyze_by_area,
            analyze_by_floor,
            analyze_by_build_year,
            analyze_by_region,
            analyze_by_apartment,
            get_apartment_detail,
            calculate_jeonse_ratio,
            analyze_gap_investment,
            detect_bargain_sales,
            calculate_price_per_area,
            analyze_price_per_area_trend,
            analyze_floor_premium,
            analyze_building_age_premium,
            analyze_rent_vs_jeonse,
            analyze_dealing_type,
            analyze_buyer_seller_type,
            analyze_cancelled_deals,
            summarize_period,
            build_baseline_summary,
            compare_periods,
            detect_market_signals,
        )

        all_functions = [
            calculate_basic_stats,
            calculate_price_trend,
            analyze_by_area,
            analyze_by_floor,
            analyze_by_build_year,
            analyze_by_region,
            analyze_by_apartment,
            get_apartment_detail,
            calculate_jeonse_ratio,
            analyze_gap_investment,
            detect_bargain_sales,
            calculate_price_per_area,
            analyze_price_per_area_trend,
            analyze_floor_premium,
            analyze_building_age_premium,
            analyze_rent_vs_jeonse,
            analyze_dealing_type,
            analyze_buyer_seller_type,
            analyze_cancelled_deals,
            summarize_period,
            build_baseline_summary,
            compare_periods,
            detect_market_signals,
        ]

        # All should be callable
        for func in all_functions:
            assert callable(func)


class TestBackwardCompatibility:
    """Test that old import paths still work (backward compatibility)"""

    def test_old_import_path_works(self):
        """Test that importing from backend.analyzer works as before"""
        # This is the old way of importing (before modularization)
        from backend.analyzer import calculate_basic_stats

        # Should be callable
        assert callable(calculate_basic_stats)

        # Should work with empty data
        result = calculate_basic_stats([])
        assert result['total_count'] == 0

    def test_module_level_access(self):
        """Test that functions can be accessed via module reference"""
        import backend.analyzer as analyzer

        # All functions should be accessible
        assert hasattr(analyzer, 'calculate_basic_stats')
        assert hasattr(analyzer, 'analyze_by_area')
        assert hasattr(analyzer, 'calculate_jeonse_ratio')
        assert hasattr(analyzer, 'calculate_price_per_area')
        assert hasattr(analyzer, 'analyze_rent_vs_jeonse')


class TestFunctionalityPreserved:
    """Test that functions still work correctly after modularization"""

    def test_basic_stats_still_works(self):
        """Test that basic_stats functions work identically"""
        from backend.analyzer import calculate_basic_stats

        items = [
            {'_deal_amount_numeric': 100000, '_area_numeric': 84, '_region_name': '강남구'},
            {'_deal_amount_numeric': 120000, '_area_numeric': 102, '_region_name': '서초구'},
        ]

        result = calculate_basic_stats(items)

        assert result['total_count'] == 2
        assert result['avg_price'] == 110000
        assert '강남구' in result['regions']

    def test_segmentation_still_works(self):
        """Test that segmentation functions work identically"""
        from backend.analyzer import analyze_by_area

        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 100000},
            {'_area_numeric': 102, '_deal_amount_numeric': 120000},
        ]

        result = analyze_by_area(items)

        assert len(result['bins']) > 0
        assert len(result['data']) > 0

    def test_investment_still_works(self):
        """Test that investment functions work identically"""
        from backend.analyzer import calculate_jeonse_ratio

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
        assert result['all_data'][0]['jeonse_ratio'] == 70.0

    def test_premium_analysis_still_works(self):
        """Test that premium analysis functions work identically"""
        from backend.analyzer import calculate_price_per_area

        items = [
            {'_area_numeric': 84, '_deal_amount_numeric': 84000},  # 1000 per ㎡
            {'_area_numeric': 102, '_deal_amount_numeric': 102000},  # 1000 per ㎡
        ]

        result = calculate_price_per_area(items)

        assert result['stats']['total_count'] == 2
        assert result['stats']['avg_price_per_area'] == 1000.0

    def test_market_signals_still_works(self):
        """Test that market signal functions work identically"""
        from backend.analyzer import analyze_rent_vs_jeonse

        items = [
            {
                '_api_type': 'api_04',
                'monthlyRent': '0',
                'deposit': '50000',
            },
            {
                '_api_type': 'api_04',
                'monthlyRent': '100',
                'deposit': '10000',
            }
        ]

        result = analyze_rent_vs_jeonse(items)

        assert result['has_data'] is True
        assert result['jeonse_count'] == 1
        assert result['wolse_count'] == 1


class TestModuleStructure:
    """Test the module structure and organization"""

    def test_submodules_not_directly_accessible(self):
        """Test that submodules are not polluting the namespace"""
        import backend.analyzer as analyzer

        # These internal module names should NOT be in __all__
        exported = set(getattr(analyzer, '__all__', []))

        assert 'basic_stats' not in exported
        assert 'segmentation' not in exported
        assert 'investment' not in exported
        assert 'premium_analysis' not in exported
        assert 'market_signals' not in exported
        assert 'utils' not in exported

    def test_all_contains_only_functions(self):
        """Test that __all__ contains only function names, not modules"""
        import backend.analyzer as analyzer

        exported = getattr(analyzer, '__all__', [])

        # All items in __all__ should be functions (lowercase with underscores)
        for name in exported:
            # Check naming convention (functions use lowercase_with_underscores)
            assert '_' in name or name.islower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
