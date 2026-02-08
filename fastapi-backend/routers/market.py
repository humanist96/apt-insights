"""
Market Analysis API endpoints
Provides market signals, trend analysis, and period comparisons
"""
import time
from datetime import datetime
import structlog
from fastapi import APIRouter, HTTPException, status

from schemas.requests import (
    RentVsJeonseRequest,
    DealingTypeRequest,
    BuyerSellerTypeRequest,
    CancelledDealsRequest,
    PeriodSummaryRequest,
    BaselineSummaryRequest,
    ComparePeriodRequest,
    MarketSignalsRequest,
)
from schemas.responses import StandardResponse, MetaData
from services.analyzer_service import AnalyzerService

logger = structlog.get_logger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/market",
    tags=["market"],
    responses={
        500: {"description": "Internal server error"},
        400: {"description": "Bad request"},
    },
)

# Initialize analyzer service (singleton)
analyzer_service = AnalyzerService()


@router.post(
    "/rent-vs-jeonse",
    response_model=StandardResponse,
    summary="Analyze rent vs jeonse",
    description="""
    Compare monthly rent (월세) vs jeonse (전세) transactions.

    Returns:
    - Transaction count by type
    - Average prices by type
    - Rent to jeonse ratio trends
    - Market preference indicators

    High rent proportion may indicate:
    - Weakening jeonse market
    - Higher interest rates
    - Investor caution
    """,
)
async def analyze_rent_vs_jeonse(request: RentVsJeonseRequest) -> StandardResponse:
    """
    Analyze rent vs jeonse distribution

    Args:
        request: RentVsJeonseRequest with optional filters

    Returns:
        StandardResponse with rent vs jeonse data
    """
    start_time = time.time()

    try:
        logger.info(
            "rent_vs_jeonse_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_rent_vs_jeonse(
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
            "rent_vs_jeonse_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze rent vs jeonse: {str(e)}",
        )


@router.post(
    "/dealing-type",
    response_model=StandardResponse,
    summary="Analyze dealing type distribution",
    description="""
    Analyze transaction dealing types.

    Categories:
    - Direct transaction (직거래)
    - Agent transaction (중개거래)
    - Other

    Returns distribution and trends.
    """,
)
async def analyze_dealing_type(request: DealingTypeRequest) -> StandardResponse:
    """
    Analyze dealing type distribution

    Args:
        request: DealingTypeRequest with optional filters

    Returns:
        StandardResponse with dealing type data
    """
    start_time = time.time()

    try:
        logger.info(
            "dealing_type_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_dealing_type(
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
            "dealing_type_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze dealing type: {str(e)}",
        )


@router.post(
    "/buyer-seller-type",
    response_model=StandardResponse,
    summary="Analyze buyer and seller types",
    description="""
    Analyze buyer and seller type distribution.

    Categories:
    - Individual
    - Corporation
    - Government
    - Other

    Returns distribution by transaction type.
    """,
)
async def analyze_buyer_seller_type(request: BuyerSellerTypeRequest) -> StandardResponse:
    """
    Analyze buyer and seller type distribution

    Args:
        request: BuyerSellerTypeRequest with optional filters

    Returns:
        StandardResponse with buyer/seller type data
    """
    start_time = time.time()

    try:
        logger.info(
            "buyer_seller_type_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_buyer_seller_type(
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
            "buyer_seller_type_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze buyer/seller type: {str(e)}",
        )


@router.post(
    "/cancelled-deals",
    response_model=StandardResponse,
    summary="Analyze cancelled deals",
    description="""
    Analyze cancelled transaction patterns.

    Returns:
    - Cancellation rate by region
    - Common cancellation reasons
    - Timing patterns
    - Risk indicators

    High cancellation rate may indicate:
    - Market uncertainty
    - Financing issues
    - Price disputes
    """,
)
async def analyze_cancelled_deals(request: CancelledDealsRequest) -> StandardResponse:
    """
    Analyze cancelled deals

    Args:
        request: CancelledDealsRequest with optional filters

    Returns:
        StandardResponse with cancelled deals data
    """
    start_time = time.time()

    try:
        logger.info(
            "cancelled_deals_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_cancelled_deals(
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
            "cancelled_deals_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze cancelled deals: {str(e)}",
        )


