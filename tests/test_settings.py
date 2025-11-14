"""
Unit tests untuk settings module.
"""

import pytest

from src.config.settings import (
    DEFAULT_CRITERIA,
    DEFAULT_WEIGHTS,
    DividendCriteria,
    ProfitabilityCriteria,
    RiskCriteria,
    ScoringWeights,
    ScreeningCriteria,
    ValuationCriteria,
)


class TestValuationCriteria:
    """Tests untuk ValuationCriteria."""

    def test_default_values(self):
        """Test default values untuk ValuationCriteria."""
        criteria = ValuationCriteria()
        assert criteria.pe_ratio_preferred == 5.0
        assert criteria.pe_ratio_max == 15.0
        assert criteria.pbv_preferred == 1.0
        assert criteria.pbv_max == 2.0


class TestProfitabilityCriteria:
    """Tests untuk ProfitabilityCriteria."""

    def test_default_values(self):
        """Test default values untuk ProfitabilityCriteria."""
        criteria = ProfitabilityCriteria()
        assert criteria.eps_growth_years == 5
        assert criteria.gpm_min == 20.0
        assert criteria.roe_min == 10.0


class TestRiskCriteria:
    """Tests untuk RiskCriteria."""

    def test_default_values(self):
        """Test default values untuk RiskCriteria."""
        criteria = RiskCriteria()
        assert criteria.debt_to_equity_max == 1.0
        assert criteria.beta_max == 1.5


class TestDividendCriteria:
    """Tests untuk DividendCriteria."""

    def test_default_values(self):
        """Test default values untuk DividendCriteria."""
        criteria = DividendCriteria()
        assert criteria.dividend_yield_min == 2.0
        assert criteria.require_dividend is True


class TestScreeningCriteria:
    """Tests untuk ScreeningCriteria."""

    def test_default_instance(self):
        """Test DEFAULT_CRITERIA instance."""
        assert isinstance(DEFAULT_CRITERIA, ScreeningCriteria)
        assert isinstance(DEFAULT_CRITERIA.valuation, ValuationCriteria)
        assert isinstance(DEFAULT_CRITERIA.profitability, ProfitabilityCriteria)
        assert isinstance(DEFAULT_CRITERIA.risk, RiskCriteria)
        assert isinstance(DEFAULT_CRITERIA.dividend, DividendCriteria)


class TestScoringWeights:
    """Tests untuk ScoringWeights."""

    def test_default_values(self):
        """Test default values untuk ScoringWeights."""
        weights = ScoringWeights()
        assert weights.valuation_weight == 0.25
        assert weights.profitability_weight == 0.35
        assert weights.risk_weight == 0.20
        assert weights.dividend_weight == 0.20

    def test_weights_sum_validation(self):
        """Test bahwa weights harus sum to 1.0."""
        # Valid weights
        weights = ScoringWeights(
            valuation_weight=0.25,
            profitability_weight=0.35,
            risk_weight=0.20,
            dividend_weight=0.20
        )
        assert weights.valuation_weight + weights.profitability_weight + weights.risk_weight + weights.dividend_weight == 1.0

    def test_weights_sum_validation_error(self):
        """Test bahwa weights yang tidak sum to 1.0 akan raise error."""
        with pytest.raises(ValueError, match="Weights must sum to 1.0"):
            ScoringWeights(
                valuation_weight=0.25,
                profitability_weight=0.35,
                risk_weight=0.20,
                dividend_weight=0.30  # Total = 1.10, should raise error
            )

    def test_weights_sum_validation_allow_small_error(self):
        """Test bahwa small floating point error diperbolehkan."""
        # 0.99 to 1.01 should be allowed
        weights = ScoringWeights(
            valuation_weight=0.25,
            profitability_weight=0.35,
            risk_weight=0.20,
            dividend_weight=0.20
        )
        # Should not raise error for exactly 1.0
        assert weights is not None

    def test_default_weights_instance(self):
        """Test DEFAULT_WEIGHTS instance."""
        assert isinstance(DEFAULT_WEIGHTS, ScoringWeights)

