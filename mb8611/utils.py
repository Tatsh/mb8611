"""Utility functions."""
from datetime import datetime
from types import FrameType
import hmac
import logging
import math
import sys
from typing import Iterator, Sequence

from loguru import logger

__all__ = ('make_hnap_auth', 'make_soap_action_uri', 'parse_table_str', 'setup_logging')


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


def make_soap_action_uri(action: str) -> str:
    return f'"http://purenetworks.com/HNAP1/{action}"'


def make_hnap_auth(action: str, private_key: str = 'withoutloginkey') -> str:
    current_time = str(math.floor(datetime.now().timestamp()) % 2000000000000)
    auth = hmac.new(private_key.encode(), (current_time + make_soap_action_uri((action))).encode(),
                    'md5')
    return f'{auth.hexdigest().upper()} {current_time}'


def parse_table_str(s: str, row_delimiter: str = '|+|') -> Iterator[Sequence[str]]:
    yield from (r.split('^') for r in s.split(row_delimiter))
