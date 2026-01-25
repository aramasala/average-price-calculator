# mypy: disable-error-code="attr-defined"
"""A tool for calculating weighted average prices after additional purchases"""

from importlib import metadata as importlib_metadata


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


__version__: str = get_version()

# Export main functions and classes
from .calculator import calculate_average_price, calculate_average_price_safe
from .models import PriceData, CalculationResult

__all__ = [
    "__version__",
    "calculate_average_price",
    "calculate_average_price_safe",
    "PriceData",
    "CalculationResult",
]

