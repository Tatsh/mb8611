"""Utility functions."""
from collections.abc import Iterator, Sequence
import hmac
import math
import time

__all__ = ('make_hnap_auth', 'make_soap_action_uri', 'parse_table_str')


def make_soap_action_uri(action: str) -> str:
    """Return the SOAP action URI for the given action."""
    return f'"http://purenetworks.com/HNAP1/{action}"'


def make_hnap_auth(action: str, private_key: str = 'withoutloginkey') -> str:
    """Create the value required for the ``HNAP_AUTH`` header."""
    current_time = str(math.floor(time.time_ns() / 1000000) % 2000000000000)
    auth = hmac.new(private_key.encode(), (current_time + make_soap_action_uri(action)).encode(),
                    'md5')
    return f'{auth.hexdigest().upper()} {current_time}'


def parse_table_str(table_str: str, row_delimiter: str = '|+|') -> Iterator[Sequence[str]]:
    """Parse a string that represents a table displayed in the UI."""
    yield from (r.split('^') for r in table_str.split(row_delimiter))
