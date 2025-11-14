"""
Data models untuk informasi saham dan data fundamental.

Model ini merepresentasikan data saham yang diambil dari berbagai sumber
(Yahoo Finance, web scraping, dll).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class CompanyInfo:
    """Informasi dasar perusahaan."""

    ticker: str
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None


@dataclass
class ValuationMetrics:
    """Metrik valuasi perusahaan."""

    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    pe_ratio: Optional[float] = None  # Trailing PE
    forward_pe: Optional[float] = None
    peg_ratio: Optional[float] = None
    price_to_book: Optional[float] = None  # PBV
    price_to_sales: Optional[float] = None
    shares_outstanding: Optional[float] = None


@dataclass
class ProfitabilityMetrics:
    """Metrik profitabilitas dan pertumbuhan."""

    # Current metrics
    revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_income: Optional[float] = None
    net_income: Optional[float] = None
    eps: Optional[float] = None  # Earnings Per Share

    # Margins (dalam desimal, e.g., 0.25 = 25%)
    gross_margin: Optional[float] = None  # GPM
    operating_margin: Optional[float] = None
    profit_margin: Optional[float] = None

    # Returns
    roe: Optional[float] = None  # Return on Equity
    roa: Optional[float] = None  # Return on Assets
    roic: Optional[float] = None  # Return on Invested Capital

    # Historical EPS (5 tahun terakhir)
    eps_history: Dict[int, float] = field(default_factory=dict)  # {year: eps}


@dataclass
class CashFlowMetrics:
    """Metrik cash flow."""

    operating_cash_flow: Optional[float] = None
    free_cash_flow: Optional[float] = None
    capital_expenditure: Optional[float] = None
    levered_free_cash_flow: Optional[float] = None


@dataclass
class LeverageMetrics:
    """Metrik leverage dan risiko."""

    total_debt: Optional[float] = None
    total_equity: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    interest_coverage: Optional[float] = None
    beta: Optional[float] = None  # Volatilitas relatif terhadap market


@dataclass
class DividendMetrics:
    """Metrik dividen."""

    dividend_rate: Optional[float] = None  # Annual dividend per share
    dividend_yield: Optional[float] = None  # Dividend yield (%)
    payout_ratio: Optional[float] = None  # Payout ratio
    five_year_avg_dividend_yield: Optional[float] = None
    dividend_history: List[Dict] = field(default_factory=list)  # Historical dividends


@dataclass
class PriceMetrics:
    """Metrik harga saham."""

    current_price: Optional[float] = None
    previous_close: Optional[float] = None
    open_price: Optional[float] = None
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    volume: Optional[int] = None
    avg_volume: Optional[int] = None


@dataclass
class NewsItem:
    """Item berita atau corporate action."""

    title: str
    source: str
    published_date: Optional[datetime] = None
    url: Optional[str] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = None  # positive, negative, neutral


@dataclass
class StockData:
    """
    Complete stock data model yang menggabungkan semua informasi.

    Model ini adalah representasi lengkap dari sebuah emiten saham
    termasuk data fundamental, teknikal, dan berita.
    """

    # Basic info
    company_info: CompanyInfo

    # Financial metrics
    valuation: ValuationMetrics = field(default_factory=ValuationMetrics)
    profitability: ProfitabilityMetrics = field(default_factory=ProfitabilityMetrics)
    cash_flow: CashFlowMetrics = field(default_factory=CashFlowMetrics)
    leverage: LeverageMetrics = field(default_factory=LeverageMetrics)
    dividend: DividendMetrics = field(default_factory=DividendMetrics)
    price: PriceMetrics = field(default_factory=PriceMetrics)

    # Additional info
    news: List[NewsItem] = field(default_factory=list)
    corporate_actions: List[NewsItem] = field(default_factory=list)

    # Metadata
    last_updated: datetime = field(default_factory=datetime.now)
    data_quality_score: Optional[float] = None  # 0-100, kualitas data yang tersedia

    def get_ticker(self) -> str:
        """Get stock ticker symbol."""
        return self.company_info.ticker

    def has_complete_data(self) -> bool:
        """Check if stock has complete fundamental data for screening."""
        required_metrics = [
            self.valuation.pe_ratio,
            self.valuation.price_to_book,
            self.profitability.roe,
            self.profitability.gross_margin,
            self.leverage.debt_to_equity,
        ]
        return all(metric is not None for metric in required_metrics)
