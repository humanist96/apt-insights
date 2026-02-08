"""
Logging middleware configuration
"""
import time
import structlog
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and log metrics

        Args:
            request: Incoming HTTP request
            call_next: Next middleware in chain

        Returns:
            HTTP response
        """
        logger = structlog.get_logger(__name__)

        # Start timer
        start_time = time.time()

        # Log incoming request
        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            query_params=str(request.query_params),
            client_host=request.client.host if request.client else None,
        )

        # Process request
        try:
            response = await call_next(request)

            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000  # Convert to ms

            # Log response
            logger.info(
                "request_completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                processing_time_ms=round(processing_time, 2),
            )

            # Add custom header with processing time
            response.headers["X-Processing-Time-Ms"] = str(round(processing_time, 2))

            return response

        except Exception as e:
            # Calculate processing time for error case
            processing_time = (time.time() - start_time) * 1000

            # Log error
            logger.error(
                "request_failed",
                method=request.method,
                path=request.url.path,
                error=str(e),
                error_type=type(e).__name__,
                processing_time_ms=round(processing_time, 2),
            )
            raise


def setup_logging_middleware(app: FastAPI) -> None:
    """
    Add logging middleware to the FastAPI application

    Note: Logging configuration is done in config/logging.py

    Args:
        app: FastAPI application instance
    """
    # Add logging middleware
    app.add_middleware(LoggingMiddleware)
