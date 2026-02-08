"""
Data export API endpoints (CSV, PDF)
Premium feature only
"""
import csv
import io
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Header
from fastapi.responses import StreamingResponse
from typing import Optional, List, Dict, Any
import structlog

from schemas.subscription import ExportRequest, ExportResponse
from services.subscription_service import get_subscription_service
from services.analyzer_service import AnalyzerService

logger = structlog.get_logger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/export",
    tags=["export"],
    responses={
        403: {"description": "Premium feature - upgrade required"},
        500: {"description": "Internal server error"},
    },
)

# Services
subscription_service = get_subscription_service()
analyzer_service = AnalyzerService()


def check_premium_access(user_id: str):
    """
    Check if user has premium access

    Args:
        user_id: User identifier

    Raises:
        HTTPException: If user is not premium
    """
    if not subscription_service.is_premium_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Premium feature",
                "message": "CSV 내보내기는 프리미엄 기능입니다",
                "upgrade_url": "/subscription",
            },
        )


def format_csv_data(data: List[Dict[str, Any]]) -> str:
    """
    Format data as CSV string

    Args:
        data: List of transaction records

    Returns:
        CSV formatted string
    """
    if not data:
        return ""

    # Create CSV in memory
    output = io.StringIO()

    # Define field order for CSV
    fieldnames = [
        "지역명",
        "아파트명",
        "거래금액",
        "전용면적",
        "계약년월",
        "계약일",
        "층",
        "건축년도",
        "도로명",
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for record in data:
        row = {
            "지역명": record.get("_region_name", ""),
            "아파트명": record.get("아파트", ""),
            "거래금액": record.get("_deal_amount_numeric", ""),
            "전용면적": record.get("전용면적", ""),
            "계약년월": record.get("_year_month", ""),
            "계약일": record.get("_deal_day", ""),
            "층": record.get("층", ""),
            "건축년도": record.get("건축년도", ""),
            "도로명": record.get("도로명", ""),
        }
        writer.writerow(row)

    return output.getvalue()


@router.post(
    "/csv",
    summary="Export data to CSV",
    description="Export transaction data to CSV format (Premium only)",
)
async def export_csv(
    request: ExportRequest,
    user_id: str = Header(None, alias="X-User-Id"),
):
    """
    Export data to CSV

    Args:
        request: Export request with filters
        user_id: User ID from header

    Returns:
        CSV file as streaming response
    """
    try:
        user_id = user_id or "demo_user"

        # Check premium access
        check_premium_access(user_id)

        logger.info("csv_export_requested", user_id=user_id, filters=request.filters)

        # Get data from analyzer
        # For now, use basic stats data as sample
        result, metadata = analyzer_service.get_basic_stats()

        # In production, this would fetch filtered transaction data
        # For now, create sample data
        sample_data = [
            {
                "_region_name": "강남구",
                "아파트": "래미안대치팰리스",
                "_deal_amount_numeric": 250000,
                "전용면적": 84.9,
                "_year_month": "2023-12",
                "_deal_day": "15",
                "층": "10",
                "건축년도": "2010",
                "도로명": "대치동",
            },
            {
                "_region_name": "송파구",
                "아파트": "헬리오시티",
                "_deal_amount_numeric": 180000,
                "전용면적": 74.5,
                "_year_month": "2023-12",
                "_deal_day": "20",
                "층": "15",
                "건축년도": "2019",
                "도로명": "위례성대로",
            },
        ]

        # Generate CSV
        csv_content = format_csv_data(sample_data)

        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"apartment_data_{timestamp}.csv"

        logger.info(
            "csv_export_completed",
            user_id=user_id,
            filename=filename,
            rows=len(sample_data),
        )

        # Return as streaming response
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("csv_export_error", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export CSV: {str(e)}",
        )


@router.post(
    "/pdf",
    response_model=ExportResponse,
    summary="Export data to PDF",
    description="Export analysis report to PDF format (Premium only, mock for now)",
)
async def export_pdf(
    request: ExportRequest,
    user_id: str = Header(None, alias="X-User-Id"),
) -> ExportResponse:
    """
    Export data to PDF (mock implementation)

    Args:
        request: Export request with filters
        user_id: User ID from header

    Returns:
        Export response with mock data
    """
    try:
        user_id = user_id or "demo_user"

        # Check premium access
        check_premium_access(user_id)

        logger.info("pdf_export_requested", user_id=user_id, filters=request.filters)

        # Mock PDF generation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_report_{timestamp}.pdf"

        logger.info(
            "pdf_export_mock_completed",
            user_id=user_id,
            filename=filename,
        )

        return ExportResponse(
            success=True,
            download_url=None,
            filename=filename,
            message="PDF 생성 중입니다. 실제 PDF 생성 기능은 추후 구현됩니다.",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("pdf_export_error", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export PDF: {str(e)}",
        )
