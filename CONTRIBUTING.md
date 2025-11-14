# Contributing to Friday Screener

Thank you for considering contributing to Friday Screener! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and encourage diverse perspectives
- Focus on constructive criticism
- Respect differing viewpoints and experiences

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Screenshots** if applicable

Example:
```
Title: PE Ratio calculation incorrect for negative earnings

Description: When a company has negative earnings, the PE Ratio shows
incorrect value instead of N/A.

Steps to reproduce:
1. Run `python -m src.main screen XXXX`
2. Check PE Ratio in output

Expected: PE Ratio should show N/A
Actual: PE Ratio shows -15.2

Environment:
- OS: macOS 14.0
- Python: 3.11.5
- Friday Screener: v1.0.0
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When suggesting:

- **Use clear and descriptive title**
- **Provide detailed description**
- **Explain why enhancement would be useful**
- **Provide examples** if possible

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   make test
   make lint
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

   Commit message format:
   - feat: New feature
   - fix: Bug fix
   - docs: Documentation changes
   - test: Test additions/changes
   - refactor: Code refactoring
   - chore: Maintenance tasks

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Provide clear description
   - Reference related issues
   - Include screenshots if applicable

## Development Setup

### Prerequisites

- Python 3.11+
- Virtual environment tool
- Git

### Setup

```bash
# Clone your fork
git clone https://github.com/kusumachan/friday-screener.git
cd friday-screener

# Add upstream remote
git remote add upstream https://github.com/original/friday-screener.git

# Create virtual environment and install dependencies
make install

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest tests/test_helpers.py

# Run specific test
pytest tests/test_helpers.py::TestSafeConversions::test_safe_float_with_valid_number
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Both
make format && make lint
```

## Coding Standards

### Python Style

- Follow **PEP 8** style guide
- Use **Black** for formatting (line length: 88)
- Use **Ruff** for linting
- Use **type hints** where applicable

Example:
```python
def calculate_score(value: float, threshold: float) -> float:
    """
    Calculate score based on value and threshold.

    Args:
        value: The value to score
        threshold: The threshold for comparison

    Returns:
        Score between 0 and 100
    """
    if value >= threshold:
        return 100.0
    return (value / threshold) * 100.0
```

### Documentation

- **Docstrings** for all modules, classes, and functions
- Follow **Google style** docstrings
- Include **type hints**
- Update **README.md** for user-facing changes
- Add **inline comments** for complex logic

Example docstring:
```python
def analyze_stock(ticker: str, use_cache: bool = True) -> ScreeningResult:
    """
    Analyze a stock and return screening result.

    This function fetches stock data, performs fundamental analysis,
    and generates a comprehensive screening result with scoring and insights.

    Args:
        ticker: Stock ticker symbol (e.g., 'BBCA', 'TLKM')
        use_cache: Whether to use cached data if available (default: True)

    Returns:
        ScreeningResult object containing analysis results

    Raises:
        ValueError: If ticker is invalid
        APIError: If data fetching fails

    Example:
        >>> result = analyze_stock('BBCA')
        >>> print(result.rating)
        Rating.STRONG_BUY
    """
    # Implementation here
```

### Testing

- Write **unit tests** for new functions
- Maintain or improve **code coverage**
- Use **pytest** for testing
- Use **fixtures** for test data
- Use **mocking** for external dependencies

Example test:
```python
import pytest
from src.utils.helpers import safe_float

class TestSafeFloat:
    """Tests for safe_float function."""

    def test_with_valid_number(self):
        """Test safe_float with valid numbers."""
        assert safe_float(123) == 123.0
        assert safe_float("123.45") == 123.45

    def test_with_invalid_input(self):
        """Test safe_float with invalid input."""
        assert safe_float(None) is None
        assert safe_float("invalid") is None
        assert safe_float("invalid", default=0.0) == 0.0
```

### Project Structure

When adding new features, follow the existing structure:

```
src/
├── analyzers/      # Analysis logic
├── cli/            # CLI commands
├── config/         # Configuration
├── models/         # Data models
├── services/       # External services
└── utils/          # Utilities

tests/              # Mirror src/ structure
```

## Priority Areas for Contribution

### High Priority

1. **Data Sources**
   - Integration with IDX official API
   - Additional news sources
   - Improved data quality checks

2. **Analysis Features**
   - Technical analysis indicators
   - Sector-specific criteria
   - Machine learning for sentiment

3. **Testing**
   - Integration tests
   - End-to-end tests
   - Performance tests

### Medium Priority

1. **User Experience**
   - Interactive prompts
   - Export to PDF/Excel
   - Web dashboard

2. **Documentation**
   - Video tutorials
   - More examples
   - Translations

### Low Priority

1. **Nice to Have**
   - Portfolio tracking
   - Backtesting
   - Real-time alerts

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion
- Reach out to maintainers

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🙏
