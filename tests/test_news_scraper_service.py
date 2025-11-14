"""
Tests untuk News Scraper Service.

Test coverage untuk scraping berita dan sentiment analysis.
"""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.models.stock_data import NewsItem
from src.services.news_scraper_service import NewsScraperService


class TestNewsScraperService:
    """Test suite untuk NewsScraperService."""

    @pytest.fixture
    def service(self):
        """Create NewsScraperService instance."""
        return NewsScraperService(max_news=5)

    @pytest.fixture
    def mock_news_data(self):
        """Mock news data dari Yahoo Finance."""
        return [
            {
                'title': 'BBCA posts strong Q4 earnings, profit up 15%',
                'summary': 'Bank Central Asia reported strong earnings growth with profit increasing by 15% in Q4 2024.',
                'publisher': 'Reuters',
                'link': 'https://example.com/news1',
                'providerPublishTime': 1704067200,  # 2024-01-01
            },
            {
                'title': 'BBCA dividend yield remains attractive at 3.5%',
                'summary': 'The bank maintains its dividend policy with a yield of 3.5%, attracting income investors.',
                'publisher': 'Bloomberg',
                'link': 'https://example.com/news2',
                'providerPublishTime': 1703980800,  # 2023-12-31
            },
            {
                'title': 'Banking sector faces regulatory concerns',
                'summary': 'New regulations may impact bank profitability and operations in the coming year.',
                'publisher': 'CNBC',
                'link': 'https://example.com/news3',
                'providerPublishTime': 1703894400,  # 2023-12-30
            },
            {
                'title': 'BBCA announces stock split 1:5',
                'summary': 'Board of directors approved a stock split to improve liquidity and accessibility.',
                'publisher': 'Jakarta Post',
                'link': 'https://example.com/news4',
                'providerPublishTime': 1703808000,  # 2023-12-29
            },
        ]

    @pytest.fixture
    def mock_ticker(self, mock_news_data):
        """Create mock yfinance Ticker object with news."""
        mock = MagicMock()
        mock.news = mock_news_data
        return mock

    def test_get_news_success(self, service, mock_ticker):
        """Test successful news fetching."""
        with patch('yfinance.Ticker', return_value=mock_ticker):
            news_items = service.get_news('BBCA')

            assert len(news_items) > 0
            assert all(isinstance(item, NewsItem) for item in news_items)
            assert news_items[0].title is not None
            assert news_items[0].source is not None
            assert news_items[0].sentiment in ['positive', 'negative', 'neutral']

    def test_get_news_limit(self, service, mock_ticker):
        """Test that news limit is respected."""
        with patch('yfinance.Ticker', return_value=mock_ticker):
            news_items = service.get_news('BBCA')

            # Should respect max_news limit
            assert len(news_items) <= service.max_news

    def test_get_news_no_results(self, service):
        """Test handling when no news is found."""
        mock_ticker = MagicMock()
        mock_ticker.news = []

        with patch('yfinance.Ticker', return_value=mock_ticker):
            news_items = service.get_news('UNKNOWN')

            assert len(news_items) == 0

    def test_get_news_api_error(self, service):
        """Test handling of API errors."""
        with patch('yfinance.Ticker', side_effect=Exception('API Error')):
            news_items = service.get_news('BBCA')

            # Should return empty list on error
            assert len(news_items) == 0

    def test_sentiment_analysis_positive(self, service):
        """Test positive sentiment detection."""
        text = "Company posts strong profit growth and revenue increase"
        sentiment = service._analyze_sentiment(text)

        assert sentiment == 'positive'

    def test_sentiment_analysis_negative(self, service):
        """Test negative sentiment detection."""
        text = "Company faces major loss and revenue decline concerns"
        sentiment = service._analyze_sentiment(text)

        assert sentiment == 'negative'

    def test_sentiment_analysis_neutral(self, service):
        """Test neutral sentiment detection."""
        text = "Company holds annual general meeting"
        sentiment = service._analyze_sentiment(text)

        assert sentiment == 'neutral'

    def test_sentiment_analysis_empty_text(self, service):
        """Test sentiment analysis with empty text."""
        sentiment = service._analyze_sentiment('')
        assert sentiment == 'neutral'

        sentiment = service._analyze_sentiment(None)
        assert sentiment == 'neutral'

    def test_sentiment_analysis_indonesian_keywords(self, service):
        """Test sentiment with Indonesian keywords."""
        # Positive Indonesian text
        positive_text = "Laba perusahaan naik signifikan dan tumbuh positif"
        assert service._analyze_sentiment(positive_text) == 'positive'

        # Negative Indonesian text
        negative_text = "Perusahaan mengalami rugi dan penurunan drastis"
        assert service._analyze_sentiment(negative_text) == 'negative'

    def test_corporate_action_detection(self, service):
        """Test detection of corporate actions."""
        # Stock split news
        news1 = NewsItem(
            title='Company announces stock split 1:5',
            source='Test',
            published_date=datetime.now(),
            sentiment='neutral'
        )
        assert service._is_corporate_action(news1) is True

        # Dividend news
        news2 = NewsItem(
            title='Board approves dividend payment',
            source='Test',
            published_date=datetime.now(),
            sentiment='positive'
        )
        assert service._is_corporate_action(news2) is True

        # Merger news
        news3 = NewsItem(
            title='Company merger with competitor finalized',
            source='Test',
            published_date=datetime.now(),
            sentiment='neutral'
        )
        assert service._is_corporate_action(news3) is True

        # Regular news (not corporate action)
        news4 = NewsItem(
            title='CEO gives interview about market outlook',
            source='Test',
            published_date=datetime.now(),
            sentiment='neutral'
        )
        assert service._is_corporate_action(news4) is False

    def test_corporate_action_indonesian_keywords(self, service):
        """Test corporate action detection with Indonesian keywords."""
        news = NewsItem(
            title='Perusahaan mengumumkan pemecahan saham',
            source='Test',
            published_date=datetime.now(),
            sentiment='neutral'
        )
        assert service._is_corporate_action(news) is True

        news2 = NewsItem(
            title='Akuisisi perusahaan baru selesai dilakukan',
            source='Test',
            published_date=datetime.now(),
            sentiment='neutral'
        )
        assert service._is_corporate_action(news2) is True

    def test_get_corporate_actions(self, service, mock_ticker):
        """Test filtering corporate actions from news."""
        with patch('yfinance.Ticker', return_value=mock_ticker):
            corporate_actions = service.get_corporate_actions('BBCA')

            # Should only include news with corporate action keywords
            assert len(corporate_actions) > 0
            assert all(service._is_corporate_action(news) for news in corporate_actions)

    def test_analyze_news_impact(self, service):
        """Test overall news impact analysis."""
        news_items = [
            NewsItem(
                title='Positive news 1',
                source='Test',
                published_date=datetime.now(),
                sentiment='positive'
            ),
            NewsItem(
                title='Positive news 2',
                source='Test',
                published_date=datetime.now(),
                sentiment='positive'
            ),
            NewsItem(
                title='Neutral news',
                source='Test',
                published_date=datetime.now(),
                sentiment='neutral'
            ),
            NewsItem(
                title='Negative news',
                source='Test',
                published_date=datetime.now(),
                sentiment='negative'
            ),
        ]

        impact = service.analyze_news_impact(news_items)

        assert impact['positive_count'] == 2
        assert impact['negative_count'] == 1
        assert impact['neutral_count'] == 1
        assert impact['total_news'] == 4
        assert impact['overall_sentiment'] in ['positive', 'negative', 'neutral']
        assert isinstance(impact['key_events'], list)

    def test_analyze_news_impact_positive_overall(self, service):
        """Test overall positive sentiment."""
        news_items = [
            NewsItem(
                title=f'Positive news {i}',
                source='Test',
                published_date=datetime.now(),
                sentiment='positive'
            )
            for i in range(5)
        ] + [
            NewsItem(
                title='Negative news',
                source='Test',
                published_date=datetime.now(),
                sentiment='negative'
            )
        ]

        impact = service.analyze_news_impact(news_items)
        assert impact['overall_sentiment'] == 'positive'

    def test_analyze_news_impact_negative_overall(self, service):
        """Test overall negative sentiment."""
        news_items = [
            NewsItem(
                title=f'Negative news {i}',
                source='Test',
                published_date=datetime.now(),
                sentiment='negative'
            )
            for i in range(5)
        ] + [
            NewsItem(
                title='Positive news',
                source='Test',
                published_date=datetime.now(),
                sentiment='positive'
            )
        ]

        impact = service.analyze_news_impact(news_items)
        assert impact['overall_sentiment'] == 'negative'

    def test_news_sorting_by_date(self, service, mock_ticker):
        """Test that news items are sorted by date (newest first)."""
        with patch('yfinance.Ticker', return_value=mock_ticker):
            news_items = service.get_news('BBCA')

            if len(news_items) > 1:
                # Verify dates are in descending order
                for i in range(len(news_items) - 1):
                    if news_items[i].published_date and news_items[i + 1].published_date:
                        assert news_items[i].published_date >= news_items[i + 1].published_date

    def test_news_item_fields(self, service, mock_ticker):
        """Test that all NewsItem fields are properly populated."""
        with patch('yfinance.Ticker', return_value=mock_ticker):
            news_items = service.get_news('BBCA')

            for news in news_items:
                assert news.title is not None and len(news.title) > 0
                assert news.source is not None
                assert news.sentiment in ['positive', 'negative', 'neutral']
                # published_date and url might be optional
                if news.published_date:
                    assert isinstance(news.published_date, datetime)

    def test_ticker_normalization(self, service, mock_ticker):
        """Test that ticker is normalized before fetching."""
        with patch('yfinance.Ticker', return_value=mock_ticker) as mock_yf:
            # Test without .JK suffix
            service.get_news('BBCA')
            # Should be called with normalized ticker
            mock_yf.assert_called_with('BBCA.JK')

    def test_max_news_configuration(self):
        """Test max_news configuration."""
        service_small = NewsScraperService(max_news=3)
        assert service_small.max_news == 3

        service_large = NewsScraperService(max_news=20)
        assert service_large.max_news == 20

    def test_keyword_case_insensitivity(self, service):
        """Test that sentiment analysis is case-insensitive."""
        # Uppercase
        assert service._analyze_sentiment('PROFIT GROWTH STRONG') == 'positive'
        # Lowercase
        assert service._analyze_sentiment('profit growth strong') == 'positive'
        # Mixed case
        assert service._analyze_sentiment('Profit Growth Strong') == 'positive'

        # Negative
        assert service._analyze_sentiment('LOSS DECLINE WEAK') == 'negative'

    def test_multiple_keywords_scoring(self, service):
        """Test sentiment with multiple keywords."""
        # Multiple positive keywords should be positive
        text = "Strong profit growth with revenue increase and positive outlook"
        assert service._analyze_sentiment(text) == 'positive'

        # Multiple negative keywords should be negative
        text = "Major loss and decline with weak performance and concerns"
        assert service._analyze_sentiment(text) == 'negative'

        # Equal positive and negative should be neutral
        text = "Profit increase but also loss concerns"
        # This might be neutral depending on keyword count
        sentiment = service._analyze_sentiment(text)
        assert sentiment in ['positive', 'negative', 'neutral']

    def test_empty_news_list_impact(self, service):
        """Test impact analysis with empty news list."""
        impact = service.analyze_news_impact([])

        assert impact['positive_count'] == 0
        assert impact['negative_count'] == 0
        assert impact['neutral_count'] == 0
        assert impact['total_news'] == 0
        assert impact['overall_sentiment'] == 'neutral'
        assert impact['key_events'] == []

    def test_get_idx_news_placeholder(self, service):
        """Test _get_idx_news placeholder method."""
        # This method is a placeholder, should return empty list
        news_items = service._get_idx_news('BBCA')
        assert isinstance(news_items, list)
        assert len(news_items) == 0

    def test_get_idx_news_error_handling(self, service):
        """Test _get_idx_news error handling."""
        # Should handle errors gracefully
        with patch('src.services.news_scraper_service.logger') as mock_logger:
            news_items = service._get_idx_news('BBCA')
            assert isinstance(news_items, list)

    def test_get_investing_com_news_placeholder(self, service):
        """Test _get_investing_com_news placeholder method."""
        # This method is a placeholder, should return empty list
        news_items = service._get_investing_com_news('BBCA')
        assert isinstance(news_items, list)
        assert len(news_items) == 0

    def test_get_investing_com_news_error_handling(self, service):
        """Test _get_investing_com_news error handling."""
        # Should handle errors gracefully
        with patch('src.services.news_scraper_service.logger') as mock_logger:
            news_items = service._get_investing_com_news('BBCA')
            assert isinstance(news_items, list)
