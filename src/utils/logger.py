import logging
import sys
import warnings


def get_logger(name: str, level: int = logging.WARNING) -> logging.Logger:
    """
    Get configured logger untuk aplikasi.

    Args:
        name: Logger name
        level: Logging level (default: WARNING, hanya tampilkan warning dan error)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    return logger


def suppress_warnings():
    """Suppress deprecation warnings dari libraries eksternal."""
    # Suppress yfinance deprecation warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    warnings.filterwarnings('ignore', message='.*Ticker.earnings.*')


# Auto-suppress warnings saat module di-import
suppress_warnings()