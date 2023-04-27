from typing import Final, Mapping

__all__ = ('SHARED_HEADERS',)

SHARED_HEADERS: Final[Mapping[str, str]] = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'cache-control': 'no-cache',
    'connection': 'keep-alive',
    'x-requested-with': 'XMLHttpRequest'
}
