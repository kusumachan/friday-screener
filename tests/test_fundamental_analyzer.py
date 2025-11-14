"""
Unit tests untuk FundamentalAnalyzer.
"""

import pytest

from src.analyzers.fundamental_analyzer import FundamentalAnalyzer
from src.config.settings import ScreeningCriteria
from src.models.screening_result import Rating
from src.models.stock_data import (
    CompanyInfo,
    DividendMetrics,
    LeverageMetrics,
    ProfitabilityMetrics,
    StockData,
    ValuationMetrics,
)


@pytest.fixture
def good_stock_data():
    """Create mock data for a fundamentally strong stock."""
    company_info = CompanyInfo(
        ticker="BBCA.JK",
        name="Bank Central Asia Tbk",
        sector="Financial Services",
        industry="Banking",
    )

    valuation = ValuationMetrics(
        market_cap=100_000_000_000_000,  # 100T
        pe_ratio=10.0,
        price_to_book=1.5,
    )

    profitability = ProfitabilityMetrics(
        eps=500,
        roe=0.20,  # 20%
        gross_margin=0.35,  # 35%
        eps_history={
            2019: 400,
            2020: 420,
            2021: 450,
            2022: 480,
            2023: 500,
        },
    )

    leverage = LeverageMetrics(
        debt_to_equity=0.3, beta=0.9
    )

    dividend = DividendMetrics(
        dividend_yield=0.045  # 4.5%
    )

    return StockData(
        company_info=company_info,
        valuation=valuation,
        profitability=profitability,
        leverage=leverage,
        dividend=dividend,
        data_quality_score=95.0,
    )


@pytest.fixture
def poor_stock_data():
    """Create mock data for a fundamentally weak stock."""
    company_info = CompanyInfo(
        ticker="POOR.JK",
        name="Poor Company",
        sector="Technology",
    )

    valuation = ValuationMetrics(
        market_cap=500_000_000_000,  # 500B (small)
        pe_ratio=25.0,  # High
        price_to_book=3.0,  # High
    )

    profitability = ProfitabilityMetrics(
        eps=50,
        roe=0.05,  # 5% (low)
        gross_margin=0.15,  # 15% (low)
        eps_history={
            2019: 100,
            2020: 80,
            2021: 70,
            2022: 60,
            2023: 50,  # Declining
        },
    )

    leverage = LeverageMetrics(
        debt_to_equity=2.0,  # High debt
        beta=1.8,  # High volatility
    )

    dividend = DividendMetrics(
        dividend_yield=0.01  # 1% (low)
    )

    return StockData(
        company_info=company_info,
        valuation=valuation,
        profitability=profitability,
        leverage=leverage,
        dividend=dividend,
        data_quality_score=85.0,
    )


class TestFundamentalAnalyzer:
    """Tests untuk FundamentalAnalyzer."""

    def test_analyze_good_stock(self, good_stock_data):
        """Test analysis of fundamentally strong stock."""
        analyzer = FundamentalAnalyzer()
        result = analyzer.analyze(good_stock_data)

        # Should get good rating
        assert result.rating in [Rating.STRONG, Rating.VERY_STRONG]
        assert result.metrics.total_score >= 60

        # Should have strengths
        assert len(result.strengths) > 0

        # Check individual category scores
        assert result.metrics.valuation_score.score > 50
        assert result.metrics.profitability_score.score > 50
        assert result.metrics.risk_score.score > 50
        assert result.metrics.dividend_score.score > 50

    def test_analyze_poor_stock(self, poor_stock_data):
        """Test analysis of fundamentally weak stock."""
        analyzer = FundamentalAnalyzer()
        result = analyzer.analyze(poor_stock_data)

        # Should get poor rating
        assert result.rating in [Rating.WEAK, Rating.FAIR, Rating.VERY_WEAK]
        assert result.metrics.total_score < 60

        # Should have weaknesses or red flags
        assert len(result.weaknesses) + len(result.red_flags) > 0

    def test_valuation_scoring(self, good_stock_data):
        """Test valuation category scoring."""
        analyzer = FundamentalAnalyzer()
        result = analyzer.analyze(good_stock_data)

        # Good stock should pass valuation
        assert result.metrics.valuation_score.passed is True
        assert result.metrics.valuation_score.score > 0

    def test_profitability_scoring(self, good_stock_data):
        """Test profitability category scoring."""
        analyzer = FundamentalAnalyzer()
        result = analyzer.analyze(good_stock_data)

        # Good stock should pass profitability
        assert result.metrics.profitability_score.passed is True
        assert result.metrics.profitability_score.score > 0

        # Should recognize EPS growth
        assert any('EPS' in s for s in result.strengths)

    def test_risk_scoring(self, good_stock_data):
        """Test risk category scoring."""
        analyzer = FundamentalAnalyzer()
        result = analyzer.analyze(good_stock_data)

        # Good stock should pass risk assessment
        assert result.metrics.risk_score.passed is True
        assert result.metrics.risk_score.score > 0

    def test_dividend_scoring(self, good_stock_data):
        """Test dividend category scoring."""
        analyzer = FundamentalAnalyzer()
        result = analyzer.analyze(good_stock_data)

        # Good stock with dividend should pass
        assert result.metrics.dividend_score.score > 0

    def test_rating_calculation(self, good_stock_data, poor_stock_data):
        """Test rating calculation from score."""
        analyzer = FundamentalAnalyzer()

        # Good stock
        good_result = analyzer.analyze(good_stock_data)
        assert good_result.rating == good_result.calculate_rating_from_score()

        # Poor stock
        poor_result = analyzer.analyze(poor_stock_data)
        assert poor_result.rating == poor_result.calculate_rating_from_score()

    def test_incomplete_data_handling(self):
        """Test handling of incomplete data."""
        company_info = CompanyInfo(ticker="INCOMPLETE.JK", name="Incomplete")

        # Minimal data
        stock_data = StockData(
            company_info=company_info,
            data_quality_score=30.0,
        )

        analyzer = FundamentalAnalyzer()
        result = analyzer.analyze(stock_data)

        # Should handle incomplete data gracefully
        assert result is not None
        assert len(result.weaknesses) > 0

    def test_batch_analyze(self, good_stock_data, poor_stock_data):
        """Test batch analysis of multiple stocks."""
        analyzer = FundamentalAnalyzer()
        stocks = [good_stock_data, poor_stock_data]

        results = analyzer.batch_analyze(stocks)

        # Should return results for all stocks
        assert len(results) == 2

        # Should be sorted by score (descending)
        assert results[0].metrics.total_score >= results[1].metrics.total_score

    def test_custom_criteria(self, good_stock_data):
        """Test analyzer with custom criteria."""
        # Create strict criteria
        strict_criteria = ScreeningCriteria()
        strict_criteria.valuation.pe_ratio_max = 5.0  # Very strict

        analyzer = FundamentalAnalyzer(criteria=strict_criteria)
        result = analyzer.analyze(good_stock_data)

        # Even good stock might not pass strict criteria
        assert result is not None
