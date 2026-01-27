"""Main calculator logic."""

from decimal import ROUND_HALF_UP, Decimal

from .models import CalculationResult, PriceData


def calculate_average_price(
    initial_quantity: float,
    initial_price: float,
    new_quantity: float,
    new_price: float,
    precision: int = 6,
) -> tuple[float, float, float]:
    """
    Calculate the weighted average price after additional purchase.

    Parameters
    ----------
    initial_quantity : float
        Initial quantity
    initial_price : float
        Initial average price
    new_quantity : float
        Newly purchased quantity
    new_price : float
        New purchase price
    precision : int
        Decimal precision for rounding

    Returns
    -------
    tuple
        (new average price, total quantity, total investment)

    Raises
    ------
    ValueError
        If any input is invalid
    ZeroDivisionError
        If total quantity is zero
    """
    # Validate inputs
    if any(x <= 0 for x in [initial_quantity, initial_price, new_quantity, new_price]):
        raise ValueError("All values must be positive")

    # Calculate using Decimal for better precision
    total_investment = Decimal(str(initial_quantity)) * Decimal(str(initial_price)) + Decimal(
        str(new_quantity)
    ) * Decimal(str(new_price))

    total_quantity = Decimal(str(initial_quantity)) + Decimal(str(new_quantity))

    if total_quantity == 0:
        raise ZeroDivisionError("Total quantity cannot be zero")

    average_price = total_investment / total_quantity

    # Round with specified precision
    rounding_format = f"0.{'0' * precision}"

    avg_price_rounded = float(
        average_price.quantize(Decimal(rounding_format), rounding=ROUND_HALF_UP)
    )
    total_qty_rounded = float(
        total_quantity.quantize(Decimal(rounding_format), rounding=ROUND_HALF_UP)
    )
    total_inv_rounded = float(
        total_investment.quantize(Decimal(rounding_format), rounding=ROUND_HALF_UP)
    )

    return avg_price_rounded, total_qty_rounded, total_inv_rounded


def calculate_average_price_safe(data: PriceData, precision: int = 6) -> CalculationResult:
    """
    Type-safe version of average price calculation.

    Parameters
    ----------
    data : PriceData
        Input data for calculation
    precision : int
        Decimal precision for rounding

    Returns
    -------
    CalculationResult
        Calculation results

    Raises
    ------
    ValueError
        If input data is invalid
    """
    avg_price, total_qty, total_inv = calculate_average_price(
        data.initial_quantity,
        data.initial_price,
        data.new_quantity,
        data.new_price,
        precision,
    )

    return CalculationResult(
        average_price=avg_price,
        total_quantity=total_qty,
        total_investment=total_inv,
    )
