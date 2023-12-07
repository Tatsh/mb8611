# pylint: disable=invalid-name
from typing import Literal, NotRequired, TypedDict

__all__ = ('GetNetworkModeSettingsPayload', 'GetNetworkModeSettingsResponse',
           'SetMotoLagStatusPayload', 'SetMotoStatusDSTargetFreqPayload',
           'SetStatusSecuritySettingsPayload')


class _SetMotoStatusDSTargetFreq(TypedDict):
    MotoStatusConnectionAction: str
    MotoCmRescanTargetFreq: str
    MotoStatusXXX: Literal['XXX']


class _SetMotoLagStatus(TypedDict):
    SetMotoLagStatus: str


class SetMotoLagStatusPayload(TypedDict):
    """Not used in cable-modem only models."""
    SetMotoLagStatus: _SetMotoLagStatus


class SetMotoStatusDSTargetFreqPayload(TypedDict):
    """Not used in cable-modem only models."""
    SetMotoStatusDSTargetFreq: _SetMotoStatusDSTargetFreq


class _GetNetworkModeSettingsResponse(TypedDict):
    global_network_mode: Literal['router', 'bridge']
    GetNetworkModeSettingsResult: str


class GetNetworkModeSettingsResponse(TypedDict):
    """Not used in cable-modem only models."""
    GetNetworkModeSettingsResponse: _GetNetworkModeSettingsResponse


class GetNetworkModeSettingsPayload(TypedDict):
    GetNetworkModeSettings: Literal['']


class _SetStatusSecuritySettings(TypedDict):
    # Username and passwords here must be AES-128 encrypted. The key is the PrivateKey assigned at
    # login.
    MotoUsername: str
    MotoPassword: str
    MotoNewUsername: str
    MotoNewPassword: str
    MotoRepPassword: str
    MotoStatusSecXXX: NotRequired[Literal['XXX']]


class SetStatusSecuritySettingsPayload(TypedDict):
    SetStatusSecuritySettings: _SetStatusSecuritySettings


class _RebootSetStatusSecuritySettings(TypedDict):
    MotoStatusSecXXX: Literal['XXX']


class RebootPayload(TypedDict):
    SetStatusSecuritySettings: _RebootSetStatusSecuritySettings


class _SetStatusLogSettings(TypedDict):
    MotoStatusLogAction: Literal['1']
    MotoStatusLogXXX: Literal['XXX']


class ClearLogPayload(TypedDict):
    SetStatusLogSettings: _SetStatusLogSettings


class _SetStatusLogSettingsResponse(TypedDict):
    SetStatusLogSettingsResult: Literal['OK', 'UN-AUTH']


class SetStatusLogSettingsResponse(TypedDict):
    SetStatusLogSettingsResponse: _SetStatusLogSettingsResponse
