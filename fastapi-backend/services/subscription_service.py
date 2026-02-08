"""
Subscription management service
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import structlog

from models.subscription import (
    User,
    SubscriptionPlan,
    UserSubscription,
    SubscriptionTier,
)

logger = structlog.get_logger(__name__)


# Mock subscription plans
SUBSCRIPTION_PLANS: Dict[str, SubscriptionPlan] = {
    "free": SubscriptionPlan(
        plan_id="free",
        name="무료",
        tier=SubscriptionTier.FREE,
        price_monthly=0,
        price_yearly=0,
        description="기본 기능 제공",
        features={
            "api_calls_per_day": 10,
            "basic_analysis": True,
            "csv_export": False,
            "pdf_export": False,
            "portfolio_tracking": False,
            "price_alerts": False,
            "max_portfolios": 0,
            "max_alerts": 0,
        },
        popular=False,
    ),
    "premium": SubscriptionPlan(
        plan_id="premium",
        name="프리미엄",
        tier=SubscriptionTier.PREMIUM,
        price_monthly=9900,
        price_yearly=99000,
        description="모든 기능 무제한 이용",
        features={
            "api_calls_per_day": None,  # Unlimited
            "basic_analysis": True,
            "csv_export": True,
            "pdf_export": True,
            "portfolio_tracking": True,
            "price_alerts": True,
            "max_portfolios": 50,
            "max_alerts": 10,
        },
        popular=True,
    ),
}


# Mock user database (in-memory for now)
MOCK_USERS: Dict[str, User] = {
    "demo_user": User(
        user_id="demo_user",
        email="demo@example.com",
        tier=SubscriptionTier.FREE,
        created_at=datetime.now(),
        subscription_expires_at=None,
    ),
}


class SubscriptionService:
    """
    Subscription management service

    Handles:
    - Subscription plan management
    - User subscription status
    - Upgrade/downgrade operations
    - Feature access checks
    """

    def __init__(self):
        """Initialize subscription service"""
        self.logger = logger
        self.plans = SUBSCRIPTION_PLANS
        self.users = MOCK_USERS

    def get_all_plans(self) -> List[SubscriptionPlan]:
        """
        Get all available subscription plans

        Returns:
            List of subscription plans
        """
        return list(self.plans.values())

    def get_plan(self, plan_id: str) -> Optional[SubscriptionPlan]:
        """
        Get specific subscription plan

        Args:
            plan_id: Plan identifier

        Returns:
            Subscription plan or None
        """
        return self.plans.get(plan_id)

    def get_user(self, user_id: str) -> User:
        """
        Get user by ID (creates demo user if not exists)

        Args:
            user_id: User identifier

        Returns:
            User object
        """
        if user_id not in self.users:
            # Create demo user
            self.users[user_id] = User(
                user_id=user_id,
                email=f"{user_id}@example.com",
                tier=SubscriptionTier.FREE,
                created_at=datetime.now(),
            )
        return self.users[user_id]

    def get_user_subscription(self, user_id: str) -> UserSubscription:
        """
        Get user's subscription status

        Args:
            user_id: User identifier

        Returns:
            UserSubscription object
        """
        user = self.get_user(user_id)
        plan = self.plans[user.tier.value]

        return UserSubscription(
            user_id=user.user_id,
            tier=user.tier,
            plan_name=plan.name,
            expires_at=user.subscription_expires_at,
            api_calls_used=0,  # Will be populated from Redis
            api_calls_limit=plan.features.get("api_calls_per_day"),
            features=plan.features,
        )

    def upgrade_subscription(
        self,
        user_id: str,
        plan_id: str,
        payment_method: str = "mock",
    ) -> Dict[str, any]:
        """
        Upgrade user subscription (mock implementation)

        Args:
            user_id: User identifier
            plan_id: Target plan ID
            payment_method: Payment method (mock)

        Returns:
            Updated subscription data

        Raises:
            ValueError: If plan not found or invalid upgrade
        """
        user = self.get_user(user_id)
        target_plan = self.get_plan(plan_id)

        if not target_plan:
            raise ValueError(f"Plan not found: {plan_id}")

        # Mock payment processing
        self.logger.info(
            "subscription_upgrade",
            user_id=user_id,
            from_tier=user.tier.value,
            to_tier=target_plan.tier.value,
            payment_method=payment_method,
        )

        # Update user tier
        user.tier = target_plan.tier

        # Set expiration date (30 days for monthly)
        if target_plan.tier == SubscriptionTier.PREMIUM:
            user.subscription_expires_at = datetime.now() + timedelta(days=30)
        else:
            user.subscription_expires_at = None

        # Return updated subscription
        subscription = self.get_user_subscription(user_id)

        return {
            "tier": subscription.tier.value,
            "plan_name": subscription.plan_name,
            "expires_at": (
                subscription.expires_at.isoformat()
                if subscription.expires_at
                else None
            ),
            "features": subscription.features,
        }

    def cancel_subscription(self, user_id: str) -> bool:
        """
        Cancel user subscription (downgrade to free)

        Args:
            user_id: User identifier

        Returns:
            Success status
        """
        user = self.get_user(user_id)

        self.logger.info(
            "subscription_cancelled",
            user_id=user_id,
            previous_tier=user.tier.value,
        )

        # Downgrade to free tier
        user.tier = SubscriptionTier.FREE
        user.subscription_expires_at = None

        return True

    def check_feature_access(
        self,
        user_id: str,
        feature: str,
    ) -> bool:
        """
        Check if user has access to specific feature

        Args:
            user_id: User identifier
            feature: Feature name

        Returns:
            Access granted status
        """
        subscription = self.get_user_subscription(user_id)
        features = subscription.features

        # Check boolean features
        if feature in features:
            access = bool(features[feature])
            if not access:
                self.logger.warning(
                    "feature_access_denied",
                    user_id=user_id,
                    feature=feature,
                    tier=subscription.tier.value,
                )
            return access

        # Feature not in plan - default deny
        return False

    def is_premium_user(self, user_id: str) -> bool:
        """
        Check if user is premium subscriber

        Args:
            user_id: User identifier

        Returns:
            Premium status
        """
        user = self.get_user(user_id)
        return user.tier == SubscriptionTier.PREMIUM


# Singleton instance
_subscription_service: Optional[SubscriptionService] = None


def get_subscription_service() -> SubscriptionService:
    """
    Get subscription service singleton

    Returns:
        SubscriptionService instance
    """
    global _subscription_service
    if _subscription_service is None:
        _subscription_service = SubscriptionService()
    return _subscription_service
