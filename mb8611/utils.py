"""Utility functions."""
from types import FrameType
import logging
import sys

from loguru import logger

__all__ = ('setup_logging',)

class InterceptHandler(logging.Handler):  # pragma: no cover
    """Intercept handler taken from Loguru's documentation."""
    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        # Find caller from where originated the logged message
        frame: FrameType | None = logging.currentframe()
        depth = 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_log_intercept_handler() -> None:  # pragma: no cover
    """Sets up Loguru to intercept records from the logging module."""
    logging.basicConfig(handlers=(InterceptHandler(),), level=0)


def setup_logging(debug: bool | None = False) -> None:
    """Shared function to enable logging."""
    if debug:  # pragma: no cover
        setup_log_intercept_handler()
        logger.enable('')
    else:
        logger.configure(handlers=(dict(
            format='<level>{message}</level>',
            level='INFO',
            sink=sys.stderr,
        ),))
