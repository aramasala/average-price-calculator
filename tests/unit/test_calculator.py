"""Tests for the calculator module."""

import pytest
from pathlib import Path

# Use relative import
try:
    from average_price_calculator import (
        PriceData,
        CalculationResult,
        calculate_average_price,
        calculate_average_price_safe,
    )
    from average_price_calculator.cli import app
except ImportError:
    # For development without installation
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from average_price_calculator import (
        PriceData,
        CalculationResult,
        calculate_average_price,
        calculate_average_price_safe,
    )
    from average_price_calculator.cli import app

# Constants for tests
INITIAL_QTY = 100.0
INITIAL_PRICE = 10.5
NEW_QTY = 50.0
NEW_PRICE = 12.0
ZERO = 0.0
PRECISION_2 = 2
PRECISION_3 = 3
EXPECTED_AVG = 15.0
EXPECTED_TOTAL_QTY = 200.0
EXPECTED_TOTAL_INV = 3000.0
RESULT_150 = 150.0


class TestPriceData:
    """Test PriceData model."""

    def test_valid_data(self) -> None:
        """Test valid data creation."""
        data = PriceData(
            initial_quantity=INITIAL_QTY,
            initial_price=INITIAL_PRICE,
            new_quantity=NEW_QTY,
            new_price=NEW_PRICE,
        )
        assert data.initial_quantity == INITIAL_QTY
        assert data.initial_price == INITIAL_PRICE

    def test_invalid_data_negative(self) -> None:
        """Test with negative values."""
        with pytest.raises(ValueError):
            PriceData(
                initial_quantity=-INITIAL_QTY,
                initial_price=INITIAL_PRICE,
                new_quantity=NEW_QTY,
                new_price=NEW_PRICE,
            )

    def test_zero_values(self) -> None:
        """Test with zero values."""
        with pytest.raises(ValueError):
            PriceData(
                initial_quantity=ZERO,
                initial_price=INITIAL_PRICE,
                new_quantity=NEW_QTY,
                new_price=NEW_PRICE,
            )


class TestCalculateAveragePrice:
    """Test calculate_average_price function."""

    def test_basic_calculation(self) -> None:
        """Test basic calculation."""
        result = calculate_average_price(100, 10, 100, 20)
        assert result[0] == EXPECTED_AVG
        assert result[1] == EXPECTED_TOTAL_QTY
        assert result[2] == EXPECTED_TOTAL_INV

    def test_decimal_values(self) -> None:
        """Test with decimal values from GUI."""
        result = calculate_average_price(4.37562, 3.602, 2.93867, 2.11, precision=6)

        # Manual calculation for verification
        total_inv = (4.37562 * 3.602) + (2.93867 * 2.11)
        total_qty = 4.37562 + 2.93867
        expected_avg = total_inv / total_qty

        assert pytest.approx(result[0], abs=1e-6) == expected_avg
        assert pytest.approx(result[1], abs=1e-6) == total_qty
        assert pytest.approx(result[2], abs=1e-6) == total_inv

    def test_zero_total_quantity(self) -> None:
        """Test with zero total quantity - should raise ValueError."""
        with pytest.raises(ValueError, match="All values must be positive"):
            calculate_average_price(0, 10, 0, 20)

    def test_partial_zero_quantity(self) -> None:
        """Test with partial zero quantity."""
        # Initial quantity is 0, but new quantity is positive
        with pytest.raises(ValueError, match="All values must be positive"):
            calculate_average_price(0, 10, 100, 20)

        # New quantity is 0, but initial quantity is positive
        with pytest.raises(ValueError, match="All values must be positive"):
            calculate_average_price(100, 10, 0, 20)

    def test_precision(self) -> None:
        """Test decimal precision."""
        result = calculate_average_price(100, 10.123456, 50, 20.987654, precision=2)
        assert len(str(result[0]).split(".")[1]) <= PRECISION_2


class TestCalculateAveragePriceSafe:
    """Test calculate_average_price_safe function."""

    def test_safe_calculation(self) -> None:
        """Test safe calculation with Pydantic."""
        data = PriceData(
            initial_quantity=INITIAL_QTY,
            initial_price=INITIAL_PRICE,
            new_quantity=NEW_QTY,
            new_price=NEW_PRICE,
        )

        result = calculate_average_price_safe(data)

        assert isinstance(result, CalculationResult)
        assert result.average_price > 0
        assert result.total_quantity == RESULT_150

    def test_with_precision(self) -> None:
        """Test with custom precision."""
        data = PriceData(
            initial_quantity=100.0,
            initial_price=10.555555,
            new_quantity=50.0,
            new_price=12.333333,
        )

        result = calculate_average_price_safe(data, precision=PRECISION_3)
        assert len(str(result.average_price).split(".")[1]) <= PRECISION_3


@pytest.mark.parametrize(
    ("q1", "p1", "q2", "p2", "expected_avg"),
    [
        (100, 10, 100, 10, 10.0),
        (100, 10, 100, 20, 15.0),
        (100, 10, 50, 20, 13.333333),
        (1000, 5, 500, 10, 6.666667),
    ],
)
def test_parametrized_calculations(
    q1: float, p1: float, q2: float, p2: float, expected_avg: float
) -> None:
    """Parametrized tests for various scenarios."""
    result = calculate_average_price(q1, p1, q2, p2)
    assert pytest.approx(result[0], abs=1e-6) == expected_avg


def test_cli_integration() -> None:
    """Test that CLI can be imported."""
    assert app is not None
    assert callable(app)
