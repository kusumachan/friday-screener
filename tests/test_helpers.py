"""
Unit tests untuk helper functions.
"""

import pytest

from src.utils.helpers import (
    calculate_percentage_change,
    format_currency,
    format_number,
    format_percentage,
    format_ratio,
    get_ticker_without_suffix,
    is_growing_trend,
    normalize_ticker,
    safe_float,
    safe_int,
)


class TestSafeConversions:
    """Tests untuk safe conversion functions."""

    def test_safe_float_with_valid_number(self):
        """Test safe_float dengan valid numbers."""
        assert safe_float(123) == 123.0
        assert safe_float(123.45) == 123.45
        assert safe_float("123.45") == 123.45

    def test_safe_float_with_invalid_input(self):
        """Test safe_float dengan invalid input."""
        assert safe_float(None) is None
        assert safe_float("invalid") is None
        assert safe_float("invalid", default=0.0) == 0.0

    def test_safe_float_with_formatted_strings(self):
        """Test safe_float dengan formatted strings."""
        assert safe_float("1,234.56") == 1234.56
        assert safe_float("$1,234.56") == 1234.56
        assert safe_float("25%") == 25.0

    def test_safe_int_with_valid_number(self):
        """Test safe_int dengan valid numbers."""
        assert safe_int(123) == 123
        assert safe_int(123.99) == 123
        assert safe_int("123") == 123

    def test_safe_int_with_invalid_input(self):
        """Test safe_int dengan invalid input."""
        assert safe_int(None) is None
        assert safe_int("invalid") is None
        assert safe_int("invalid", default=0) == 0


class TestFormatting:
    """Tests untuk formatting functions."""

    def test_format_currency_idr(self):
        """Test format_currency untuk IDR."""
        assert format_currency(1_500_000_000_000) == "Rp 1.50T"
        assert format_currency(2_500_000_000) == "Rp 2.50B"
        assert format_currency(500_000_000) == "Rp 500.00M"
        assert format_currency(2_000_000) == "Rp 2.00M"
        assert format_currency(5000) == "Rp 5,000"

    def test_format_currency_none(self):
        """Test format_currency dengan None."""
        assert format_currency(None) == "N/A"

    def test_format_percentage(self):
        """Test format_percentage."""
        assert format_percentage(0.25) == "25.00%"
        assert format_percentage(25) == "25.00%"
        assert format_percentage(None) == "N/A"

    def test_format_ratio(self):
        """Test format_ratio."""
        assert format_ratio(1.5) == "1.50x"
        assert format_ratio(0.75) == "0.75x"
        assert format_ratio(None) == "N/A"

    def test_format_number(self):
        """Test format_number."""
        assert format_number(1234567.89) == "1,234,567.89"
        assert format_number(None) == "N/A"


class TestTickerNormalization:
    """Tests untuk ticker normalization."""

    def test_normalize_ticker_indonesian(self):
        """Test normalize_ticker untuk Indonesian stocks."""
        assert normalize_ticker("BBCA") == "BBCA.JK"
        assert normalize_ticker("bbca") == "BBCA.JK"
        assert normalize_ticker("TLKM") == "TLKM.JK"

    def test_normalize_ticker_already_normalized(self):
        """Test normalize_ticker yang sudah ada suffix."""
        assert normalize_ticker("BBCA.JK") == "BBCA.JK"
        assert normalize_ticker("AAPL") == "AAPL.JK"  # Assumes Indonesian if no suffix

    def test_get_ticker_without_suffix(self):
        """Test get_ticker_without_suffix."""
        assert get_ticker_without_suffix("BBCA.JK") == "BBCA"
        assert get_ticker_without_suffix("BBCA") == "BBCA"


class TestTrendAnalysis:
    """Tests untuk trend analysis functions."""

    def test_is_growing_trend_positive(self):
        """Test is_growing_trend dengan growing trend."""
        values = [100, 110, 120, 130, 140]
        assert is_growing_trend(values, min_positive_years=3) is True

    def test_is_growing_trend_negative(self):
        """Test is_growing_trend dengan declining trend."""
        values = [140, 130, 120, 110, 100]
        assert is_growing_trend(values, min_positive_years=3) is False

    def test_is_growing_trend_mixed(self):
        """Test is_growing_trend dengan mixed trend."""
        values = [100, 110, 105, 120, 125]  # 3 positive, 1 negative
        assert is_growing_trend(values, min_positive_years=3) is True
        assert is_growing_trend(values, min_positive_years=4) is False

    def test_is_growing_trend_insufficient_data(self):
        """Test is_growing_trend dengan insufficient data."""
        assert is_growing_trend([100]) is False
        assert is_growing_trend([]) is False

    def test_calculate_percentage_change(self):
        """Test calculate_percentage_change."""
        assert calculate_percentage_change(100, 110) == 0.1  # 10% increase
        assert calculate_percentage_change(100, 90) == -0.1  # 10% decrease
        assert calculate_percentage_change(0, 100) == 0.0  # Handle zero
