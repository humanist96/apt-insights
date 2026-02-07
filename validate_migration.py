"""
Migration Validation Script

Verifies that all migrated code works correctly
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test that all imports work"""
    print("🔍 Testing imports...")

    try:
        from api_01.api_01_silv_trade import SilvTradeAPI
        from api_02.api_02_apt_trade import AptTradeAPI
        from api_03.api_03_apt_trade_dev import AptTradeDevAPI
        from api_04.api_04_apt_rent import AptRentAPI
        from base_api_client import BaseAPIClient
        from logger import get_logger, APILogger
        from config import settings

        print("  ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False


def test_api_clients():
    """Test that API clients can be instantiated"""
    print("\n🏗️  Testing API client instantiation...")

    from api_01.api_01_silv_trade import SilvTradeAPI
    from api_02.api_02_apt_trade import AptTradeAPI
    from api_03.api_03_apt_trade_dev import AptTradeDevAPI
    from api_04.api_04_apt_rent import AptRentAPI

    clients = {
        'API 01 (분양권)': SilvTradeAPI,
        'API 02 (매매)': AptTradeAPI,
        'API 03 (매매 상세)': AptTradeDevAPI,
        'API 04 (전월세)': AptRentAPI,
    }

    all_success = True
    for name, ClientClass in clients.items():
        try:
            client = ClientClass()
            assert hasattr(client, 'get_trade_data')
            assert hasattr(client, 'get_trade_data_parsed')
            assert hasattr(client, 'get_all_pages')
            print(f"  ✅ {name}: OK")
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            all_success = False

    return all_success


def test_backward_compatibility():
    """Test backward compatibility"""
    print("\n🔄 Testing backward compatibility...")

    try:
        # Test that SERVICE_KEY is still available
        from config import SERVICE_KEY
        assert SERVICE_KEY is not None
        print("  ✅ SERVICE_KEY backward compatibility: OK")

        # Test that API interface is unchanged
        from api_01.api_01_silv_trade import SilvTradeAPI
        api = SilvTradeAPI()

        # Old methods
        assert hasattr(api, 'get_trade_data')
        assert hasattr(api, 'parse_response')
        assert hasattr(api, 'get_trade_data_parsed')

        # New methods
        assert hasattr(api, 'get_all_pages')

        print("  ✅ API interface compatibility: OK")
        return True
    except Exception as e:
        print(f"  ❌ Backward compatibility failed: {e}")
        return False


def test_logging_integration():
    """Test logging system integration"""
    print("\n📝 Testing logging integration...")

    try:
        from logger import get_logger, APILogger

        # Just test that logging doesn't crash
        logger = get_logger("test")
        logger.info("test_message", value=42)

        api_logger = APILogger("test_api")
        api_logger.log_request("GET", "https://test.com", {"key": "value"})

        print("  ✅ Logging system: OK")
        return True

    except Exception as e:
        print(f"  ❌ Logging failed: {e}")
        return False


def test_file_structure():
    """Test that file structure is correct"""
    print("\n📁 Testing file structure...")

    required_files = [
        'base_api_client.py',
        'logger.py',
        'config.py',
        '.env',
        '.env.example',
        '.gitignore',
        'api_01/api_01_silv_trade.py',
        'api_02/api_02_apt_trade.py',
        'api_03/api_03_apt_trade_dev.py',
        'api_04/api_04_apt_rent.py',
        'tests/test_base_api_client.py',
        'tests/test_integration.py',
    ]

    backup_files = [
        'api_01/api_01_silv_trade.old.py',
        'api_02/api_02_apt_trade.old.py',
        'api_03/api_03_apt_trade_dev.old.py',
        'api_04/api_04_apt_rent.old.py',
    ]

    all_exist = True

    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")
            all_exist = False

    print(f"\n📦 Backup files:")
    for file in backup_files:
        path = Path(file)
        if path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} (not found - may not have existed)")

    return all_exist


def main():
    """Run all validation tests"""
    print("="*60)
    print("🧪 Migration Validation")
    print("="*60)

    results = {
        'Imports': test_imports(),
        'API Clients': test_api_clients(),
        'Backward Compatibility': test_backward_compatibility(),
        'Logging Integration': test_logging_integration(),
        'File Structure': test_file_structure(),
    }

    print("\n" + "="*60)
    print("📊 Validation Results")
    print("="*60)

    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False

    print("="*60)

    if all_passed:
        print("\n🎉 All validation tests passed!")
        print("✅ Migration successful!")
        return 0
    else:
        print("\n⚠️  Some validation tests failed")
        print("Please review the issues above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
