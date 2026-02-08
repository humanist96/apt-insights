"""
Subscription management API endpoints
"""
from fastapi import APIRouter, HTTPException, status, Header
from typing import Optional
import structlog

from schemas.subscription import (
    SubscriptionPlansResponse,
    SubscriptionPlanResponse,
    UserSubscriptionResponse,
    UpgradeRequest,
    UpgradeResponse,
    CancelSubscriptionResponse,
    UsageStatsResponse,
)
from services.subscription_service import get_subscription_service
from services.usage_tracking import get_usage_tracking_service

logger = structlog.get_logger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/subscriptions",
    tags=["subscriptions"],
    responses={
        500: {"description": "Internal server error"},
        401: {"description": "Unauthorized"},
    },
)

# Services
subscription_service = get_subscription_service()
usage_service = get_usage_tracking_service()


def get_user_id(x_user_id: Optional[str] = Header(None)) -> str:
    """
    Extract user ID from header (temporary auth method)

    Args:
        x_user_id: User ID from header

    Returns:
        User ID (defaults to demo_user)
    """
    return x_user_id or "demo_user"


@router.get(
    "/plans",
    response_model=SubscriptionPlansResponse,
    summary="List subscription plans",
    description="Get all available subscription plans with features and pricing",
)
async def list_plans() -> SubscriptionPlansResponse:
    """
    List all subscription plans

    Returns:
        List of available plans
    """
    try:
        plans = subscription_service.get_all_plans()

        # Convert to response format
        plan_responses = [
            SubscriptionPlanResponse(
                plan_id=plan.plan_id,
                name=plan.name,
                tier=plan.tier.value,
                price_monthly=plan.price_monthly,
                price_yearly=plan.price_yearly,
                features=plan.features,
                description=plan.description,
                popular=plan.popular,
            )
            for plan in plans
        ]

        return SubscriptionPlansResponse(
            success=True,
            data=plan_responses,
        )

    except Exception as e:
        logger.error("list_plans_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve plans: {str(e)}",
        )


@router.get(
    "/current",
    response_model=UserSubscriptionResponse,
    summary="Get current subscription",
    description="Get the current user's subscription status and features",
)
async def get_current_subscription(
    user_id: str = Header(None, alias="X-User-Id"),
) -> UserSubscriptionResponse:
    """
    Get current user subscription

    Args:
        user_id: User ID from header

    Returns:
        User subscription details
    """
    try:
        user_id = user_id or "demo_user"

        subscription = subscription_service.get_user_subscription(user_id)
        usage_stats = usage_service.get_usage_stats(
            user_id,
            subscription.api_calls_limit,
        )

        data = {
            "user_id": subscription.user_id,
            "tier": subscription.tier.value,
            "plan_name": subscription.plan_name,
            "expires_at": (
                subscription.expires_at.isoformat()
                if subscription.expires_at
                else None
            ),
            "features": subscription.features,
            "usage": usage_stats,
        }

        logger.info("subscription_retrieved", user_id=user_id)

        return UserSubscriptionResponse(
            success=True,
            data=data,
        )

    except Exception as e:
        logger.error("get_subscription_error", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve subscription: {str(e)}",
        )


@router.post(
    "/upgrade",
    response_model=UpgradeResponse,
    summary="Upgrade subscription",
    description="Upgrade to premium plan (mock payment for now)",
)
async def upgrade_subscription(
    request: UpgradeRequest,
    user_id: str = Header(None, alias="X-User-Id"),
) -> UpgradeResponse:
    """
    Upgrade user subscription

    Args:
        request: Upgrade request with plan_id
        user_id: User ID from header

    Returns:
        Updated subscription details
    """
    try:
        user_id = user_id or "demo_user"

        # Validate plan
        plan = subscription_service.get_plan(request.plan_id)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plan not found: {request.plan_id}",
            )

        # Process upgrade
        updated_data = subscription_service.upgrade_subscription(
            user_id=user_id,
            plan_id=request.plan_id,
            payment_method=request.payment_method,
        )

        logger.info(
            "subscription_upgraded",
            user_id=user_id,
            plan_id=request.plan_id,
        )

        return UpgradeResponse(
            success=True,
            message=f"{plan.name} 플랜으로 업그레이드되었습니다",
            data=updated_data,
        )

    except ValueError as e:
        logger.warning("upgrade_failed", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error("upgrade_error", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upgrade subscription: {str(e)}",
        )


@router.post(
    "/cancel",
    response_model=CancelSubscriptionResponse,
    summary="Cancel subscription",
    description="Cancel premium subscription and revert to free plan",
)
async def cancel_subscription(
    user_id: str = Header(None, alias="X-User-Id"),
) -> CancelSubscriptionResponse:
    """
    Cancel user subscription

    Args:
        user_id: User ID from header

    Returns:
        Cancellation confirmation
    """
    try:
        user_id = user_id or "demo_user"

        success = subscription_service.cancel_subscription(user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to cancel subscription",
            )

        logger.info("subscription_cancelled", user_id=user_id)

        return CancelSubscriptionResponse(
            success=True,
            message="구독이 취소되었습니다. 무료 플랜으로 전환됩니다.",
        )

    except Exception as e:
        logger.error("cancel_error", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel subscription: {str(e)}",
        )


@router.get(
    "/usage",
    response_model=UsageStatsResponse,
    summary="Get usage statistics",
    description="Get current API usage statistics for the user",
)
async def get_usage_stats(
    user_id: str = Header(None, alias="X-User-Id"),
) -> UsageStatsResponse:
    """
    Get usage statistics

    Args:
        user_id: User ID from header

    Returns:
        Usage statistics
    """
    try:
        user_id = user_id or "demo_user"

        subscription = subscription_service.get_user_subscription(user_id)
        usage_stats = usage_service.get_usage_stats(
            user_id,
            subscription.api_calls_limit,
        )

        logger.debug("usage_stats_retrieved", user_id=user_id)

        return UsageStatsResponse(
            success=True,
            data=usage_stats,
        )

    except Exception as e:
        logger.error("usage_stats_error", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve usage stats: {str(e)}",
        )
