"""View-model composition for the local application."""

from .stage04_dashboard import (
    EXPORT_ENABLED,
    build_numeric_card,
    build_suppressed_card,
    filter_estimates,
)

__all__ = [
    "EXPORT_ENABLED",
    "build_numeric_card",
    "build_suppressed_card",
    "filter_estimates",
]
