"""
Payment schemas for request/response validation
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class PaymentCreateRequest(BaseModel):
    """Payment creation request schema"""
    amount: Decimal = Field(..., description="Payment amount", gt=0)
    currency: str = Field(default="KRW", description="Currency code")
    payment_method: str = Field(..., description="Payment method (card, bank_transfer)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": 9900,
                "currency": "KRW",
                "payment_method": "card"
            }
        }
    )


class PaymentCreateResponse(BaseModel):
    """Payment creation response schema"""
    success: bool
    payment_id: str
    portone_payment_id: str
    amount: Decimal
    currency: str
    status: str
    created_at: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "payment_id": "1",
                "portone_payment_id": "mock_pay_20260208_abcd1234",
                "amount": 9900,
                "currency": "KRW",
                "status": "pending",
                "created_at": "2026-02-08T12:00:00"
            }
        }
    )


class PaymentVerifyRequest(BaseModel):
    """Payment verification request schema"""
    portone_payment_id: str = Field(..., description="PortOne payment ID")
    webhook_signature: Optional[str] = Field(None, description="Webhook signature for verification")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "portone_payment_id": "mock_pay_20260208_abcd1234",
                "webhook_signature": "mock_signature_xyz"
            }
        }
    )


class PaymentVerifyResponse(BaseModel):
    """Payment verification response schema"""
    success: bool
    payment_id: str
    status: str
    receipt_number: Optional[str] = None
    completed_at: Optional[datetime] = None
    subscription_activated: bool = False
    subscription_expires_at: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "payment_id": "1",
                "status": "completed",
                "receipt_number": "RCP20260208-ABC123",
                "completed_at": "2026-02-08T12:00:05",
                "subscription_activated": True,
                "subscription_expires_at": "2026-03-08T12:00:05"
            }
        }
    )


class PaymentHistoryItem(BaseModel):
    """Single payment history item"""
    id: int
    amount: Decimal
    currency: str
    status: str
    payment_method: Optional[str] = None
    receipt_number: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaymentHistoryResponse(BaseModel):
    """Payment history response schema"""
    success: bool
    payments: list[PaymentHistoryItem]
    total: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "total": 2,
                "payments": [
                    {
                        "id": 1,
                        "amount": 9900,
                        "currency": "KRW",
                        "status": "completed",
                        "payment_method": "card",
                        "receipt_number": "RCP20260208-ABC123",
                        "created_at": "2026-02-08T12:00:00",
                        "completed_at": "2026-02-08T12:00:05"
                    }
                ]
            }
        }
    )


class PaymentWebhookPayload(BaseModel):
    """Webhook payload from PortOne"""
    payment_id: str
    status: str
    amount: Decimal
    currency: str
    receipt_number: Optional[str] = None
    signature: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_id": "mock_pay_20260208_abcd1234",
                "status": "completed",
                "amount": 9900,
                "currency": "KRW",
                "receipt_number": "RCP20260208-ABC123",
                "signature": "mock_signature_xyz"
            }
        }
    )
