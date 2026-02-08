"""
API routers
"""
from .analysis import router as analysis_router
from .segmentation import router as segmentation_router
from .premium import router as premium_router
from .investment import router as investment_router
from .market import router as market_router
from .payment import router as payment_router
from .subscriptions import router as subscriptions_router
from .export import router as export_router

__all__ = [
    "analysis_router",
    "segmentation_router",
    "premium_router",
    "investment_router",
    "market_router",
    "payment_router",
    "subscriptions_router",
    "export_router",
]
