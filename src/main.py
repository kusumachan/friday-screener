"""
Friday Screener - Stock Screening Tool for Indonesian Market.

Main entry point untuk CLI application.
"""

import warnings

# Suppress all warnings untuk clean output
warnings.filterwarnings('ignore')

from src.cli.commands import cli

if __name__ == '__main__':
    cli()
