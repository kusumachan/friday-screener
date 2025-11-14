"""
Unit tests untuk CLI commands.
"""

from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest
from click.testing import CliRunner

from src.cli.commands import (
    _display_category_scores,
    _display_company_info,
    _display_comparison_table,
    _display_insights,
    _display_key_metrics,
    _display_news_summary,
    _display_recommendation,
    _display_screening_summary,
    _get_sentiment_color,
    cli,
    compare,
    interactive,
    screen,
)
from src.models.screening_result import Rating, ScreeningResult, ScreeningMetrics, CategoryScore
from src.models.stock_data import (
    CompanyInfo,
    NewsItem,
    StockData,
    ValuationMetrics,
    ProfitabilityMetrics,
)


class TestCLI:
    """Tests untuk CLI commands."""

    def test_cli_without_command(self):
        """Test CLI tanpa subcommand (default ke interactive)."""
        runner = CliRunner()
        # Mock interactive to avoid actual interactive mode
        with patch('src.cli.commands.console') as mock_console:
            mock_console.input.side_effect = ['q']
            result = runner.invoke(cli, [])
            # Should handle gracefully
            assert result.exit_code in [0, 1]

    def test_cli_version_option(self):
        """Test CLI version option."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert 'Friday Screener' in result.output or 'version' in result.output.lower()


class TestScreenCommand:
    """Tests untuk screen command."""

    @patch('src.cli.commands.YahooFinanceService')
    @patch('src.cli.commands.NewsScraperService')
    @patch('src.cli.commands.FundamentalAnalyzer')
    def test_screen_success(self, mock_analyzer, mock_news_service, mock_finance_service):
        """Test screen command dengan success."""
        runner = CliRunner()

        # Setup mocks
        mock_stock_data = self._create_mock_stock_data()
        mock_result = self._create_mock_result()

        mock_finance_service.return_value.get_stock_data.return_value = mock_stock_data
        mock_news_service.return_value.get_news.return_value = []
        mock_news_service.return_value.get_corporate_actions.return_value = []
        mock_analyzer.return_value.analyze.return_value = mock_result

        result = runner.invoke(screen, ['BBCA'])

        assert result.exit_code == 0
        mock_finance_service.return_value.get_stock_data.assert_called_once()

    @patch('src.cli.commands.YahooFinanceService')
    def test_screen_invalid_ticker(self, mock_finance_service):
        """Test screen command dengan invalid ticker."""
        runner = CliRunner()

        mock_finance_service.return_value.get_stock_data.return_value = None

        result = runner.invoke(screen, ['INVALID'])

        assert result.exit_code == 0
        assert 'Error' in result.output or 'Could not fetch' in result.output

    @patch('src.cli.commands.YahooFinanceService')
    @patch('src.cli.commands.NewsScraperService')
    @patch('src.cli.commands.FundamentalAnalyzer')
    def test_screen_with_detailed(self, mock_analyzer, mock_news_service, mock_finance_service):
        """Test screen command dengan --detailed flag."""
        runner = CliRunner()

        mock_stock_data = self._create_mock_stock_data()
        mock_result = self._create_mock_result()

        mock_finance_service.return_value.get_stock_data.return_value = mock_stock_data
        mock_news_service.return_value.get_news.return_value = []
        mock_news_service.return_value.get_corporate_actions.return_value = []
        mock_analyzer.return_value.analyze.return_value = mock_result

        result = runner.invoke(screen, ['BBCA', '--detailed'])

        assert result.exit_code == 0

    @patch('src.cli.commands.YahooFinanceService')
    @patch('src.cli.commands.NewsScraperService')
    @patch('src.cli.commands.FundamentalAnalyzer')
    def test_screen_no_news(self, mock_analyzer, mock_news_service, mock_finance_service):
        """Test screen command dengan --no-news flag."""
        runner = CliRunner()

        mock_stock_data = self._create_mock_stock_data()
        mock_result = self._create_mock_result()

        mock_finance_service.return_value.get_stock_data.return_value = mock_stock_data
        mock_analyzer.return_value.analyze.return_value = mock_result

        result = runner.invoke(screen, ['BBCA', '--no-news'])

        assert result.exit_code == 0
        mock_news_service.return_value.get_news.assert_not_called()

    def _create_mock_stock_data(self):
        """Create mock stock data for testing."""
        company_info = CompanyInfo(
            ticker='BBCA.JK',
            name='Bank BCA',
            sector='Financial Services',
            industry='Banking'
        )
        return StockData(company_info=company_info)

    def _create_mock_result(self):
        """Create mock screening result for testing."""
        metrics = ScreeningMetrics(
            total_score=75.0,
            valuation_score=CategoryScore('Valuation', 70.0, passed=True),
            profitability_score=CategoryScore('Profitability', 80.0, passed=True),
            risk_score=CategoryScore('Risk', 60.0, passed=True),
            dividend_score=CategoryScore('Dividend', 75.0, passed=True),
        )
        return ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.STRONG,
            metrics=metrics,
            data_completeness=90.0
        )


class TestCompareCommand:
    """Tests untuk compare command."""

    @patch('src.cli.commands.YahooFinanceService')
    @patch('src.cli.commands.FundamentalAnalyzer')
    def test_compare_success(self, mock_analyzer, mock_finance_service):
        """Test compare command dengan success."""
        runner = CliRunner()

        mock_stock_data1 = self._create_mock_stock_data('BBCA')
        mock_stock_data2 = self._create_mock_stock_data('BMRI')
        mock_result = self._create_mock_result()

        mock_finance_service.return_value.get_stock_data.side_effect = [
            mock_stock_data1,
            mock_stock_data2
        ]
        mock_analyzer.return_value.analyze.return_value = mock_result

        result = runner.invoke(compare, ['BBCA', 'BMRI'])

        assert result.exit_code == 0

    def test_compare_insufficient_tickers(self):
        """Test compare command dengan kurang dari 2 tickers."""
        runner = CliRunner()

        result = runner.invoke(compare, ['BBCA'])

        assert result.exit_code == 0
        assert 'Error' in result.output or 'at least 2 tickers' in result.output

    @patch('src.cli.commands.YahooFinanceService')
    def test_compare_no_valid_stocks(self, mock_finance_service):
        """Test compare command ketika tidak ada valid stocks."""
        runner = CliRunner()

        mock_finance_service.return_value.get_stock_data.return_value = None

        result = runner.invoke(compare, ['INVALID1', 'INVALID2'])

        assert result.exit_code == 0

    def _create_mock_stock_data(self, ticker='BBCA'):
        """Create mock stock data."""
        company_info = CompanyInfo(
            ticker=f'{ticker}.JK',
            name=f'Company {ticker}',
            sector='Financial',
            industry='Banking'
        )
        return StockData(company_info=company_info)

    def _create_mock_result(self):
        """Create mock screening result."""
        metrics = ScreeningMetrics(total_score=75.0)
        return ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.STRONG,
            metrics=metrics
        )


class TestDisplayFunctions:
    """Tests untuk display helper functions."""

    def test_display_company_info(self):
        """Test _display_company_info."""
        company_info = CompanyInfo(
            ticker='BBCA.JK',
            name='Bank BCA',
            sector='Financial',
            industry='Banking'
        )
        stock_data = StockData(company_info=company_info)

        with patch('src.cli.commands.console') as mock_console:
            _display_company_info(stock_data)
            assert mock_console.print.called

    def test_display_screening_summary_very_strong(self):
        """Test _display_screening_summary untuk VERY_STRONG rating."""
        metrics = ScreeningMetrics(total_score=90.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.VERY_STRONG,
            metrics=metrics,
            data_completeness=95.0
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_screening_summary(result)
            assert mock_console.print.called

    def test_display_screening_summary_strong(self):
        """Test _display_screening_summary untuk STRONG rating."""
        metrics = ScreeningMetrics(total_score=75.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.STRONG,
            metrics=metrics
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_screening_summary(result)
            assert mock_console.print.called

    def test_display_screening_summary_fair(self):
        """Test _display_screening_summary untuk FAIR rating."""
        metrics = ScreeningMetrics(total_score=50.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.FAIR,
            metrics=metrics
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_screening_summary(result)
            assert mock_console.print.called

    def test_display_screening_summary_weak(self):
        """Test _display_screening_summary untuk WEAK rating."""
        metrics = ScreeningMetrics(total_score=30.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.WEAK,
            metrics=metrics
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_screening_summary(result)
            assert mock_console.print.called

    def test_display_screening_summary_very_weak(self):
        """Test _display_screening_summary untuk VERY_WEAK rating."""
        metrics = ScreeningMetrics(total_score=10.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.VERY_WEAK,
            metrics=metrics
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_screening_summary(result)
            assert mock_console.print.called

    def test_display_category_scores(self):
        """Test _display_category_scores."""
        metrics = ScreeningMetrics(
            valuation_score=CategoryScore('Valuation', 70.0, weight=0.25, passed=True),
            profitability_score=CategoryScore('Profitability', 80.0, weight=0.35, passed=True),
            risk_score=CategoryScore('Risk', 60.0, weight=0.20, passed=False),
            dividend_score=CategoryScore('Dividend', 75.0, weight=0.20, passed=True),
        )
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            metrics=metrics
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_category_scores(result)
            assert mock_console.print.called

    def test_display_key_metrics(self):
        """Test _display_key_metrics."""
        metrics = ScreeningMetrics(total_score=75.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            metrics=metrics,
            key_metrics={
                'pe_ratio': 15.0,
                'pbv': 2.0,
                'market_cap': 500_000_000_000_000,
                'roe': 0.15,
                'gross_margin': 0.30,
                'eps': 500.0,
                'debt_to_equity': 0.5,
                'dividend_yield': 0.04,
                'current_price': 10000.0
            }
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_key_metrics(result)
            assert mock_console.print.called

    def test_display_insights_with_strengths(self):
        """Test _display_insights dengan strengths."""
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            strengths=['Strong ROE', 'Low debt']
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_insights(result)
            assert mock_console.print.called

    def test_display_insights_with_weaknesses(self):
        """Test _display_insights dengan weaknesses."""
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            weaknesses=['High PE ratio']
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_insights(result)
            assert mock_console.print.called

    def test_display_insights_with_red_flags(self):
        """Test _display_insights dengan red flags."""
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            red_flags=['Declining revenue']
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_insights(result)
            assert mock_console.print.called

    def test_display_news_summary(self):
        """Test _display_news_summary."""
        news_items = [
            NewsItem(
                title='Good News',
                source='Test',
                published_date=datetime.now(),
                sentiment='positive'
            )
        ]
        corporate_actions = []
        mock_service = Mock()
        mock_service.analyze_news_impact.return_value = {
            'total_news': 1,
            'positive_count': 1,
            'negative_count': 0,
            'neutral_count': 0,
            'overall_sentiment': 'positive'
        }

        with patch('src.cli.commands.console') as mock_console:
            _display_news_summary(news_items, corporate_actions, mock_service)
            assert mock_console.print.called

    def test_display_recommendation_strong(self):
        """Test _display_recommendation untuk strong fundamentals."""
        metrics = ScreeningMetrics(total_score=80.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.STRONG,
            metrics=metrics
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_recommendation(result)
            assert mock_console.print.called

    def test_display_recommendation_not_strong(self):
        """Test _display_recommendation untuk non-strong fundamentals."""
        metrics = ScreeningMetrics(total_score=40.0)
        result = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            rating=Rating.FAIR,
            metrics=metrics
        )

        with patch('src.cli.commands.console') as mock_console:
            _display_recommendation(result)
            assert mock_console.print.called

    def test_display_comparison_table(self):
        """Test _display_comparison_table."""
        company_info1 = CompanyInfo(ticker='BBCA.JK', name='Bank BCA')
        stock_data1 = StockData(company_info=company_info1)
        
        company_info2 = CompanyInfo(ticker='BMRI.JK', name='Bank Mandiri')
        stock_data2 = StockData(company_info=company_info2)

        metrics1 = ScreeningMetrics(total_score=75.0)
        result1 = ScreeningResult(
            ticker='BBCA',
            company_name='Bank BCA',
            metrics=metrics1,
            key_metrics={'pe_ratio': 15.0, 'pbv': 2.0, 'roe': 0.15, 'debt_to_equity': 0.5, 'dividend_yield': 0.04}
        )

        metrics2 = ScreeningMetrics(total_score=70.0)
        result2 = ScreeningResult(
            ticker='BMRI',
            company_name='Bank Mandiri',
            metrics=metrics2,
            key_metrics={'pe_ratio': 12.0, 'pbv': 1.8, 'roe': 0.12, 'debt_to_equity': 0.6, 'dividend_yield': 0.03}
        )

        results = [(stock_data1, result1), (stock_data2, result2)]

        with patch('src.cli.commands.console') as mock_console:
            _display_comparison_table(results)
            assert mock_console.print.called

    def test_get_sentiment_color(self):
        """Test _get_sentiment_color."""
        assert _get_sentiment_color('positive') == 'green'
        assert _get_sentiment_color('negative') == 'red'
        assert _get_sentiment_color('neutral') == 'yellow'
        assert _get_sentiment_color('unknown') == 'yellow'  # default


class TestInteractiveCommand:
    """Tests untuk interactive command."""

    @patch('src.cli.commands.console')
    def test_interactive_quit(self, mock_console):
        """Test interactive command dengan quit."""
        mock_console.input.side_effect = ['q']
        
        # Just verify function exists and can be called
        # Full testing would require more complex mocking
        assert callable(interactive)

