"""
Test script for new analyzer endpoints
Tests all 20 newly implemented endpoints
"""
import asyncio
from datetime import datetime
from services.analyzer_service import AnalyzerService


async def test_all_endpoints():
    """Test all new endpoints"""
    service = AnalyzerService()
    results = {}

    print("=" * 80)
    print("TESTING ALL 20 NEW ANALYZER ENDPOINTS")
    print("=" * 80)

    # Common test parameters
    region_filter = "강남구"
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    # ========== GROUP 1: Segmentation (5 endpoints) ==========
    print("\n" + "=" * 80)
    print("GROUP 1: SEGMENTATION ANALYSIS (5 endpoints)")
    print("=" * 80)

    # 1. By Area
    print("\n1. Testing get_area_analysis...")
    try:
        result, meta = service.get_area_analysis(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['area_analysis'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['area_analysis'] = 'FAIL'

    # 2. By Floor
    print("\n2. Testing get_floor_analysis...")
    try:
        result, meta = service.get_floor_analysis(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['floor_analysis'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['floor_analysis'] = 'FAIL'

    # 3. By Build Year
    print("\n3. Testing get_build_year_analysis...")
    try:
        result, meta = service.get_build_year_analysis(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['build_year_analysis'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['build_year_analysis'] = 'FAIL'

    # 4. By Apartment
    print("\n4. Testing get_apartment_analysis...")
    try:
        result, meta = service.get_apartment_analysis(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date,
            min_count=5
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['apartment_analysis'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['apartment_analysis'] = 'FAIL'

    # 5. Apartment Detail
    print("\n5. Testing get_apartment_detail...")
    try:
        result, meta = service.get_apartment_detail(
            apt_name="래미안",
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Found: {result.get('found', False)}")
        results['apartment_detail'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['apartment_detail'] = 'FAIL'

    # ========== GROUP 2: Premium Analysis (4 endpoints) ==========
    print("\n" + "=" * 80)
    print("GROUP 2: PREMIUM ANALYSIS (4 endpoints)")
    print("=" * 80)

    # 6. Price Per Area
    print("\n6. Testing get_price_per_area...")
    try:
        result, meta = service.get_price_per_area(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['price_per_area'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['price_per_area'] = 'FAIL'

    # 7. Price Per Area Trend
    print("\n7. Testing get_price_per_area_trend...")
    try:
        result, meta = service.get_price_per_area_trend(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['price_per_area_trend'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['price_per_area_trend'] = 'FAIL'

    # 8. Floor Premium
    print("\n8. Testing get_floor_premium...")
    try:
        result, meta = service.get_floor_premium(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['floor_premium'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['floor_premium'] = 'FAIL'

    # 9. Building Age Premium
    print("\n9. Testing get_building_age_premium...")
    try:
        result, meta = service.get_building_age_premium(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['building_age_premium'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['building_age_premium'] = 'FAIL'

    # ========== GROUP 3: Investment (3 endpoints) ==========
    print("\n" + "=" * 80)
    print("GROUP 3: INVESTMENT ANALYSIS (3 endpoints)")
    print("=" * 80)

    # 10. Jeonse Ratio
    print("\n10. Testing get_jeonse_ratio...")
    try:
        result, meta = service.get_jeonse_ratio(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['jeonse_ratio'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['jeonse_ratio'] = 'FAIL'

    # 11. Gap Investment
    print("\n11. Testing get_gap_investment...")
    try:
        result, meta = service.get_gap_investment(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date,
            min_gap_ratio=0.7
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['gap_investment'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['gap_investment'] = 'FAIL'

    # 12. Bargain Sales
    print("\n12. Testing get_bargain_sales...")
    try:
        result, meta = service.get_bargain_sales(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date,
            threshold_pct=10.0
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['bargain_sales'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['bargain_sales'] = 'FAIL'

    # ========== GROUP 4: Market Signals (8 endpoints) ==========
    print("\n" + "=" * 80)
    print("GROUP 4: MARKET SIGNALS (8 endpoints)")
    print("=" * 80)

    # 13. Rent vs Jeonse
    print("\n13. Testing get_rent_vs_jeonse...")
    try:
        result, meta = service.get_rent_vs_jeonse(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['rent_vs_jeonse'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['rent_vs_jeonse'] = 'FAIL'

    # 14. Dealing Type
    print("\n14. Testing get_dealing_type...")
    try:
        result, meta = service.get_dealing_type(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['dealing_type'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['dealing_type'] = 'FAIL'

    # 15. Buyer Seller Type
    print("\n15. Testing get_buyer_seller_type...")
    try:
        result, meta = service.get_buyer_seller_type(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['buyer_seller_type'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['buyer_seller_type'] = 'FAIL'

    # 16. Cancelled Deals
    print("\n16. Testing get_cancelled_deals...")
    try:
        result, meta = service.get_cancelled_deals(
            region_filter=region_filter,
            start_date=start_date,
            end_date=end_date
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['cancelled_deals'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['cancelled_deals'] = 'FAIL'

    # 17. Period Summary
    print("\n17. Testing get_period_summary...")
    try:
        result, meta = service.get_period_summary(
            start_date=start_date,
            end_date=end_date,
            region_filter=region_filter
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['period_summary'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['period_summary'] = 'FAIL'

    # 18. Baseline Summary
    print("\n18. Testing get_baseline_summary...")
    try:
        result, meta = service.get_baseline_summary(
            start_date=start_date,
            end_date=end_date,
            region_filter=region_filter
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['baseline_summary'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['baseline_summary'] = 'FAIL'

    # 19. Period Comparison
    print("\n19. Testing get_period_comparison...")
    try:
        result, meta = service.get_period_comparison(
            current_start_date="2023-07-01",
            current_end_date="2023-12-31",
            previous_start_date="2023-01-01",
            previous_end_date="2023-06-30",
            region_filter=region_filter,
            current_label="H2 2023",
            previous_label="H1 2023"
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['period_comparison'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['period_comparison'] = 'FAIL'

    # 20. Market Signals
    print("\n20. Testing get_market_signals...")
    try:
        result, meta = service.get_market_signals(
            start_date=start_date,
            end_date=end_date,
            region_filter=region_filter
        )
        print(f"   ✓ Success - Filtered: {meta['filtered_records']} records")
        print(f"   Data keys: {list(result.keys())}")
        results['market_signals'] = 'PASS'
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results['market_signals'] = 'FAIL'

    # ========== Summary ==========
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for v in results.values() if v == 'PASS')
    failed = sum(1 for v in results.values() if v == 'FAIL')

    print(f"\nTotal Tests: {len(results)}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")

    if failed > 0:
        print("\nFailed tests:")
        for name, status in results.items():
            if status == 'FAIL':
                print(f"  - {name}")

    print("\n" + "=" * 80)

    return results


if __name__ == "__main__":
    asyncio.run(test_all_endpoints())
