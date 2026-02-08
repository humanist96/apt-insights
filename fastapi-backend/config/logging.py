"""
Structured Logging Configuration
JSON format with log rotation and retention policies
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
import structlog
from structlog.stdlib import BoundLogger
from structlog.processors import CallsiteParameter


# Log directory
LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log levels
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
ACCESS_LOG_ENABLED = os.getenv("ACCESS_LOG_ENABLED", "true").lower() == "true"

# Log retention
MAX_LOG_SIZE = int(os.getenv("MAX_LOG_SIZE_MB", "100")) * 1024 * 1024  # bytes
BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "10"))
RETENTION_DAYS = int(os.getenv("LOG_RETENTION_DAYS", "30"))


def setup_logging():
    """
    Configure structured logging with JSON output and log rotation

    Creates separate log files:
    - app.log: Application logs (INFO and above)
    - error.log: Error logs only (ERROR and above)
    - access.log: HTTP access logs
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, LOG_LEVEL),
        handlers=[],
    )

    # Remove all existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create formatters
    console_renderer = (
        structlog.dev.ConsoleRenderer()
        if os.getenv("LOG_FORMAT", "json") == "console"
        else structlog.processors.JSONRenderer()
    )

    # Shared processors
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.CallsiteParameterAdder(
            [
                CallsiteParameter.FILENAME,
                CallsiteParameter.FUNC_NAME,
                CallsiteParameter.LINENO,
            ]
        ),
    ]

    # Configure structlog
    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=console_renderer,
            foreign_pre_chain=shared_processors,
        )
    )
    root_logger.addHandler(console_handler)

    # Application log file handler (rotating by size)
    app_log_file = LOG_DIR / "app.log"
    app_file_handler = RotatingFileHandler(
        app_log_file,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    app_file_handler.setLevel(logging.INFO)
    app_file_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer(),
            foreign_pre_chain=shared_processors,
        )
    )
    root_logger.addHandler(app_file_handler)

    # Error log file handler (rotating by size)
    error_log_file = LOG_DIR / "error.log"
    error_file_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer(),
            foreign_pre_chain=shared_processors,
        )
    )
    root_logger.addHandler(error_file_handler)

    # Access log file handler (rotating daily)
    if ACCESS_LOG_ENABLED:
        access_log_file = LOG_DIR / "access.log"
        access_file_handler = TimedRotatingFileHandler(
            access_log_file,
            when="midnight",
            interval=1,
            backupCount=RETENTION_DAYS,
            encoding="utf-8",
        )
        access_file_handler.setLevel(logging.INFO)
        access_file_handler.setFormatter(
            structlog.stdlib.ProcessorFormatter(
                processor=structlog.processors.JSONRenderer(),
                foreign_pre_chain=shared_processors,
            )
        )

        # Create access logger
        access_logger = logging.getLogger("access")
        access_logger.setLevel(logging.INFO)
        access_logger.addHandler(access_file_handler)
        access_logger.propagate = False

    # Silence noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("multipart").setLevel(logging.WARNING)

    logger = structlog.get_logger(__name__)
    logger.info(
        "logging_configured",
        log_level=LOG_LEVEL,
        log_dir=str(LOG_DIR),
        max_log_size_mb=MAX_LOG_SIZE // (1024 * 1024),
        backup_count=BACKUP_COUNT,
        retention_days=RETENTION_DAYS,
    )


def get_logger(name: str = None) -> BoundLogger:
    """
    Get a structlog logger instance

    Args:
        name: Logger name (defaults to module name)

    Returns:
        BoundLogger instance
    """
    return structlog.get_logger(name)


def log_with_context(**context):
    """
    Context manager for adding context to logs

    Usage:
        with log_with_context(user_id="123", request_id="abc"):
            logger.info("processing_request")
    """
    return structlog.contextvars.bind_contextvars(**context)


def sanitize_log_data(data: dict) -> dict:
    """
    Remove sensitive information from log data

    Args:
        data: Dictionary to sanitize

    Returns:
        Sanitized dictionary
    """
    sensitive_keys = [
        "password",
        "token",
        "secret",
        "api_key",
        "authorization",
        "cookie",
        "access_token",
        "refresh_token",
        "credit_card",
        "ssn",
    ]

    sanitized = {}
    for key, value in data.items():
        key_lower = key.lower()

        # Check if key contains sensitive information
        if any(sensitive in key_lower for sensitive in sensitive_keys):
            sanitized[key] = "[REDACTED]"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_log_data(value)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_log_data(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized
