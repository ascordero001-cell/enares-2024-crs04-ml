"""Configuration for the local Stage 04 application shell."""

from enares.stage04.modules import get_module, module_for_page

from .modules import (
    FUTURE_DIMENSIONS,
    MODULES,
    NAVIGATION,
    QUALITY_LABELS,
    SUPPORTED_FILTER,
)

__all__ = [
    "FUTURE_DIMENSIONS",
    "MODULES",
    "NAVIGATION",
    "QUALITY_LABELS",
    "SUPPORTED_FILTER",
    "get_module",
    "module_for_page",
]
