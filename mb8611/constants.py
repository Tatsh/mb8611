"""Common constants."""
from collections.abc import Mapping
from typing import Final

from .api import MultipleHNAPAction

__all__ = ('MUST_BE_CALLED_FROM_MULTIPLE', 'ROW_DELIMITERS', 'SHARED_HEADERS', 'TABLE_KEYS')

SHARED_HEADERS: Final[Mapping[str, str]] = {
    'accept': 'application/json',
    'cache-control': 'no-cache',
    'connection': 'keep-alive',
    'content-type': 'application/json',
    'x-requested-with': 'XMLHttpRequest'
}
"""Common HTTP headers."""
TABLE_KEYS = ('MotoConnDownstreamChannel', 'MotoConnUpstreamChannel', 'MotoStatusLogList')
"""Keys that contain specially encoded lists to be displayed in tables."""
MUST_BE_CALLED_FROM_MULTIPLE: Final[set[MultipleHNAPAction]] = {
    'GetHomeAddress', 'GetHomeConnection', 'GetMotoLagStatus', 'GetMotoStatusConnectionInfo',
    'GetMotoStatusDownstreamChannelInfo', 'GetMotoStatusLog', 'GetMotoStatusLogXXX',
    'GetMotoStatusSecAccount', 'GetMotoStatusSecXXX', 'GetMotoStatusSoftware',
    'GetMotoStatusStartupSequence', 'GetMotoStatusUpstreamChannelInfo'
}
"""Actions that do not work without using GetMultipleHNAPs."""
ROW_DELIMITERS: Final[dict[str, str]] = dict(MotoStatusLogList='}-{')
"""Delimiters used in encoded table strings, keyed by action."""
