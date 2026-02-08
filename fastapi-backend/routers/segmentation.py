"""
Segmentation Analysis API endpoints
Provides apartment transaction segmentation by area, floor, build year, and apartment
"""
import time
from datetime import datetime
import structlog
from fastapi import APIRouter, HTTPException, status

from schemas.requests import (
    AreaAnalysisRequest,
    FloorAnalysisRequest,
    BuildYearAnalysisRequest,
    ApartmentAnalysisRequest,
    ApartmentDetailRequest,
)
from schemas.responses import StandardResponse, MetaData
from services.analyzer_service import AnalyzerService

logger = structlog.get_logger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/analysis",
    tags=["segmentation"],
    responses={
        500: {"description": "Internal server error"},
        400: {"description": "Bad request"},
    },
)

# Initialize analyzer service (singleton)
analyzer_service = AnalyzerService()


@router.post(
    "/by-area",
    response_model=StandardResponse,
    summary="Analyze by area",
    description="""
    Analyze apartment transactions by exclusive area.
    Returns statistics for each area segment including:
    - Transaction count
    - Average, min, max, median prices
    - Price per area statistics

    Supports custom area bins or automatic binning.
    """,
)
async def analyze_by_area(request: AreaAnalysisRequest) -> StandardResponse:
    """
    Analyze transactions by area

    Args:
        request: AreaAnalysisRequest with optional filters and bins

    Returns:
        StandardResponse with area analysis data
    """
    start_time = time.time()

    try:
        logger.info(
            "area_analysis_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
            bins=request.bins,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_area_analysis(
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
            bins=request.bins,
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
            "area_analysis_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze by area: {str(e)}",
        )


@router.post(
    "/by-floor",
    response_model=StandardResponse,
    summary="Analyze by floor",
    description="""
    Analyze apartment transactions by floor level.
    Returns statistics for each floor segment:
    - Low floors (1-5)
    - Mid floors (6-15)
    - High floors (16+)

    Includes price premium analysis by floor.
    """,
)
async def analyze_by_floor(request: FloorAnalysisRequest) -> StandardResponse:
    """
    Analyze transactions by floor

    Args:
        request: FloorAnalysisRequest with optional filters

    Returns:
        StandardResponse with floor analysis data
    """
    start_time = time.time()

    try:
        logger.info(
            "floor_analysis_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_floor_analysis(
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
            "floor_analysis_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze by floor: {str(e)}",
        )


@router.post(
    "/by-build-year",
    response_model=StandardResponse,
    summary="Analyze by building year",
    description="""
    Analyze apartment transactions by construction year.
    Returns statistics for each year segment including:
    - Transaction count
    - Average, min, max prices
    - Building age at transaction time

    Groups buildings by construction year.
    """,
)
async def analyze_by_build_year(request: BuildYearAnalysisRequest) -> StandardResponse:
    """
    Analyze transactions by building construction year

    Args:
        request: BuildYearAnalysisRequest with optional filters

    Returns:
        StandardResponse with build year analysis data
    """
    start_time = time.time()

    try:
        logger.info(
            "build_year_analysis_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_build_year_analysis(
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
            "build_year_analysis_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze by build year: {str(e)}",
        )


@router.post(
    "/by-apartment",
    response_model=StandardResponse,
    summary="Analyze by apartment complex",
    description="""
    Analyze transactions grouped by apartment complex.
    Returns statistics for each apartment including:
    - Transaction count
    - Average, min, max prices
    - Price per area
    - Most common area sizes

    Only includes apartments with minimum transaction count.
    """,
)
async def analyze_by_apartment(request: ApartmentAnalysisRequest) -> StandardResponse:
    """
    Analyze transactions by apartment complex

    Args:
        request: ApartmentAnalysisRequest with optional filters

    Returns:
        StandardResponse with apartment analysis data
    """
    start_time = time.time()

    try:
        logger.info(
            "apartment_analysis_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
            min_count=request.min_count,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_apartment_analysis(
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
            min_count=request.min_count,
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
            "apartment_analysis_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze by apartment: {str(e)}",
        )


@router.post(
    "/apartment-detail",
    response_model=StandardResponse,
    summary="Get apartment detail",
    description="""
    Get detailed information for a specific apartment complex.
    Returns comprehensive statistics including:
    - All transaction history
    - Price trends over time
    - Area distribution
    - Floor distribution
    - Recent transactions

    Use region filter to distinguish apartments with same name.
    """,
)
async def get_apartment_detail(request: ApartmentDetailRequest) -> StandardResponse:
    """
    Get detailed information for a specific apartment

    Args:
        request: ApartmentDetailRequest with apartment name and optional filters

    Returns:
        StandardResponse with apartment detail data
    """
    start_time = time.time()

    try:
        logger.info(
            "apartment_detail_request",
            apt_name=request.apt_name,
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_apartment_detail(
            apt_name=request.apt_name,
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
            "apartment_detail_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get apartment detail: {str(e)}",
        )
