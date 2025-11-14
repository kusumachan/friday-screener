# Friday Screener

[![CI](https://github.com/kusumachan/friday-screener/actions/workflows/ci.yml/badge.svg)](https://github.com/kusumachan/friday-screener/actions/workflows/ci.yml)
[![Release](https://github.com/kusumachan/friday-screener/actions/workflows/release.yml/badge.svg)](https://github.com/kusumachan/friday-screener/actions/workflows/release.yml)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Professional-grade stock screening tool untuk analisis fundamental emiten saham di Bursa Efek Indonesia (BEI).**

Friday Screener adalah aplikasi CLI yang dirancang khusus untuk investor dan analis yang ingin melakukan screening saham berdasarkan kriteria fundamental yang ketat. Tool ini mengintegrasikan data dari Yahoo Finance, analisis berita, dan kriteria screening yang komprehensif untuk memberikan rekomendasi investasi yang data-driven.

## Features

### 🎯 Comprehensive Fundamental Analysis
- **Valuasi**: PE Ratio, PBV, Market Cap
- **Profitabilitas**: ROE, Gross Margin, EPS Growth
- **Risk Management**: Debt-to-Equity, Beta, Leverage Metrics
- **Dividend Analysis**: Dividend Yield, Payout Ratio
- **Cash Flow**: Operating Cash Flow, Free Cash Flow

### 📰 News & Corporate Actions
- Scraping berita terkini dari Yahoo Finance
- Identifikasi corporate actions (stock split, dividend, merger, dll)
- Sentiment analysis untuk berita (positive/negative/neutral)
- Analisis dampak berita terhadap performa saham

### 📊 Intelligent Scoring System
- Weighted scoring berdasarkan kategori (Valuation 25%, Profitability 35%, Risk 20%, Dividend 20%)
- Rating system: Strong Buy, Buy, Hold, Sell, Strong Sell
- Detailed insights untuk setiap kategori
- Red flags dan strengths identification

### 💻 User-Friendly CLI
- Interactive command-line interface dengan Rich formatting
- Support untuk single stock screening dan multiple stock comparison
- Detailed dan summary views
- Color-coded output untuk quick insights

## Installation

### Option 1: Download Pre-built Binary (Recommended)

Cara termudah - download executable yang sudah di-build:

1. **Go to [Releases](../../releases)**
2. **Download file untuk OS Anda:**
   - Windows: `friday-screener-windows-amd64.exe`
   - Linux: `friday-screener-linux-amd64`
   - macOS: `friday-screener-macos-amd64`

3. **Make executable (Linux/macOS only):**
```bash
chmod +x friday-screener-*
```

4. **Run:**
```bash
# Linux/macOS
./friday-screener

# Windows
friday-screener.exe
```

### Option 2: Install from Source

Untuk development atau customization:

#### Prerequisites
- Python 3.11 atau lebih tinggi
- Virtual environment (recommended)

#### Setup

1. **Clone repository**
```bash
git clone <repository-url>
cd friday-screener
```

2. **Create dan activate virtual environment**
```bash
make venv
source venv/bin/activate  # On Unix/macOS
# atau
venv\Scripts\activate  # On Windows
```

3. **Install dependencies**
```bash
make install
```

### Option 3: Build Your Own Executable

Untuk build sendiri, lihat [BUILD.md](BUILD.md) untuk instruksi lengkap.

## Usage

### Interactive Mode (Recommended)

Cara termudah untuk memulai - interactive mode akan memandu Anda step-by-step:

```bash
# Jalankan salah satu:
make run
# atau
python -m src.main
# atau
python -m src.main interactive
```

Interactive mode akan menampilkan menu:
1. **Screen single stock** - Analisis satu emiten
2. **Compare multiple stocks** - Bandingkan beberapa emiten
3. **Quit** - Keluar

Anda akan dipandu untuk:
- Input ticker saham (contoh: BBCA, TLKM)
- Pilih opsi detailed analysis
- Pilih include/exclude news
- Continue untuk screening lagi atau quit

### Command Line Mode

Untuk pengguna advanced atau automation, gunakan command line directly:

#### Single Stock Screening

Screen satu emiten dengan analisis lengkap:

```bash
python -m src.main screen BBCA
```

Dengan detailed insights:

```bash
python -m src.main screen BBCA --detailed
```

Tanpa news analysis (lebih cepat):

```bash
python -m src.main screen BBCA --no-news
```

#### Multiple Stock Comparison

Compare beberapa emiten side-by-side:

```bash
python -m src.main compare BBCA BMRI BBNI
```

### Available Commands

```bash
# Help
python -m src.main --help

# Interactive mode (default)
python -m src.main
python -m src.main interactive

# Screen single stock
python -m src.main screen <TICKER> [OPTIONS]

# Compare multiple stocks
python -m src.main compare <TICKER1> <TICKER2> [TICKER3] ...
```

## Screening Criteria

### 1. Valuation (25% weight)
- **PE Ratio**: Prefer ≤ 5, acceptable < 15
- **PBV**: Prefer ≤ 1, acceptable < 2
- **Market Cap**: Prefer ≥ 100T (blue chip)

### 2. Profitability (35% weight)
- **EPS Growth**: Harus positif dalam 5 tahun terakhir
- **Gross Margin**: Prefer ≥ 30%, minimum 20%
- **ROE**: Prefer ≥ 15%, minimum 10%
- **Cash Flow**: Operating CF dan Free CF harus positif

### 3. Risk (20% weight)
- **Debt-to-Equity**: Prefer < 0.5, maximum < 1.0
- **Beta**: Maximum 1.5 (volatilitas)

### 4. Dividend (20% weight)
- **Dividend Yield**: Prefer ≥ 4%, minimum 2%
- **Requirement**: Minimal ada dividen

### Rating System

**IMPORTANT**: Rating adalah kategori fundamental, **BUKAN** rekomendasi investasi.

| Score Range | Rating | Meaning |
|------------|--------|---------|
| 80-100 | Very Strong ⭐⭐⭐ | Fundamental sangat kuat |
| 60-79 | Strong ⭐⭐ | Fundamental kuat |
| 40-59 | Fair ⭐ | Fundamental cukup |
| 20-39 | Weak ⚠️ | Fundamental lemah |
| 0-19 | Very Weak ⚠️⚠️ | Fundamental sangat lemah |

## Project Structure

```
friday-screener/
├── .github/
│   └── workflows/          # GitHub Actions
│       ├── ci.yml          # Continuous Integration
│       └── release.yml     # Automated Releases
├── src/
│   ├── __version__.py      # Version info
│   ├── analyzers/          # Fundamental analysis logic
│   │   └── fundamental_analyzer.py
│   ├── cli/                # CLI commands
│   │   └── commands.py
│   ├── config/             # Configuration & criteria
│   │   └── settings.py
│   ├── models/             # Data models
│   │   ├── stock_data.py
│   │   └── screening_result.py
│   ├── services/           # External services
│   │   ├── yahoo_finance_service.py
│   │   └── news_scraper_service.py
│   ├── utils/              # Utilities
│   │   ├── logger.py
│   │   └── helpers.py
│   └── main.py             # Entry point
├── tests/                  # Unit tests
│   ├── test_helpers.py
│   └── test_fundamental_analyzer.py
├── friday-screener.spec    # PyInstaller spec file
├── requirements.txt        # Dependencies
├── pyproject.toml         # Project config
├── pytest.ini             # Test config
├── makefile               # Build & dev automation
├── BUILD.md               # Build instructions
├── CHANGELOG.md           # Version history
├── RELEASE.md             # Release process
└── README.md              # This file
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_helpers.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Format and lint
make format && make lint
```

### Makefile Commands

```bash
# Development
make venv          # Create virtual environment
make install       # Install dependencies
make run           # Run the application
make test          # Run tests with pytest
make test-cov      # Run tests with coverage
make format        # Format code with Black & Ruff
make lint          # Lint code with Ruff

# Build
make build         # Build single executable
make build/exe     # Build single executable (explicit)
make build/dist    # Build with dependencies folder

# Clean
make clean/all     # Remove venv and all caches
make clean/cache   # Remove Python caches only
make clean/build   # Remove build artifacts
```

## Building Executables

### Quick Build

```bash
# Install PyInstaller (if not installed)
make install

# Build single executable
make build

# Output: dist/friday-screener atau dist/friday-screener.exe
```

### Platform-Specific Builds

**Windows:**
```powershell
python -m PyInstaller friday-screener.spec --clean --noconfirm
# Output: dist\friday-screener.exe
```

**Linux/macOS:**
```bash
python -m PyInstaller friday-screener.spec --clean --noconfirm
chmod +x dist/friday-screener
# Output: dist/friday-screener
```

**For complete build instructions**, see [BUILD.md](BUILD.md)

## Releases

### Download Pre-built Binaries

1. Go to [Releases](../../releases)
2. Download untuk OS Anda (Windows/Linux/macOS)
3. Run executable

### Create Release (Maintainers)

```bash
# 1. Update version in src/__version__.py
# 2. Update CHANGELOG.md
# 3. Commit and tag
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0

# GitHub Actions will automatically:
# - Run tests
# - Build for all platforms
# - Create GitHub Release
# - Upload binaries
```

**For complete release process**, see [RELEASE.md](RELEASE.md)

## Examples

### Example 1: Screening Bank BCA (BBCA)

```bash
$ python -m src.main screen BBCA --detailed

Screening BBCA...

╭──────────────── Company Information ────────────────╮
│ Ticker    BBCA                                       │
│ Company   Bank Central Asia Tbk                     │
│ Sector    Financial Services                        │
│ Industry  Banking                                   │
╰──────────────────────────────────────────────────────╯

╭──────────────── Screening Result ───────────────────╮
│ Fundamental Rating: Very Strong ⭐⭐⭐               │
│ Total Score: 82.5/100                               │
│ Data Quality: 95%                                   │
╰──────────────────────────────────────────────────────╯

Category Scores:
┏━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Category     ┃  Score ┃ Status ┃ Weight ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ Valuation    │   85.0 │ ✓ Pass │    25% │
│ Profitability│   88.0 │ ✓ Pass │    35% │
│ Risk         │   75.0 │ ✓ Pass │    20% │
│ Dividend     │   80.0 │ ✓ Pass │    20% │
└──────────────┴────────┴────────┴────────┘

╭───────────────── Screening Summary ──────────────────╮
│ FUNDAMENTAL RATING: Very Strong ⭐⭐⭐                │
│                                                      │
│ Berdasarkan analisis fundamental, saham ini          │
│ menunjukkan kualitas yang baik.                      │
│ Total Score: 82.5/100                                │
│                                                      │
│ Disclaimer: Ini bukan rekomendasi investasi.         │
│ Lakukan riset sendiri dan konsultasi dengan          │
│ financial advisor.                                   │
╰──────────────────────────────────────────────────────╯
```

### Example 2: Comparing Banks

```bash
$ python -m src.main compare BBCA BMRI BBNI

Comparing 3 stocks...

Stock Comparison:
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━━┳━━━━━━┓
┃ Ticker ┃ Company            ┃ Rating    ┃ Score ┃   PE ┃  PBV ┃   ROE ┃  D/E ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━━╇━━━━━━┩
│ BBCA   │ Bank Central Asia  │ Very      │  82.5 │ 10.5 │ 1.2x │ 20.0% │ 0.3x │
│        │                    │ Strong    │       │      │      │       │      │
│ BMRI   │ Bank Mandiri       │ Strong    │  75.2 │ 12.0 │ 1.5x │ 18.5% │ 0.4x │
│ BBNI   │ Bank Negara Indo.. │ Strong    │  71.8 │ 11.5 │ 1.8x │ 16.0% │ 0.5x │
└────────┴────────────────────┴───────────┴───────┴──────┴──────┴───────┴──────┘
```

## Customization

Anda bisa customize screening criteria dengan memodifikasi `src/config/settings.py`:

```python
from src.config.settings import ScreeningCriteria

# Create custom criteria
criteria = ScreeningCriteria()
criteria.valuation.pe_ratio_max = 10.0  # More strict
criteria.profitability.roe_min = 15.0   # Higher ROE requirement

# Use with analyzer
analyzer = FundamentalAnalyzer(criteria=criteria)
```

## Limitations

1. **Data Source**: Bergantung pada Yahoo Finance API yang mungkin tidak selalu akurat atau lengkap untuk saham Indonesia
2. **News Scraping**: Berita terbatas pada sumber Yahoo Finance
3. **Real-time Data**: Data mungkin delayed, bukan real-time
4. **Sentiment Analysis**: Sentiment analysis menggunakan keyword-based approach, bukan ML-based
5. **Historical Data**: EPS historical data kadang tidak lengkap untuk semua emiten

## Future Enhancements

- [ ] Integrasi dengan IDX website untuk data yang lebih akurat
- [ ] Machine learning untuk sentiment analysis
- [ ] Technical analysis indicators
- [ ] Portfolio management features
- [ ] Export results ke PDF/Excel
- [ ] Web dashboard interface
- [ ] Real-time price alerts
- [ ] Backtesting capabilities

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

**IMPORTANT**: This tool is for educational and research purposes only. It should not be considered as financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions. The developers are not responsible for any financial losses incurred from using this tool.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for Indonesian investors**
