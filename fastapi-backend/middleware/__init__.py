"""
Middleware components
"""
from .cors import setup_cors
from .logging import setup_logging
from .compression import setup_compression

try:
    from .rate_limiter import setup_rate_limiting
except ImportError:
    from .rate_limit import setup_rate_limiting

__all__ = ["setup_cors", "setup_logging", "setup_compression", "setup_rate_limiting"]
