from typing import Literal

from .get_multiple_hnaps import (
    GetHomeAddressResponse,
    GetMultipleHNAPsPayload,
    GetMultipleHNAPsResponse,
)
from .login import LoginPayload, LoginResponse
from .settings import (
    ClearLogPayload,
    GetNetworkModeSettingsPayload,
    GetNetworkModeSettingsResponse,
    RebootPayload,
    SetMotoLagStatusPayload,
    SetMotoLagStatusResponse,
    SetMotoStatusDSTargetFreqPayload,
    SetStatusLogSettingsResponse,
    SetStatusSecuritySettingsPayload,
    SetStatusSecuritySettingsResponse,
)

__all__ = ('Action', 'MultipleHNAPAction', 'Payload', 'Response')

Action = Literal['GetHomeAddress', 'GetHomeConnection', 'GetMotoLagStatus',
                 'GetMotoStatusConnectionInfo', 'GetMotoStatusDownstreamChannelInfo',
                 'GetMotoStatusLog', 'GetMotoStatusLogXXX', 'GetMotoStatusSecAccount',
                 'GetMotoStatusSecXXX', 'GetMotoStatusSoftware', 'GetMotoStatusStartupSequence',
                 'GetMotoStatusUpstreamChannelInfo', 'GetMultipleHNAPs', 'GetNetworkModeSettings',
                 'Login', 'Logout', 'SetMotoLagStatus', 'SetMotoStatusDSTargetFreq',
                 'SetStatusLogSettings', 'SetStatusSecuritySettings']
"""Valid actions."""
MultipleHNAPAction = Literal['GetHomeAddress', 'GetHomeConnection', 'GetMotoLagStatus',
                             'GetMotoStatusConnectionInfo', 'GetMotoStatusDownstreamChannelInfo',
                             'GetMotoStatusLog', 'GetMotoStatusLogXXX', 'GetMotoStatusSecAccount',
                             'GetMotoStatusSecXXX', 'GetMotoStatusSoftware',
                             'GetMotoStatusStartupSequence', 'GetMotoStatusUpstreamChannelInfo']
"""Actions that must be wrapped in multiple HNAP."""
Payload = (ClearLogPayload | GetMultipleHNAPsPayload | GetNetworkModeSettingsPayload | LoginPayload
           | SetMotoLagStatusPayload | RebootPayload | SetMotoStatusDSTargetFreqPayload
           | SetStatusSecuritySettingsPayload)
"""Payload types."""
Response = (GetHomeAddressResponse | GetMultipleHNAPsResponse | GetNetworkModeSettingsResponse
            | LoginResponse | SetMotoLagStatusResponse | SetStatusLogSettingsResponse
            | SetStatusSecuritySettingsResponse)
"""Response types."""
