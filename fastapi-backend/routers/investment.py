"""
Investment Analysis API endpoints
Provides jeonse ratio, gap investment, and bargain sales detection
"""
import time
from datetime import datetime
import structlog
from fastapi import APIRouter, HTTPException, status

from schemas.requests import (
    JeonseRatioRequest,
    GapInvestmentRequest,
    BargainSalesRequest,
)
from schemas.responses import StandardResponse, MetaData
from services.analyzer_service import AnalyzerService

logger = structlog.get_logger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/investment",
    tags=["investment"],
    responses={
        500: {"description": "Internal server error"},
        400: {"description": "Bad request"},
    },
)

# Initialize analyzer service (singleton)
analyzer_service = AnalyzerService()


@router.post(
    "/jeonse-ratio",
    response_model=StandardResponse,
    summary="Calculate jeonse ratio",
    description="""
    Calculate jeonse ratio (전세가율) for apartments.

    Jeonse Ratio = (Jeonse Price / Sale Price) × 100

    Returns:
    - Average jeonse ratio by region
    - Distribution of ratios
    - High ratio apartments (investment opportunity)
    - Low ratio apartments (risky)

    High ratio (>80%) suggests strong rental demand.
    Low ratio (<60%) suggests weak rental market.
    """,
)
async def calculate_jeonse_ratio(request: JeonseRatioRequest) -> StandardResponse:
    """
    Calculate jeonse ratio statistics

    Args:
        request: JeonseRatioRequest with optional filters

    Returns:
        StandardResponse with jeonse ratio data
    """
    start_time = time.time()

    try:
        logger.info(
            "jeonse_ratio_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_jeonse_ratio(
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
            "jeonse_ratio_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate jeonse ratio: {str(e)}",
        )


@router.post(
    "/gap-investment",
    response_model=StandardResponse,
    summary="Analyze gap investment opportunities",
    description="""
    Analyze gap investment (갭투자) opportunities.

    Gap = Sale Price - Jeonse Price

    Lower gap means:
    - Less capital required
    - Better investment leverage
    - Potential cashflow positive

    Returns:
    - Top gap investment candidates
    - Gap ratio distribution
    - Regional gap analysis
    - Risk indicators

    Typical good gap ratio: 70-80% (jeonse ratio)
    """,
)
async def analyze_gap_investment(request: GapInvestmentRequest) -> StandardResponse:
    """
    Analyze gap investment opportunities

    Args:
        request: GapInvestmentRequest with optional filters

    Returns:
        StandardResponse with gap investment data
    """
    start_time = time.time()

    try:
        logger.info(
            "gap_investment_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
            min_gap_ratio=request.min_gap_ratio,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_gap_investment(
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
            min_gap_ratio=request.min_gap_ratio,
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
            "gap_investment_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze gap investment: {str(e)}",
        )


@router.post(
    "/bargain-sales",
    response_model=StandardResponse,
    summary="Detect bargain sales",
    description="""
    Detect bargain sales (급매물) opportunities.

    Definition: Transactions significantly below recent average prices

    Detection criteria:
    - Compare to 3-month average for same apartment + area
    - Below threshold percentage (default 10%)
    - Recent transaction (within analysis period)

    Returns:
    - List of potential bargain sales
    - Price discount percentage
    - Comparison to market average
    - Risk factors

    Note: Low price may indicate issues (defects, disputes, etc.)
    """,
)
async def detect_bargain_sales(request: BargainSalesRequest) -> StandardResponse:
    """
    Detect bargain sales opportunities

    Args:
        request: BargainSalesRequest with optional filters

    Returns:
        StandardResponse with bargain sales data
    """
    start_time = time.time()

    try:
        logger.info(
            "bargain_sales_request",
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
            threshold_pct=request.threshold_pct,
        )

        # Call analyzer service
        result, metadata = analyzer_service.get_bargain_sales(
            region_filter=request.region_filter,
            start_date=request.start_date,
            end_date=request.end_date,
            threshold_pct=request.threshold_pct,
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
            "bargain_sales_error",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to detect bargain sales: {str(e)}",
        )
