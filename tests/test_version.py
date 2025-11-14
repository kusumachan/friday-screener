"""
Unit tests untuk version module.
"""

import pytest

from src.__version__ import __version__, __author__, __description__


class TestVersion:
    """Tests untuk version information."""

    def test_version_exists(self):
        """Test bahwa __version__ ada dan valid."""
        assert __version__ is not None
        assert isinstance(__version__, str)
        # Should be in format X.Y.Z
        assert len(__version__.split('.')) == 3

    def test_author_exists(self):
        """Test bahwa __author__ ada."""
        assert __author__ is not None
        assert isinstance(__author__, str)

    def test_description_exists(self):
        """Test bahwa __description__ ada."""
        assert __description__ is not None
        assert isinstance(__description__, str)

