"""
Subscription-related request and response schemas
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from models.subscription import SubscriptionTier


class SubscriptionPlanResponse(BaseModel):
    """Response schema for subscription plan"""
    plan_id: str = Field(..., description="Plan identifier")
    name: str = Field(..., description="Plan name")
    tier: str = Field(..., description="Tier: free or premium")
    price_monthly: int = Field(..., description="Monthly price in KRW")
    price_yearly: Optional[int] = Field(None, description="Yearly price in KRW")
    features: dict = Field(..., description="Feature details")
    description: str = Field(..., description="Plan description")
    popular: bool = Field(default=False, description="Popular flag")


class SubscriptionPlansResponse(BaseModel):
    """Response for listing all subscription plans"""
    success: bool = Field(default=True, description="Success flag")
    data: List[SubscriptionPlanResponse] = Field(..., description="List of plans")


class UserSubscriptionResponse(BaseModel):
    """Response schema for user subscription status"""
    success: bool = Field(default=True, description="Success flag")
    data: dict = Field(..., description="Subscription data")


class UpgradeRequest(BaseModel):
    """Request to upgrade subscription"""
    plan_id: str = Field(..., description="Target plan ID")
    payment_method: Optional[str] = Field(
        "mock",
        description="Payment method (mock for now)"
    )


class UpgradeResponse(BaseModel):
    """Response for upgrade request"""
    success: bool = Field(..., description="Upgrade success")
    message: str = Field(..., description="Result message")
    data: Optional[dict] = Field(None, description="Updated subscription data")


class CancelSubscriptionResponse(BaseModel):
    """Response for cancellation request"""
    success: bool = Field(..., description="Cancellation success")
    message: str = Field(..., description="Result message")


class UsageStatsResponse(BaseModel):
    """Response for usage statistics"""
    success: bool = Field(default=True, description="Success flag")
    data: dict = Field(..., description="Usage statistics")


class ExportRequest(BaseModel):
    """Request for data export"""
    export_type: str = Field(..., description="Export type: csv or pdf")
    filters: Optional[dict] = Field(None, description="Data filters")
    fields: Optional[List[str]] = Field(None, description="Fields to include")


class ExportResponse(BaseModel):
    """Response for export request"""
    success: bool = Field(..., description="Export success")
    download_url: Optional[str] = Field(None, description="Download URL")
    filename: str = Field(..., description="Generated filename")
    message: Optional[str] = Field(None, description="Status message")
