# pylint: disable=invalid-name
from typing import Literal, TypedDict

from typing_extensions import NotRequired


class _SetMotoStatusDSTargetFreq(TypedDict):
    MotoStatusConnectionAction: str
    MotoCmRescanTargetFreq: str
    MotoStatusXXX: Literal['XXX']


class _SetMotoLagStatus(TypedDict):
    SetMotoLagStatus: str


class SetMotoLagStatusPayload(TypedDict):
    SetMotoLagStatus: _SetMotoLagStatus


class SetMotoStatusDSTargetFreqPayload(TypedDict):
    SetMotoStatusDSTargetFreq: _SetMotoStatusDSTargetFreq


class _GetNetworkModeSettingsResponse(TypedDict):
    """Not used in cable-modem only models."""
    global_network_mode: Literal['router', 'bridge']
    GetNetworkModeSettingsResult: str


class GetNetworkModeSettingsResponse(TypedDict):
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
