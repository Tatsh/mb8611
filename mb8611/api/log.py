# pylint: disable=invalid-name
from typing import Literal, TypedDict


class _SetStatusLogSettings(TypedDict):
    MotoStatusLogAction: Literal['1']
    MotoStatusLogXXX: Literal['XXX']


class ClearLogPayload(TypedDict):
    # SOAPAction = SetStatusLogSettings
    SetStatusLogSettings: _SetStatusLogSettings
