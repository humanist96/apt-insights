"""
Compression middleware configuration
"""
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware


def setup_compression(app: FastAPI) -> None:
    """
    Configure compression middleware for the FastAPI application

    Args:
        app: FastAPI application instance
    """
    # Add GZip compression middleware
    # Compresses responses larger than minimum_size (default 500 bytes)
    app.add_middleware(
        GZipMiddleware,
        minimum_size=500,  # Only compress responses larger than 500 bytes
        compresslevel=6,   # Compression level 1-9 (6 is a good balance of speed/compression)
    )
