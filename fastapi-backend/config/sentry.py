"""
Sentry Configuration for FastAPI Backend
Error tracking and performance monitoring
"""
import os
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
import structlog

logger = structlog.get_logger(__name__)


def init_sentry():
    """
    Initialize Sentry SDK for error tracking and performance monitoring

    Environment Variables:
        SENTRY_DSN: Sentry Data Source Name (required)
        SENTRY_ENVIRONMENT: Environment name (default: development)
        SENTRY_TRACES_SAMPLE_RATE: Performance monitoring sample rate (default: 0.1)
        SENTRY_PROFILES_SAMPLE_RATE: Profiling sample rate (default: 0.1)
    """
    sentry_dsn = os.getenv("SENTRY_DSN")

    if not sentry_dsn:
        logger.warning(
            "sentry_not_configured",
            message="SENTRY_DSN not set, error tracking disabled"
        )
        return

    environment = os.getenv("SENTRY_ENVIRONMENT", "development")
    traces_sample_rate = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1"))
    profiles_sample_rate = float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.1"))

    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=environment,

        # Integrations
        integrations=[
            FastApiIntegration(
                transaction_style="endpoint",  # Use endpoint name as transaction
                failed_request_status_codes=[403, range(500, 599)],
            ),
            SqlalchemyIntegration(),
            RedisIntegration(),
        ],

        # Performance Monitoring
        traces_sample_rate=traces_sample_rate,
        _experiments={
            "profiles_sample_rate": profiles_sample_rate,
        },

        # Privacy: Don't send sensitive data
        send_default_pii=False,

        # Request data
        max_request_body_size="medium",  # Capture request bodies up to medium size

        # Release tracking
        release=os.getenv("APP_VERSION", "1.0.0"),

        # Error filtering: Don't send these errors to Sentry
        before_send=filter_errors,

        # Breadcrumbs configuration
        max_breadcrumbs=50,
    )

    logger.info(
        "sentry_initialized",
        environment=environment,
        traces_sample_rate=traces_sample_rate,
        profiles_sample_rate=profiles_sample_rate,
    )


def filter_errors(event, hint):
    """
    Filter out errors that shouldn't be sent to Sentry

    Args:
        event: Sentry event dictionary
        hint: Additional context about the error

    Returns:
        Event if it should be sent, None otherwise
    """
    # Don't send validation errors (4xx client errors)
    if "exc_info" in hint:
        exc_type, exc_value, tb = hint["exc_info"]

        # Filter out common client errors
        if exc_type.__name__ in [
            "ValidationError",
            "HTTPException",
        ]:
            # Only send if it's a 5xx error
            if hasattr(exc_value, "status_code") and exc_value.status_code < 500:
                return None

    # Don't send certain log levels
    if event.get("level") == "info":
        return None

    # Sanitize sensitive data from event
    if "request" in event:
        request = event["request"]

        # Remove sensitive headers
        if "headers" in request:
            sensitive_headers = ["Authorization", "Cookie", "X-Api-Key"]
            for header in sensitive_headers:
                if header in request["headers"]:
                    request["headers"][header] = "[Filtered]"

        # Remove sensitive query params
        if "query_string" in request:
            sensitive_params = ["token", "password", "secret", "api_key"]
            # This is a simple example - implement proper param filtering
            for param in sensitive_params:
                if param in request["query_string"].lower():
                    request["query_string"] = "[Filtered]"

    return event


def capture_exception(error: Exception, context: dict = None):
    """
    Capture an exception with additional context

    Args:
        error: The exception to capture
        context: Additional context dictionary
    """
    if context:
        with sentry_sdk.push_scope() as scope:
            for key, value in context.items():
                scope.set_context(key, value)
            sentry_sdk.capture_exception(error)
    else:
        sentry_sdk.capture_exception(error)


def capture_message(message: str, level: str = "info", context: dict = None):
    """
    Capture a message with additional context

    Args:
        message: The message to capture
        level: Log level (info, warning, error)
        context: Additional context dictionary
    """
    if context:
        with sentry_sdk.push_scope() as scope:
            for key, value in context.items():
                scope.set_context(key, value)
            sentry_sdk.capture_message(message, level=level)
    else:
        sentry_sdk.capture_message(message, level=level)


def set_user_context(user_id: str, email: str = None, username: str = None):
    """
    Set user context for error tracking

    Args:
        user_id: User identifier
        email: User email (optional, will be filtered if send_default_pii=False)
        username: Username (optional)
    """
    sentry_sdk.set_user({
        "id": user_id,
        "email": email,
        "username": username,
    })


def set_transaction_name(name: str):
    """
    Set custom transaction name for performance monitoring

    Args:
        name: Transaction name (e.g., "GET /api/v1/analysis/basic-stats")
    """
    with sentry_sdk.configure_scope() as scope:
        scope.transaction = name
