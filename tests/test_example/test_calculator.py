"""Tests for the calculator module."""

import pytest
from average_price_calculator import (
    PriceData,
    CalculationResult,
    calculate_average_price,
    calculate_average_price_safe,
)


class TestPriceData:
    """Test PriceData model."""
    
    def test_valid_data(self):
        """Test valid data creation."""
        data = PriceData(
            initial_quantity=100.0,
            initial_price=10.5,
            new_quantity=50.0,
            new_price=12.0,
        )
        assert data.initial_quantity == 100.0
        assert data.initial_price == 10.5
    
    def test_invalid_data_negative(self):
        """Test with negative values."""
        with pytest.raises(ValueError):
            PriceData(
                initial_quantity=-100.0,
                initial_price=10.5,
                new_quantity=50.0,
                new_price=12.0,
            )
    
    def test_zero_values(self):
        """Test with zero values."""
        with pytest.raises(ValueError):
            PriceData(
                initial_quantity=0.0,
                initial_price=10.5,
                new_quantity=50.0,
                new_price=12.0,
            )


class TestCalculateAveragePrice:
    """Test calculate_average_price function."""
    
    def test_basic_calculation(self):
        """Test basic calculation."""
        result = calculate_average_price(100, 10, 100, 20)
        assert result[0] == 15.0  # Average price
        assert result[1] == 200.0  # Total quantity
        assert result[2] == 3000.0  # Total investment
    
    def test_decimal_values(self):
        """Test with decimal values from GUI."""
        result = calculate_average_price(4.37562, 3.602, 2.93867, 2.11, precision=6)
        
        # Manual calculation for verification
        total_inv = (4.37562 * 3.602) + (2.93867 * 2.11)
        total_qty = 4.37562 + 2.93867
        expected_avg = total_inv / total_qty
        
        assert pytest.approx(result[0], abs=1e-6) == expected_avg
        assert pytest.approx(result[1], abs=1e-6) == total_qty
        assert pytest.approx(result[2], abs=1e-6) == total_inv
    
    def test_zero_total_quantity(self):
        """Test with zero total quantity."""
        with pytest.raises(ZeroDivisionError):
            calculate_average_price(0, 10, 0, 20)
    
    def test_precision(self):
        """Test decimal precision."""
        result = calculate_average_price(100, 10.123456, 50, 20.987654, precision=2)
        assert len(str(result[0]).split('.')[1]) <= 2


class TestCalculateAveragePriceSafe:
    """Test calculate_average_price_safe function."""
    
    def test_safe_calculation(self):
        """Test safe calculation with Pydantic."""
        data = PriceData(
            initial_quantity=100.0,
            initial_price=10.5,
            new_quantity=50.0,
            new_price=12.0,
        )
        
        result = calculate_average_price_safe(data)
        
        assert isinstance(result, CalculationResult)
        assert result.average_price > 0
        assert result.total_quantity == 150.0
    
    def test_with_precision(self):
        """Test with custom precision."""
        data = PriceData(
            initial_quantity=100.0,
            initial_price=10.555555,
            new_quantity=50.0,
            new_price=12.333333,
        )
        
        result = calculate_average_price_safe(data, precision=3)
        assert len(str(result.average_price).split('.')[1]) <= 3


@pytest.mark.parametrize("q1,p1,q2,p2,expected_avg", [
    (100, 10, 100, 10, 10.0),
    (100, 10, 100, 20, 15.0),
    (100, 10, 50, 20, 13.333333),
    (1000, 5, 500, 10, 6.666667),
])
def test_parametrized_calculations(q1, p1, q2, p2, expected_avg):
    """Parametrized tests for various scenarios."""
    result = calculate_average_price(q1, p1, q2, p2)
    assert pytest.approx(result[0], abs=1e-6) == expected_avg


def test_cli_integration():
    """Test that CLI can be imported."""
    from average_price_calculator.cli import app
    assert app is not None
    assert hasattr(app, '__call__')