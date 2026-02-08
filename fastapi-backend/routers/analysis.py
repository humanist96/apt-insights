"""
Analysis API endpoints
Provides access to apartment transaction analysis functions
"""
import time
from datetime import datetime
from typing import Dict, Any
import structlog
from fastapi import APIRouter, HTTPException, status

from schemas.requests import (
    BasicStatsRequest,
    PriceTrendRequest,
    RegionalAnalysisRequest,
)
from schemas.responses import (
    StandardResponse,
    MetaData,
    BasicStatsData,
    BasicStatsResponse,
    PriceTrendData,
    PriceTrendResponse,
    RegionalAnalysisData,
    RegionalAnalysisResponse,
    MonthlyTrendData,
    RegionData,
)
from services.analyzer_service import AnalyzerService

logger = structlog.get_logger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/analysis",
    tags=["analysis"],
    responses={
        500: {"description": "Internal server error"},
        400: {"description": "Bad request"},
    },
)

# Initialize analyzer service (singleton)
analyzer_service = AnalyzerService()


@router.post(
    "/basic-stats",
    response_model=BasicStatsResponse,
    summary="Calculate basic statistics",
    description="""
    Calculate basic statistics for apartment transactions including:
    - Total transaction count
    - Average, min, max, median prices
    - Average area
    - Regional statistics

    Supports filtering by region and date range.
    """,
)
async def calculate_basic_stats(
    request: BasicStatsRequest,
) -> BasicStatsResponse:
    """
    Calculate basic statistics for apartment transactions

    Args:
        request: BasicStatsRequest with optional filters

    Returns:
        BasicStatsResponse with statistics data
    """
    start_time = time.time()

    try:
        logger.info(
            "basic_stats_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        stats, metadata = analyzer_service.get_basic_stats(
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000

        # Build response
        response_data = BasicStatsData(**stats)
        response_meta = MetaData(
            **metadata,
            processing_time_ms=round(processing_time, 2),
        )

        return BasicStatsResponse(
            success=True,
            data=response_data,
            meta=response_meta,
        )

    except Exception as e:
        logger.error(
            "basic_stats_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate basic statistics: {str(e)}",
        )


@router.post(
    "/price-trend",
    response_model=PriceTrendResponse,
    summary="Analyze price trends",
    description="""
    Analyze price trends over time for apartment transactions.
    Returns monthly aggregated data including:
    - Transaction count
    - Average, min, max, median prices
    - Overall trend direction
    - Price change percentage

    Supports filtering by region and date range.
    """,
)
async def calculate_price_trend(
    request: PriceTrendRequest,
) -> PriceTrendResponse:
    """
    Calculate price trend analysis

    Args:
        request: PriceTrendRequest with optional filters

    Returns:
        PriceTrendResponse with trend data
    """
    start_time = time.time()

    try:
        logger.info(
            "price_trend_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
            group_by=request.group_by,
        )

        # Call analyzer service
        trend, metadata = analyzer_service.get_price_trend(
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000

        # Transform trend data to match response schema
        trend_data_list = []
        for month_data in trend.get('monthly_trend', []):
            trend_data_list.append(
                MonthlyTrendData(
                    year_month=month_data.get('year_month', ''),
                    count=month_data.get('count', 0),
                    avg_price=month_data.get('avg_price', 0.0),
                    max_price=month_data.get('max_price', 0.0),
                    min_price=month_data.get('min_price', 0.0),
                    median_price=month_data.get('median_price', 0.0),
                )
            )

        # Calculate overall trend and price change
        overall_trend = None
        price_change_pct = None

        if len(trend_data_list) >= 2:
            first_price = trend_data_list[0].avg_price
            last_price = trend_data_list[-1].avg_price

            if first_price > 0:
                price_change_pct = ((last_price - first_price) / first_price) * 100

                if price_change_pct > 5:
                    overall_trend = "increasing"
                elif price_change_pct < -5:
                    overall_trend = "decreasing"
                else:
                    overall_trend = "stable"

        # Build response
        response_data = PriceTrendData(
            trend_data=trend_data_list,
            overall_trend=overall_trend,
            price_change_pct=round(price_change_pct, 2) if price_change_pct is not None else None,
        )

        response_meta = MetaData(
            **metadata,
            processing_time_ms=round(processing_time, 2),
        )

        return PriceTrendResponse(
            success=True,
            data=response_data,
            meta=response_meta,
        )

    except Exception as e:
        logger.error(
            "price_trend_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate price trend: {str(e)}",
        )


@router.post(
    "/regional",
    response_model=RegionalAnalysisResponse,
    summary="Analyze by region",
    description="""
    Analyze apartment transactions by region.
    Returns statistics for each region including:
    - Transaction count
    - Average, min, max, median prices
    - Total transaction volume

    Results are sorted by average price in descending order.
    Supports filtering by specific regions and date range.
    """,
)
async def analyze_regional(
    request: RegionalAnalysisRequest,
) -> RegionalAnalysisResponse:
    """
    Analyze transactions by region

    Args:
        request: RegionalAnalysisRequest with optional filters

    Returns:
        RegionalAnalysisResponse with regional data
    """
    start_time = time.time()

    try:
        logger.info(
            "regional_analysis_request",
            regions=request.regions,
            start_date=request.start_date,
            end_date=request.end_date,
            top_n=request.top_n,
        )

        # Call analyzer service
        regional_data, metadata = analyzer_service.get_regional_analysis(
            regions=request.regions,
            start_date=request.start_date,
            end_date=request.end_date,
            top_n=request.top_n,
        )

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000

        # Transform regional data to match response schema
        regions_list = []
        for region_data in regional_data.get('regions', []):
            regions_list.append(
                RegionData(
                    region_name=region_data.get('region_name', ''),
                    count=region_data.get('count', 0),
                    avg_price=region_data.get('avg_price', 0.0),
                    max_price=region_data.get('max_price', 0.0),
                    min_price=region_data.get('min_price', 0.0),
                    median_price=region_data.get('median_price'),
                    total_volume=region_data.get('total_volume'),
                )
            )

        # Get top region
        top_region = regions_list[0].region_name if regions_list else None

        # Build response
        response_data = RegionalAnalysisData(
            regions=regions_list,
            top_region=top_region,
            total_regions=len(regions_list),
        )

        response_meta = MetaData(
            **metadata,
            processing_time_ms=round(processing_time, 2),
        )

        return RegionalAnalysisResponse(
            success=True,
            data=response_data,
            meta=response_meta,
        )

    except Exception as e:
        logger.error(
            "regional_analysis_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze regional data: {str(e)}",
        )


@router.post(
    "/cache/clear",
    summary="Clear data cache",
    description="Clear the in-memory data cache to force reload on next request",
)
async def clear_cache() -> Dict[str, Any]:
    """
    Clear the data cache

    Returns:
        Success message
    """
    try:
        analyzer_service.clear_cache()
        logger.info("cache_cleared_via_api")

        return {
            "success": True,
            "message": "Cache cleared successfully",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(
            "cache_clear_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}",
        )
