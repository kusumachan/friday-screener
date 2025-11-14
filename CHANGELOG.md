# Changelog

All notable changes to Friday Screener will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- PyInstaller build system for creating standalone executables
- GitHub Actions CI/CD pipeline for automated testing and releases
- Cross-platform builds (Windows, Linux, macOS)
- Automated releases on version tags

## [1.0.0] - 2025-11-14

### Added
- Interactive mode untuk user-friendly screening
- Single stock screening dengan analisis fundamental komprehensif
- Multiple stock comparison
- Beautiful colored CLI output dengan Rich library
- News & sentiment analysis
- Corporate actions detection
- Customizable screening criteria
- Unit tests dengan pytest
- Comprehensive documentation

### Features
- **Valuation Analysis**: PE Ratio, PBV, Market Cap
- **Profitability Analysis**: ROE, Gross Margin, EPS Growth, Cash Flow
- **Risk Analysis**: Debt-to-Equity, Beta
- **Dividend Analysis**: Dividend Yield, Payment History
- **News Integration**: Yahoo Finance news dengan sentiment analysis
- **Fundamental Rating**: Very Strong, Strong, Fair, Weak, Very Weak (bukan rekomendasi investasi)

### Rating System
- 80-100: Very Strong ⭐⭐⭐
- 60-79: Strong ⭐⭐
- 40-59: Fair ⭐
- 20-39: Weak ⚠️
- 0-19: Very Weak ⚠️⚠️

### Technical
- Python 3.11+ support
- yfinance for financial data
- Rich for beautiful terminal output
- Click for CLI framework
- BeautifulSoup4 for web scraping
- Comprehensive test coverage (48%+)

### Documentation
- README.md - Full documentation
- QUICKSTART.md - Quick start guide
- ARCHITECTURE.md - Technical architecture
- CONTRIBUTING.md - Contribution guidelines
- FEATURES.md - Feature overview

## Release Notes

### How to Use

**Interactive Mode:**
```bash
./friday-screener
```

**Screen Single Stock:**
```bash
./friday-screener screen BBCA
```

**Compare Stocks:**
```bash
./friday-screener compare BBCA BMRI BBNI
```

**Get Help:**
```bash
./friday-screener --help
```

### Disclaimer

Friday Screener adalah tool untuk edukasi dan research purposes only. Ini bukan financial advice atau rekomendasi investasi. Selalu lakukan riset sendiri dan konsultasi dengan qualified financial advisor sebelum membuat keputusan investasi.

### Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for Indonesian investors**
