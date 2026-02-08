"""
Response schemas for API endpoints
"""
from typing import Any, Optional, Dict, List, Generic, TypeVar
from pydantic import BaseModel, Field

# Generic type for data payload
T = TypeVar('T')


class MetaData(BaseModel):
    """
    Metadata for responses
    """
    total_records: Optional[int] = Field(
        None,
        description="Total number of records processed"
    )
    filtered_records: Optional[int] = Field(
        None,
        description="Number of records after filtering"
    )
    data_source: Optional[str] = Field(
        None,
        description="Data source: 'postgresql' or 'json'"
    )
    timestamp: Optional[str] = Field(
        None,
        description="Response timestamp (ISO format)"
    )
    processing_time_ms: Optional[float] = Field(
        None,
        description="Processing time in milliseconds"
    )


class StandardResponse(BaseModel, Generic[T]):
    """
    Standard API response wrapper
    """
    success: bool = Field(
        ...,
        description="Whether the request was successful"
    )
    data: Optional[T] = Field(
        None,
        description="Response data payload"
    )
    error: Optional[str] = Field(
        None,
        description="Error message if success is False"
    )
    meta: Optional[MetaData] = Field(
        None,
        description="Response metadata"
    )


class RegionStats(BaseModel):
    """
    Statistics for a single region
    """
    count: int
    avg_price: float
    max_price: float
    min_price: float


class BasicStatsData(BaseModel):
    """
    Data structure for basic statistics response
    """
    total_count: int = Field(..., description="Total number of transactions")
    avg_price: float = Field(..., description="Average price in 만원")
    max_price: float = Field(..., description="Maximum price in 만원")
    min_price: float = Field(..., description="Minimum price in 만원")
    median_price: float = Field(..., description="Median price in 만원")
    avg_area: float = Field(..., description="Average area in m²")
    regions: Dict[str, RegionStats] = Field(
        ...,
        description="Statistics by region"
    )


class BasicStatsResponse(StandardResponse[BasicStatsData]):
    """
    Response for basic statistics endpoint
    """
    pass


class MonthlyTrendData(BaseModel):
    """
    Monthly trend data point
    """
    year_month: str = Field(..., description="Year-month (YYYY-MM)")
    count: int = Field(..., description="Number of transactions")
    avg_price: float = Field(..., description="Average price in 만원")
    max_price: float = Field(..., description="Maximum price in 만원")
    min_price: float = Field(..., description="Minimum price in 만원")
    median_price: float = Field(..., description="Median price in 만원")


class PriceTrendData(BaseModel):
    """
    Data structure for price trend response
    """
    trend_data: List[MonthlyTrendData] = Field(
        ...,
        description="Monthly price trend data"
    )
    overall_trend: Optional[str] = Field(
        None,
        description="Overall trend direction: 'increasing', 'decreasing', 'stable'"
    )
    price_change_pct: Optional[float] = Field(
        None,
        description="Price change percentage from start to end"
    )


class PriceTrendResponse(StandardResponse[PriceTrendData]):
    """
    Response for price trend endpoint
    """
    pass


class RegionData(BaseModel):
    """
    Data for a single region
    """
    region_name: str = Field(..., description="Region name")
    count: int = Field(..., description="Number of transactions")
    avg_price: float = Field(..., description="Average price in 만원")
    max_price: float = Field(..., description="Maximum price in 만원")
    min_price: float = Field(..., description="Minimum price in 만원")
    median_price: Optional[float] = Field(None, description="Median price in 만원")
    total_volume: Optional[float] = Field(
        None,
        description="Total transaction volume in 만원"
    )


class RegionalAnalysisData(BaseModel):
    """
    Data structure for regional analysis response
    """
    regions: List[RegionData] = Field(
        ...,
        description="Regional statistics sorted by average price (descending)"
    )
    top_region: Optional[str] = Field(
        None,
        description="Region with highest average price"
    )
    total_regions: int = Field(
        ...,
        description="Total number of regions analyzed"
    )


class RegionalAnalysisResponse(StandardResponse[RegionalAnalysisData]):
    """
    Response for regional analysis endpoint
    """
    pass