@router.post(
    "/period-summary",
    response_model=StandardResponse,
    summary="Summarize period",
    description="""
    Generate comprehensive summary for a specific time period.

    Returns:
    - Transaction count and volume
    - Price statistics
    - Regional breakdown
    - API type distribution
    - Key metrics and trends

    Useful for monthly/quarterly reports.
    """,
)
async def summarize_period(request: PeriodSummaryRequest) -> StandardResponse:
    """
    Generate period summary

    Args:
        request: PeriodSummaryRequest with date range

    Returns:
        StandardResponse with period summary data
    """
    start_time = time.time()

    try:
        logger.info(
            "period_summary_request",
            start_date=request.start_date,
            end_date=request.end_date,
            region_filter=request.region_filter,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_period_summary(
            start_date=request.start_date,
            end_date=request.end_date,
            region_filter=request.region_filter,
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
            "period_summary_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to summarize period: {str(e)}",
        )


@router.post(
    "/baseline-summary",
    response_model=StandardResponse,
    summary="Build baseline summary",
    description="""
    Build baseline summary from previous period.

    Calculates summary for the period immediately before
    the specified date range (same duration).

    Useful for period-over-period comparisons.
    """,
)
async def build_baseline_summary(request: BaselineSummaryRequest) -> StandardResponse:
    """
    Build baseline summary from previous period

    Args:
        request: BaselineSummaryRequest with date range

    Returns:
        StandardResponse with baseline summary data
    """
    start_time = time.time()

    try:
        logger.info(
            "baseline_summary_request",
            start_date=request.start_date,
            end_date=request.end_date,
            region_filter=request.region_filter,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_baseline_summary(
            start_date=request.start_date,
            end_date=request.end_date,
            region_filter=request.region_filter,
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
            "baseline_summary_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to build baseline summary: {str(e)}",
        )


@router.post(
    "/compare-periods",
    response_model=StandardResponse,
    summary="Compare periods",
    description="""
    Compare two time periods.

    Returns:
    - Price change percentage
    - Volume change percentage
    - Transaction count change
    - Market trend indicators

    Useful for:
    - Month-over-month analysis
    - Year-over-year analysis
    - Seasonal trend detection
    """,
)
async def compare_periods(request: ComparePeriodRequest) -> StandardResponse:
    """
    Compare two time periods

    Args:
        request: ComparePeriodRequest with two date ranges

    Returns:
        StandardResponse with period comparison data
    """
    start_time = time.time()

    try:
        logger.info(
            "compare_periods_request",
            current_start=request.current_start_date,
            current_end=request.current_end_date,
            previous_start=request.previous_start_date,
            previous_end=request.previous_end_date,
            region_filter=request.region_filter,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_period_comparison(
            current_start_date=request.current_start_date,
            current_end_date=request.current_end_date,
            previous_start_date=request.previous_start_date,
            previous_end_date=request.previous_end_date,
            region_filter=request.region_filter,
            current_label=request.current_label,
            previous_label=request.previous_label,
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
            "compare_periods_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compare periods: {str(e)}",
        )


@router.post(
    "/signals",
    response_model=StandardResponse,
    summary="Detect market signals",
    description="""
    Detect market signals and anomalies.

    Returns:
    - Price surge/drop signals
    - Volume spike signals
    - Ratio anomalies
    - Risk warnings
    - Opportunity alerts

    Signals include:
    - Strong price increase (>10% change)
    - Price decline (<-5% change)
    - Transaction surge (>50% increase)
    - Market freeze (<-30% volume drop)
    - High jeonse ratio (>85%)
    """,
)
async def detect_market_signals(request: MarketSignalsRequest) -> StandardResponse:
    """
    Detect market signals

    Args:
        request: MarketSignalsRequest with date range

    Returns:
        StandardResponse with market signals data
    """
    start_time = time.time()

    try:
        logger.info(
            "market_signals_request",
            start_date=request.start_date,
            end_date=request.end_date,
            region_filter=request.region_filter,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_market_signals(
            start_date=request.start_date,
            end_date=request.end_date,
            region_filter=request.region_filter,
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
            "market_signals_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to detect market signals: {str(e)}",
        )
