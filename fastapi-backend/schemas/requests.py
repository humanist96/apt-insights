"""
Request schemas for API endpoints
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class BasicStatsRequest(BaseModel):
    """
    Request for basic statistics analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name (e.g., '강남구', '서초구')",
        examples=["강남구", "서초구 반포동"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date for filtering (YYYY-MM-DD format)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date for filtering (YYYY-MM-DD format)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class PriceTrendRequest(BaseModel):
    """
    Request for price trend analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )
    group_by: Optional[str] = Field(
        "month",
        description="Grouping period: 'day', 'week', 'month', 'year'",
        examples=["month"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')

    @field_validator('group_by')
    @classmethod
    def validate_group_by(cls, v: str) -> str:
        allowed = ['day', 'week', 'month', 'year']
        if v not in allowed:
            raise ValueError(f'group_by must be one of: {", ".join(allowed)}')
        return v


class RegionalAnalysisRequest(BaseModel):
    """
    Request for regional analysis
    """
    regions: Optional[List[str]] = Field(
        None,
        description="List of regions to analyze (if None, analyze all regions)",
        examples=[["강남구", "서초구", "송파구"]]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )
    top_n: Optional[int] = Field(
        10,
        description="Number of top regions to return",
        ge=1,
        le=100,
        examples=[10]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


# ========== Segmentation Requests ==========

class AreaAnalysisRequest(BaseModel):
    """
    Request for area-based analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )
    bins: Optional[List[float]] = Field(
        None,
        description="Custom area bins (if None, auto-generated)",
        examples=[[50, 60, 85, 100, 135]]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class FloorAnalysisRequest(BaseModel):
    """
    Request for floor-based analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class BuildYearAnalysisRequest(BaseModel):
    """
    Request for build year analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class ApartmentAnalysisRequest(BaseModel):
    """
    Request for apartment-based analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )
    min_count: Optional[int] = Field(
        5,
        description="Minimum transaction count to include apartment",
        ge=1,
        examples=[5]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class ApartmentDetailRequest(BaseModel):
    """
    Request for specific apartment detail
    """
    apt_name: str = Field(
        ...,
        description="Apartment name to search",
        examples=["래미안"]
    )
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name (to distinguish same-name apartments)",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


# ========== Premium Requests ==========

class PricePerAreaRequest(BaseModel):
    """
    Request for price per area calculation
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class PricePerAreaTrendRequest(BaseModel):
    """
    Request for price per area trend analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class FloorPremiumRequest(BaseModel):
    """
    Request for floor premium analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class BuildingAgePremiumRequest(BaseModel):
    """
    Request for building age premium analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


# ========== Investment Requests ==========

class JeonseRatioRequest(BaseModel):
    """
    Request for jeonse ratio analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class GapInvestmentRequest(BaseModel):
    """
    Request for gap investment analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )
    min_gap_ratio: Optional[float] = Field(
        0.7,
        description="Minimum gap ratio (jeonse/sale ratio) to consider",
        ge=0.0,
        le=1.0,
        examples=[0.7]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class BargainSalesRequest(BaseModel):
    """
    Request for bargain sales detection
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )
    threshold_pct: Optional[float] = Field(
        10.0,
        description="Threshold percentage below average to consider bargain",
        ge=0.0,
        le=50.0,
        examples=[10.0]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


# ========== Market Requests ==========

class RentVsJeonseRequest(BaseModel):
    """
    Request for rent vs jeonse analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class DealingTypeRequest(BaseModel):
    """
    Request for dealing type analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class BuyerSellerTypeRequest(BaseModel):
    """
    Request for buyer/seller type analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class CancelledDealsRequest(BaseModel):
    """
    Request for cancelled deals analysis
    """
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class PeriodSummaryRequest(BaseModel):
    """
    Request for period summary
    """
    start_date: str = Field(
        ...,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: str = Field(
        ...,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class BaselineSummaryRequest(BaseModel):
    """
    Request for baseline summary (previous period)
    """
    start_date: str = Field(
        ...,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: str = Field(
        ...,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class ComparePeriodRequest(BaseModel):
    """
    Request for period comparison
    """
    current_start_date: str = Field(
        ...,
        description="Current period start date (YYYY-MM-DD)",
        examples=["2023-07-01"]
    )
    current_end_date: str = Field(
        ...,
        description="Current period end date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )
    previous_start_date: str = Field(
        ...,
        description="Previous period start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    previous_end_date: str = Field(
        ...,
        description="Previous period end date (YYYY-MM-DD)",
        examples=["2023-06-30"]
    )
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )
    current_label: Optional[str] = Field(
        "Current",
        description="Label for current period",
        examples=["Q2 2023"]
    )
    previous_label: Optional[str] = Field(
        "Previous",
        description="Label for previous period",
        examples=["Q1 2023"]
    )

    @field_validator('current_start_date', 'current_end_date', 'previous_start_date', 'previous_end_date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class MarketSignalsRequest(BaseModel):
    """
    Request for market signals detection
    """
    start_date: str = Field(
        ...,
        description="Start date (YYYY-MM-DD)",
        examples=["2023-01-01"]
    )
    end_date: str = Field(
        ...,
        description="End date (YYYY-MM-DD)",
        examples=["2023-12-31"]
    )
    region_filter: Optional[str] = Field(
        None,
        description="Filter by region name",
        examples=["강남구"]
    )

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
