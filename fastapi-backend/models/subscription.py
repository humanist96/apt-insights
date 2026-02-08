"""
Subscription-related database models
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SubscriptionTier(str, Enum):
    """Subscription tier enumeration"""
    FREE = "free"
    PREMIUM = "premium"


class User(BaseModel):
    """
    User model (mock - no database yet)
    In production, this would be a SQLAlchemy model
    """
    user_id: str = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User email")
    tier: SubscriptionTier = Field(
        default=SubscriptionTier.FREE,
        description="Current subscription tier"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Account creation timestamp"
    )
    subscription_expires_at: Optional[datetime] = Field(
        None,
        description="Premium subscription expiration date"
    )


class SubscriptionPlan(BaseModel):
    """
    Subscription plan definition
    """
    plan_id: str = Field(..., description="Plan identifier")
    name: str = Field(..., description="Plan name (Korean)")
    tier: SubscriptionTier = Field(..., description="Tier level")
    price_monthly: int = Field(..., description="Monthly price in KRW")
    price_yearly: Optional[int] = Field(None, description="Yearly price in KRW")
    features: dict = Field(..., description="Feature limits and capabilities")
    description: str = Field(..., description="Plan description")
    popular: bool = Field(default=False, description="Popular/recommended flag")


class UserSubscription(BaseModel):
    """
    User subscription status
    """
    user_id: str = Field(..., description="User identifier")
    tier: SubscriptionTier = Field(..., description="Current tier")
    plan_name: str = Field(..., description="Plan name")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")
    api_calls_used: int = Field(0, description="API calls used today")
    api_calls_limit: Optional[int] = Field(None, description="Daily API call limit (None = unlimited)")
    features: dict = Field(..., description="Available features")
