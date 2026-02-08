"""
Test script for payment integration

This script tests the payment endpoints to ensure they work correctly.
Run this after starting the FastAPI backend.

Usage:
    python test_payment_integration.py
"""
import asyncio
import sys
from decimal import Decimal

try:
    from services.payment_service import MockPortOneService, PaymentService
except ImportError:
    print("❌ Error: Could not import payment services")
    print("Make sure you're running this from the fastapi-backend directory")
    sys.exit(1)


async def test_mock_portone_service():
    """Test MockPortOneService directly"""
    print("\n" + "="*60)
    print("Testing MockPortOneService")
    print("="*60)

    service = MockPortOneService()

    # Test 1: Create payment intent
    print("\n1. Creating payment intent...")
    try:
        result = await service.create_payment_intent(
            amount=Decimal("9900"),
            currency="KRW",
            payment_method="card",
            user_id=1
        )
        print(f"✅ Payment intent created:")
        print(f"   - PortOne Payment ID: {result['portone_payment_id']}")
        print(f"   - Status: {result['status']}")
        print(f"   - Amount: {result['amount']} {result['currency']}")

        portone_payment_id = result['portone_payment_id']

    except Exception as e:
        print(f"❌ Failed to create payment intent: {e}")
        return False

    # Test 2: Verify payment
    print("\n2. Verifying payment (this takes 2 seconds)...")
    try:
        result = await service.verify_payment(
            portone_payment_id=portone_payment_id
        )
        print(f"✅ Payment verified:")
        print(f"   - Status: {result['status']}")
        print(f"   - Receipt: {result['receipt_number']}")
        print(f"   - Completed: {result['completed_at']}")

    except Exception as e:
        print(f"❌ Failed to verify payment: {e}")
        return False

    # Test 3: Webhook signature verification
    print("\n3. Testing webhook signature verification...")
    try:
        payload = {"payment_id": portone_payment_id, "status": "completed"}
        signature = "test_signature"
        is_valid = service.verify_webhook_signature(payload, signature)
        print(f"✅ Signature verification: {'Valid' if is_valid else 'Invalid'}")

    except Exception as e:
        print(f"❌ Failed signature verification: {e}")
        return False

    # Test 4: Process webhook
    print("\n4. Testing webhook processing...")
    try:
        webhook_payload = {
            "payment_id": portone_payment_id,
            "status": "completed",
            "amount": 9900,
            "currency": "KRW",
            "receipt_number": "RCP20260208-TEST",
            "signature": "test_signature"
        }
        result = await service.process_webhook(webhook_payload)
        print(f"✅ Webhook processed:")
        print(f"   - Payment ID: {result['payment_id']}")
        print(f"   - Processed: {result['processed']}")

    except Exception as e:
        print(f"❌ Failed to process webhook: {e}")
        return False

    return True


async def test_payment_service():
    """Test PaymentService wrapper"""
    print("\n" + "="*60)
    print("Testing PaymentService")
    print("="*60)

    service = PaymentService()

    # Test 1: Create payment
    print("\n1. Creating payment...")
    try:
        result = await service.create_payment(
            user_id=1,
            amount=Decimal("9900"),
            currency="KRW",
            payment_method="card"
        )
        print(f"✅ Payment created:")
        print(f"   - PortOne Payment ID: {result['portone_payment_id']}")

        portone_payment_id = result['portone_payment_id']

    except Exception as e:
        print(f"❌ Failed to create payment: {e}")
        return False

    # Test 2: Verify and complete payment
    print("\n2. Verifying and completing payment (2 seconds)...")
    try:
        result = await service.verify_and_complete_payment(
            portone_payment_id=portone_payment_id
        )
        print(f"✅ Payment completed:")
        print(f"   - Status: {result['status']}")
        print(f"   - Receipt: {result['receipt_number']}")

    except Exception as e:
        print(f"❌ Failed to verify payment: {e}")
        return False

    return True


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Payment Integration Test Suite")
    print("="*60)
    print("\nThis will test the mock payment service implementation.")
    print("Note: All tests use mock data and don't require database connection.\n")

    # Run tests
    test1_passed = await test_mock_portone_service()
    test2_passed = await test_payment_service()

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"MockPortOneService: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"PaymentService: {'✅ PASSED' if test2_passed else '❌ FAILED'}")

    if test1_passed and test2_passed:
        print("\n🎉 All tests passed!")
        print("\nNext steps:")
        print("1. Run database migration: python -m auth.migrate_payments")
        print("2. Start backend: uvicorn main:app --reload")
        print("3. Test API endpoints at: http://localhost:8000/docs")
        return 0
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
