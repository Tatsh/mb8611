"""Common constants."""
from typing import Final, Mapping

__all__ = ('SHARED_HEADERS',)

#: Common HTTP headers
SHARED_HEADERS: Final[Mapping[str, str]] = {
    'accept': 'application/json',
    'cache-control': 'no-cache',
    'connection': 'keep-alive',
    'content-type': 'application/json',
    'x-requested-with': 'XMLHttpRequest'
}
#: Keys that contain specially encoded lists to be displayed in tables.
TABLE_KEYS = ('MotoConnDownstreamChannel', 'MotoConnUpstreamChannel', 'MotoStatusLogList')
#: Actions that do not work without using GetMultipleHNAPs.
MUST_BE_CALLED_FROM_MULTIPLE: Final[set[str]] = set(
    ('GetHomeAddress', 'GetHomeConnection', 'GetMotoLagStatus', 'GetMotoStatusConnectionInfo',
     'GetMotoStatusDownstreamChannelInfo', 'GetMotoStatusLog', 'GetMotoStatusLogXXX',
     'GetMotoStatusSecAccount', 'GetMotoStatusSecXXX', 'GetMotoStatusSoftware',
     'GetMotoStatusStartupSequence', 'GetMotoStatusUpstreamChannelInfo'))
#: Delimiters used in encoded table strings, keyed by action.
ROW_DELIMITERS = dict(MotoStatusLogList='}-{')
