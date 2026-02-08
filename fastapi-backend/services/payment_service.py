"""
Payment service with mock PortOne integration
"""
import os
import asyncio
import secrets
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional
import structlog

logger = structlog.get_logger(__name__)


class MockPortOneService:
    """
    Mock PortOne payment gateway service

    In production, replace this with real PortOne API integration
    by setting PAYMENT_MODE=production in environment variables.
    """

    def __init__(self):
        self.api_key = os.getenv("PORTONE_API_KEY", "test_key")
        self.api_secret = os.getenv("PORTONE_API_SECRET", "test_secret")
        self.webhook_secret = os.getenv("PORTONE_WEBHOOK_SECRET", "test_webhook_secret")
        self.payment_mode = os.getenv("PAYMENT_MODE", "mock")

        if self.payment_mode == "production":
            logger.warning(
                "payment_mode_production",
                message="Production payment mode enabled - implement real PortOne integration"
            )

    async def create_payment_intent(
        self,
        amount: Decimal,
        currency: str,
        payment_method: str,
        user_id: int
    ) -> dict:
        """
        Create a payment intent

        Args:
            amount: Payment amount
            currency: Currency code (KRW)
            payment_method: Payment method (card, bank_transfer)
            user_id: User ID for tracking

        Returns:
            Payment intent data with portone_payment_id
        """
        logger.info(
            "creating_payment_intent",
            amount=float(amount),
            currency=currency,
            payment_method=payment_method,
            user_id=user_id,
            mode=self.payment_mode
        )

        if self.payment_mode == "production":
            raise NotImplementedError("Real PortOne integration not implemented")

        # Mock implementation
        await asyncio.sleep(0.5)  # Simulate API latency

        portone_payment_id = f"mock_pay_{datetime.now().strftime('%Y%m%d')}_{secrets.token_hex(8)}"

        return {
            "portone_payment_id": portone_payment_id,
            "status": "pending",
            "amount": float(amount),
            "currency": currency,
            "payment_method": payment_method,
            "created_at": datetime.utcnow()
        }

    async def verify_payment(
        self,
        portone_payment_id: str,
        webhook_signature: Optional[str] = None
    ) -> dict:
        """
        Verify payment status with PortOne

        Args:
            portone_payment_id: PortOne payment ID
            webhook_signature: Webhook signature for verification

        Returns:
            Payment verification result
        """
        logger.info(
            "verifying_payment",
            portone_payment_id=portone_payment_id,
            has_signature=webhook_signature is not None,
            mode=self.payment_mode
        )

        if self.payment_mode == "production":
            raise NotImplementedError("Real PortOne integration not implemented")

        # Mock implementation - simulate processing delay
        await asyncio.sleep(2.0)  # 2 second delay for realism

        # Mock: always succeed
        receipt_number = f"RCP{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(6).upper()}"

        return {
            "status": "completed",
            "receipt_number": receipt_number,
            "completed_at": datetime.utcnow(),
            "verified": True
        }

    def verify_webhook_signature(
        self,
        payload: dict,
        signature: str
    ) -> bool:
        """
        Verify webhook signature from PortOne

        Args:
            payload: Webhook payload
            signature: Signature to verify

        Returns:
            True if signature is valid
        """
        if self.payment_mode == "production":
            # In production, implement actual signature verification
            # using HMAC-SHA256 with webhook_secret
            raise NotImplementedError("Real signature verification not implemented")

        # Mock: always valid
        return True

    async def process_webhook(
        self,
        payload: dict
    ) -> dict:
        """
        Process webhook from PortOne

        Args:
            payload: Webhook payload

        Returns:
            Processed webhook data
        """
        logger.info(
            "processing_webhook",
            payment_id=payload.get("payment_id"),
            status=payload.get("status"),
            mode=self.payment_mode
        )

        if self.payment_mode == "production":
            raise NotImplementedError("Real webhook processing not implemented")

        # Mock implementation
        signature = payload.get("signature", "")
        if not self.verify_webhook_signature(payload, signature):
            raise ValueError("Invalid webhook signature")

        return {
            "payment_id": payload.get("payment_id"),
            "status": payload.get("status"),
            "amount": payload.get("amount"),
            "currency": payload.get("currency"),
            "receipt_number": payload.get("receipt_number"),
            "processed": True
        }

    async def refund_payment(
        self,
        portone_payment_id: str,
        amount: Optional[Decimal] = None,
        reason: str = ""
    ) -> dict:
        """
        Refund a payment

        Args:
            portone_payment_id: PortOne payment ID
            amount: Refund amount (None for full refund)
            reason: Refund reason

        Returns:
            Refund result
        """
        logger.info(
            "refunding_payment",
            portone_payment_id=portone_payment_id,
            amount=float(amount) if amount else None,
            reason=reason,
            mode=self.payment_mode
        )

        if self.payment_mode == "production":
            raise NotImplementedError("Real refund not implemented")

        # Mock implementation
        await asyncio.sleep(1.0)

        return {
            "status": "refunded",
            "refund_id": f"mock_refund_{secrets.token_hex(8)}",
            "refunded_amount": float(amount) if amount else None,
            "refunded_at": datetime.utcnow()
        }


class PaymentService:
    """
    Payment service for handling payment operations
    """

    def __init__(self, portone_service: Optional[MockPortOneService] = None):
        self.portone = portone_service or MockPortOneService()

    async def create_payment(
        self,
        user_id: int,
        amount: Decimal,
        currency: str,
        payment_method: str
    ) -> dict:
        """
        Create a new payment

        Args:
            user_id: User ID
            amount: Payment amount
            currency: Currency code
            payment_method: Payment method

        Returns:
            Payment creation result
        """
        return await self.portone.create_payment_intent(
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            user_id=user_id
        )

    async def verify_and_complete_payment(
        self,
        portone_payment_id: str,
        webhook_signature: Optional[str] = None
    ) -> dict:
        """
        Verify and complete a payment

        Args:
            portone_payment_id: PortOne payment ID
            webhook_signature: Webhook signature

        Returns:
            Verification result
        """
        return await self.portone.verify_payment(
            portone_payment_id=portone_payment_id,
            webhook_signature=webhook_signature
        )

    async def process_webhook(self, payload: dict) -> dict:
        """
        Process payment webhook

        Args:
            payload: Webhook payload

        Returns:
            Processed webhook data
        """
        return await self.portone.process_webhook(payload)

    async def refund_payment(
        self,
        portone_payment_id: str,
        amount: Optional[Decimal] = None,
        reason: str = ""
    ) -> dict:
        """
        Refund a payment

        Args:
            portone_payment_id: PortOne payment ID
            amount: Refund amount
            reason: Refund reason

        Returns:
            Refund result
        """
        return await self.portone.refund_payment(
            portone_payment_id=portone_payment_id,
            amount=amount,
            reason=reason
        )
