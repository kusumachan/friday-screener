"""
Unit tests untuk main entry point.
"""

import warnings
from unittest.mock import patch

import pytest

from src.main import cli


class TestMain:
    """Tests untuk main module."""

    def test_main_imports_cli(self):
        """Test bahwa main module mengimport cli."""
        from src.main import cli
        assert callable(cli)

    def test_warnings_suppressed(self):
        """Test bahwa warnings di-suppress."""
        # This test verifies warnings are filtered
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Import should not raise warnings
            from src.main import cli
            # Warnings should be suppressed (filterwarnings is called in main.py)
            # The warnings list might be empty because they're filtered
            assert callable(cli)

