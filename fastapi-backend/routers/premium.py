"""
Premium Analysis API endpoints
Provides price per area and premium analysis endpoints
"""
import time
from datetime import datetime
import structlog
from fastapi import APIRouter, HTTPException, status

from schemas.requests import (
    PricePerAreaRequest,
    PricePerAreaTrendRequest,
    FloorPremiumRequest,
    BuildingAgePremiumRequest,
)
from schemas.responses import StandardResponse, MetaData
from services.analyzer_service import AnalyzerService

logger = structlog.get_logger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/premium",
    tags=["premium"],
    responses={
        500: {"description": "Internal server error"},
        400: {"description": "Bad request"},
    },
)

# Initialize analyzer service (singleton)
analyzer_service = AnalyzerService()


@router.post(
    "/price-per-area",
    response_model=StandardResponse,
    summary="Calculate price per area",
    description="""
    Calculate price per area (평당가) statistics.
    Returns:
    - Average, min, max, median price per area
    - Distribution by area size
    - Regional comparisons

    Price per area = Total price / Exclusive area
    """,
)
async def calculate_price_per_area(request: PricePerAreaRequest) -> StandardResponse:
    """
    Calculate price per area statistics

    Args:
        request: PricePerAreaRequest with optional filters

    Returns:
        StandardResponse with price per area data
    """
    start_time = time.time()

    try:
        logger.info(
            "price_per_area_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_price_per_area(
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000

        # Build response
        response_meta = MetaData(
            **metadata,
            processing_time_ms=round(processing_time, 2),
        )

        return StandardResponse(
            success=True,
            data=result,
            meta=response_meta,
        )

    except Exception as e:
        logger.error(
            "price_per_area_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate price per area: {str(e)}",
        )


@router.post(
    "/price-per-area-trend",
    response_model=StandardResponse,
    summary="Analyze price per area trend",
    description="""
    Analyze price per area trends over time.
    Returns monthly aggregated data:
    - Average price per area
    - Transaction count
    - Min/max values
    - Trend direction

    Useful for tracking market premium changes.
    """,
)
async def analyze_price_per_area_trend(request: PricePerAreaTrendRequest) -> StandardResponse:
    """
    Analyze price per area trend over time

    Args:
        request: PricePerAreaTrendRequest with optional filters

    Returns:
        StandardResponse with price per area trend data
    """
    start_time = time.time()

    try:
        logger.info(
            "price_per_area_trend_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_price_per_area_trend(
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000

        # Build response
        response_meta = MetaData(
            **metadata,
            processing_time_ms=round(processing_time, 2),
        )

        return StandardResponse(
            success=True,
            data=result,
            meta=response_meta,
        )

    except Exception as e:
        logger.error(
            "price_per_area_trend_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze price per area trend: {str(e)}",
        )


@router.post(
    "/floor-premium",
    response_model=StandardResponse,
    summary="Analyze floor premium",
    description="""
    Analyze price premium by floor level.
    Compares:
    - Low floors (1-5)
    - Mid floors (6-15)
    - High floors (16+)

    Returns premium percentage and absolute price differences.
    """,
)
async def analyze_floor_premium(request: FloorPremiumRequest) -> StandardResponse:
    """
    Analyze floor premium

    Args:
        request: FloorPremiumRequest with optional filters

    Returns:
        StandardResponse with floor premium data
    """
    start_time = time.time()

    try:
        logger.info(
            "floor_premium_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_floor_premium(
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000

        # Build response
        response_meta = MetaData(
            **metadata,
            processing_time_ms=round(processing_time, 2),
        )

        return StandardResponse(
            success=True,
            data=result,
            meta=response_meta,
        )

    except Exception as e:
        logger.error(
            "floor_premium_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze floor premium: {str(e)}",
        )


@router.post(
    "/building-age-premium",
    response_model=StandardResponse,
    summary="Analyze building age premium",
    description="""
    Analyze price premium by building age.
    Compares:
    - New buildings (0-5 years)
    - Mid-age buildings (6-15 years)
    - Old buildings (16+ years)

    Returns premium percentage relative to average.
    """,
)
async def analyze_building_age_premium(request: BuildingAgePremiumRequest) -> StandardResponse:
    """
    Analyze building age premium

    Args:
        request: BuildingAgePremiumRequest with optional filters

    Returns:
        StandardResponse with building age premium data
    """
    start_time = time.time()

    try:
        logger.info(
            "building_age_premium_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_building_age_premium(
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000

        # Build response
        response_meta = MetaData(
            **metadata,
            processing_time_ms=round(processing_time, 2),
        )

        return StandardResponse(
            success=True,
            data=result,
            meta=response_meta,
        )

    except Exception as e:
        logger.error(
            "building_age_premium_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze building age premium: {str(e)}",
        )
