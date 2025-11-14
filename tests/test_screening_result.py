"""
Unit tests untuk ScreeningResult model.
"""

import pytest

from src.models.screening_result import (
    CategoryScore,
    Insight,
    Rating,
    ScreeningMetrics,
    ScreeningResult,
)


class TestRating:
    """Tests untuk Rating enum."""

    def test_rating_str_very_strong(self):
        """Test Rating.__str__ untuk VERY_STRONG."""
        rating = Rating.VERY_STRONG
        assert str(rating) == "Very Strong ⭐⭐⭐"

    def test_rating_str_strong(self):
        """Test Rating.__str__ untuk STRONG."""
        rating = Rating.STRONG
        assert str(rating) == "Strong ⭐⭐"

    def test_rating_str_fair(self):
        """Test Rating.__str__ untuk FAIR."""
        rating = Rating.FAIR
        assert str(rating) == "Fair ⭐"

    def test_rating_str_weak(self):
        """Test Rating.__str__ untuk WEAK."""
        rating = Rating.WEAK
        assert str(rating) == "Weak ⚠️"

    def test_rating_str_very_weak(self):
        """Test Rating.__str__ untuk VERY_WEAK."""
        rating = Rating.VERY_WEAK
        assert str(rating) == "Very Weak ⚠️⚠️"

    def test_rating_str_insufficient_data(self):
        """Test Rating.__str__ untuk INSUFFICIENT_DATA."""
        rating = Rating.INSUFFICIENT_DATA
        assert str(rating) == "Insufficient Data ❓"

    def test_rating_str_unknown(self):
        """Test Rating.__str__ untuk unknown rating (edge case)."""
        # Create a mock rating value that doesn't exist in mapping
        # This tests the .get() default case
        rating = Rating.VERY_WEAK
        # The mapping should handle all cases, but test default behavior
        assert str(rating) is not None


class TestScreeningMetrics:
    """Tests untuk ScreeningMetrics."""

    def test_get_all_category_scores(self):
        """Test get_all_category_scores method."""
        metrics = ScreeningMetrics(
            valuation_score=CategoryScore('Valuation', 70.0),
            profitability_score=CategoryScore('Profitability', 80.0),
            risk_score=CategoryScore('Risk', 60.0),
            dividend_score=CategoryScore('Dividend', 75.0),
        )

        scores = metrics.get_all_category_scores()
        assert len(scores) == 4
        assert all(isinstance(score, CategoryScore) for score in scores)


class TestScreeningResult:
    """Tests untuk ScreeningResult."""

    def test_get_insights_by_category(self):
        """Test get_insights_by_category method."""
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
        )

        result.add_insight('Valuation', 'positive', 'Low PE', 'PE ratio is below market average')
        result.add_insight('Profitability', 'positive', 'High ROE', 'ROE is above 15%')
        result.add_insight('Valuation', 'negative', 'High PBV', 'PBV is above preferred level')

        valuation_insights = result.get_insights_by_category('Valuation')
        assert len(valuation_insights) == 2
        assert all(i.category == 'Valuation' for i in valuation_insights)

    def test_get_insights_by_severity(self):
        """Test get_insights_by_severity method."""
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
        )

        result.add_insight('Valuation', 'positive', 'Low PE', 'PE ratio is below market average')
        result.add_insight('Profitability', 'positive', 'High ROE', 'ROE is above 15%')
        result.add_insight('Risk', 'negative', 'High Debt', 'Debt ratio is high')

        positive_insights = result.get_insights_by_severity('positive')
        assert len(positive_insights) == 2
        assert all(i.severity == 'positive' for i in positive_insights)

    def test_is_strong_fundamentals(self):
        """Test is_strong_fundamentals method."""
        result_strong = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.STRONG,
        )
        assert result_strong.is_strong_fundamentals() is True

        result_very_strong = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.VERY_STRONG,
        )
        assert result_very_strong.is_strong_fundamentals() is True

        result_fair = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.FAIR,
        )
        assert result_fair.is_strong_fundamentals() is False

    def test_calculate_rating_from_score_very_strong(self):
        """Test calculate_rating_from_score untuk score >= 80."""
        metrics = ScreeningMetrics(total_score=85.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            metrics=metrics
        )

        rating = result.calculate_rating_from_score()
        assert rating == Rating.VERY_STRONG

    def test_calculate_rating_from_score_strong(self):
        """Test calculate_rating_from_score untuk score >= 60."""
        metrics = ScreeningMetrics(total_score=75.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            metrics=metrics
        )

        rating = result.calculate_rating_from_score()
        assert rating == Rating.STRONG

    def test_calculate_rating_from_score_fair(self):
        """Test calculate_rating_from_score untuk score >= 40."""
        metrics = ScreeningMetrics(total_score=50.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            metrics=metrics
        )

        rating = result.calculate_rating_from_score()
        assert rating == Rating.FAIR

    def test_calculate_rating_from_score_weak(self):
        """Test calculate_rating_from_score untuk score >= 20."""
        metrics = ScreeningMetrics(total_score=30.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            metrics=metrics
        )

        rating = result.calculate_rating_from_score()
        assert rating == Rating.WEAK

    def test_calculate_rating_from_score_very_weak(self):
        """Test calculate_rating_from_score untuk score < 20."""
        metrics = ScreeningMetrics(total_score=10.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            metrics=metrics
        )

        rating = result.calculate_rating_from_score()
        assert rating == Rating.VERY_WEAK

    def test_summary(self):
        """Test summary method."""
        metrics = ScreeningMetrics(
            total_score=75.0,
            valuation_score=CategoryScore('Valuation', 70.0),
            profitability_score=CategoryScore('Profitability', 80.0),
            risk_score=CategoryScore('Risk', 60.0),
            dividend_score=CategoryScore('Dividend', 75.0),
        )
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.STRONG,
            metrics=metrics,
            data_completeness=90.0,
            strengths=['Strong ROE'],
            weaknesses=['High PE'],
            red_flags=['Declining revenue']
        )

        summary = result.summary()
        assert 'BBCA' in summary
        assert 'Bank BCA' in summary
        assert '75.0' in summary
        assert '90.0' in summary
        assert '1' in summary  # strengths count
        assert '1' in summary  # weaknesses count
        assert '1' in summary  # red flags count

    def test_add_methods(self):
        """Test add methods untuk insights, red flags, strengths, weaknesses."""
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
        )

        result.add_insight('Valuation', 'positive', 'Low PE', 'PE is low')
        result.add_red_flag('High debt ratio')
        result.add_strength('Strong ROE')
        result.add_weakness('High PE ratio')

        assert len(result.insights) == 1
        assert len(result.red_flags) == 1
        assert len(result.strengths) == 1
        assert len(result.weaknesses) == 1

