"""
Payment router - handles payment operations
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import structlog

from auth.database import get_db
from auth.dependencies import get_current_user
from auth.models import User, Payment, PaymentStatus, Subscription, SubscriptionStatus, SubscriptionTier
from schemas.payment import (
    PaymentCreateRequest,
    PaymentCreateResponse,
    PaymentVerifyRequest,
    PaymentVerifyResponse,
    PaymentHistoryResponse,
    PaymentHistoryItem,
    PaymentWebhookPayload
)
from services.payment_service import PaymentService

logger = structlog.get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/payments",
    tags=["payments"],
)


# Initialize payment service
payment_service = PaymentService()


@router.post(
    "/create",
    response_model=PaymentCreateResponse,
    summary="Create payment intent",
    description="Create a new payment intent for subscription"
)
async def create_payment(
    request: PaymentCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a payment intent

    - **amount**: Payment amount (must be positive)
    - **currency**: Currency code (default: KRW)
    - **payment_method**: Payment method (card, bank_transfer)
    """
    try:
        logger.info(
            "create_payment_request",
            user_id=current_user.id,
            amount=float(request.amount),
            currency=request.currency,
            payment_method=request.payment_method
        )

        # Create payment intent with PortOne
        payment_intent = await payment_service.create_payment(
            user_id=current_user.id,
            amount=request.amount,
            currency=request.currency,
            payment_method=request.payment_method
        )

        # Create payment record in database
        payment = Payment(
            user_id=current_user.id,
            amount=request.amount,
            currency=request.currency,
            status=PaymentStatus.PENDING,
            payment_method=request.payment_method,
            portone_payment_id=payment_intent["portone_payment_id"]
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)

        logger.info(
            "payment_created",
            payment_id=payment.id,
            portone_payment_id=payment.portone_payment_id
        )

        return PaymentCreateResponse(
            success=True,
            payment_id=str(payment.id),
            portone_payment_id=payment.portone_payment_id,
            amount=payment.amount,
            currency=payment.currency,
            status=payment.status.value,
            created_at=payment.created_at
        )

    except Exception as e:
        logger.error(
            "create_payment_error",
            user_id=current_user.id,
            error=str(e)
        )
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create payment: {str(e)}"
        )


@router.post(
    "/verify",
    response_model=PaymentVerifyResponse,
    summary="Verify payment",
    description="Verify payment status and activate subscription"
)
async def verify_payment(
    request: PaymentVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify payment and activate subscription

    - **portone_payment_id**: PortOne payment ID
    - **webhook_signature**: Optional webhook signature for verification
    """
    try:
        logger.info(
            "verify_payment_request",
            user_id=current_user.id,
            portone_payment_id=request.portone_payment_id
        )

        # Find payment record
        payment = db.query(Payment).filter(
            Payment.portone_payment_id == request.portone_payment_id,
            Payment.user_id == current_user.id
        ).first()

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

        # Verify payment with PortOne
        verification_result = await payment_service.verify_and_complete_payment(
            portone_payment_id=request.portone_payment_id,
            webhook_signature=request.webhook_signature
        )

        # Update payment status
        payment.status = PaymentStatus.COMPLETED
        payment.receipt_number = verification_result.get("receipt_number")
        payment.completed_at = verification_result.get("completed_at")

        # Activate subscription
        subscription_expires_at = datetime.utcnow() + timedelta(days=30)

        current_user.subscription_tier = SubscriptionTier.PREMIUM
        current_user.subscription_expires_at = subscription_expires_at

        # Create subscription record
        subscription = Subscription(
            user_id=current_user.id,
            plan="premium_monthly",
            amount=payment.amount,
            started_at=datetime.utcnow(),
            expires_at=subscription_expires_at,
            status=SubscriptionStatus.ACTIVE
        )
        db.add(subscription)

        db.commit()
        db.refresh(payment)

        logger.info(
            "payment_verified_subscription_activated",
            payment_id=payment.id,
            user_id=current_user.id,
            subscription_expires_at=subscription_expires_at.isoformat()
        )

        return PaymentVerifyResponse(
            success=True,
            payment_id=str(payment.id),
            status=payment.status.value,
            receipt_number=payment.receipt_number,
            completed_at=payment.completed_at,
            subscription_activated=True,
            subscription_expires_at=subscription_expires_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "verify_payment_error",
            user_id=current_user.id,
            portone_payment_id=request.portone_payment_id,
            error=str(e)
        )
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify payment: {str(e)}"
        )


@router.get(
    "/history",
    response_model=PaymentHistoryResponse,
    summary="Get payment history",
    description="Get payment history for current user"
)
async def get_payment_history(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get payment history

    - **limit**: Maximum number of records to return (default: 50)
    - **offset**: Number of records to skip (default: 0)
    """
    try:
        logger.info(
            "get_payment_history",
            user_id=current_user.id,
            limit=limit,
            offset=offset
        )

        # Query payments
        payments_query = db.query(Payment).filter(
            Payment.user_id == current_user.id
        ).order_by(Payment.created_at.desc())

        total = payments_query.count()
        payments = payments_query.limit(limit).offset(offset).all()

        # Convert to response schema
        payment_items = [
            PaymentHistoryItem(
                id=p.id,
                amount=p.amount,
                currency=p.currency,
                status=p.status.value,
                payment_method=p.payment_method,
                receipt_number=p.receipt_number,
                created_at=p.created_at,
                completed_at=p.completed_at
            )
            for p in payments
        ]

        return PaymentHistoryResponse(
            success=True,
            payments=payment_items,
            total=total
        )

    except Exception as e:
        logger.error(
            "get_payment_history_error",
            user_id=current_user.id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get payment history: {str(e)}"
        )


@router.post(
    "/webhook",
    summary="Payment webhook",
    description="Webhook endpoint for PortOne payment notifications"
)
async def payment_webhook(
    payload: PaymentWebhookPayload,
    db: Session = Depends(get_db)
):
    """
    Handle payment webhook from PortOne

    This endpoint receives payment status updates from PortOne.
    In production, verify the webhook signature.
    """
    try:
        logger.info(
            "payment_webhook_received",
            payment_id=payload.payment_id,
            status=payload.status
        )

        # Process webhook
        webhook_result = await payment_service.process_webhook(
            payload.dict()
        )

        # Find payment by portone_payment_id
        payment = db.query(Payment).filter(
            Payment.portone_payment_id == payload.payment_id
        ).first()

        if not payment:
            logger.warning(
                "webhook_payment_not_found",
                portone_payment_id=payload.payment_id
            )
            return {"success": False, "error": "Payment not found"}

        # Update payment status
        if payload.status == "completed":
            payment.status = PaymentStatus.COMPLETED
            payment.receipt_number = payload.receipt_number
            payment.completed_at = datetime.utcnow()

            # Note: Subscription activation should be handled in verify endpoint
            # This webhook is for notification purposes only

        elif payload.status == "failed":
            payment.status = PaymentStatus.FAILED

        db.commit()

        logger.info(
            "webhook_processed",
            payment_id=payment.id,
            status=payment.status.value
        )

        return {"success": True, "payment_id": payment.id}

    except Exception as e:
        logger.error(
            "webhook_processing_error",
            payment_id=payload.payment_id,
            error=str(e)
        )
        db.rollback()
        return {"success": False, "error": str(e)}
