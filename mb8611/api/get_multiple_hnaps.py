"""Type information for use with the ``GetMultipleHNAPs`` API."""
from typing import Literal, TypedDict

from typing_extensions import NotRequired


class _GetMultipleHNAPsPayloadGetMultipleHNAPs(TypedDict, total=False):
    GetHomeAddress: Literal['']
    GetHomeConnection: Literal['']
    GetMotoLagStatus: Literal['']
    GetMotoStatusConnectionInfo: Literal['']
    GetMotoStatusDownstreamChannelInfo: Literal['']
    GetMotoStatusSoftware: Literal['']
    GetMotoStatusStartupSequence: Literal['']
    GetMotoStatusUpstreamChannelInfo: Literal['']
    GetMotoStatusXXX: Literal['']
    GetMotoStatusSecAccount: Literal['']
    GetMotoStatusSecXXX: Literal['']
    GetMotoStatusLog: Literal['']
    GetMotoStatusLogXXX: Literal['']


class GetMultipleHNAPsPayload(TypedDict):
    """Multiple HNAPs payload."""
    GetMultipleHNAPs: _GetMultipleHNAPsPayloadGetMultipleHNAPs


class GetHomeAddressResponse(TypedDict):
    """Network address information."""
    GetHomeAddressResult: Literal['OK', 'UN-AUTH']
    MotoHomeIpAddress: str
    """IPv4 address."""
    MotoHomeIpv6Address: str
    """IPv6 address."""
    MotoHomeMacAddress: str
    """MAC address."""
    MotoHomeSfVer: str
    """Firmware version."""


class _GetHomeConnectionResponse(TypedDict):
    GetHomeConnectionResult: str
    MotoHomeOnline: str
    """``'Connected'``."""
    MotoHomeDownNum: str
    """Downstream number of channels connected."""
    MotoHomeUpNum: str
    """Upstream number of channels connected."""


class _GetMotoStatusSoftwareResponse(TypedDict):
    GetMotoStatusSoftwareResult: str
    StatusSoftwareCertificate: str
    StatusSoftwareCustomerVer: str
    StatusSoftwareHdVer: str
    StatusSoftwareMac: str
    StatusSoftwareSerialNum: str
    StatusSoftwareSfVer: str
    StatusSoftwareSpecVer: str


class XXXResponse(TypedDict):
    """Unknown."""
    XXX: str


class _GetMotoStatusXXXResponse(XXXResponse, TypedDict):
    GetMotoStatusXXXResult: str


class _GetMotoLagStatusResponse(TypedDict):
    GetMotoLagStatusResult: str
    MotoLagCurrentStatus: str


class _GetMotoStatusConnectionInfoResponse(TypedDict):
    GetMotoStatusConnectionInfoResult: str
    MotoConnNetworkAccess: str
    MotoConnSystemUpTime: str


class _GetMotoStatusDownstreamChannelInfoResponse(TypedDict):
    GetMotoStatusDownstreamChannelInfoResult: str
    """
    Bonded Channels
    Table string with `|+|` as the row delimiter, `^` for columns.
    Columns are:
        - Channel
        - Lock Status
        - Modulation
        - Channel ID
        - Freq. (MHz)
        - Pwr (dBmV)
        - SNR (dB)
        - Corrected
        - Uncorrected
    """
    MotoConnDownstreamChannel: str


class _GetMotoStatusStartupSequenceResponse(TypedDict):
    GetMotoStatusStartupSequenceResult: str
    MotoConnBootComment: str
    MotoConnBootStatus: str
    MotoConnConfigurationFileComment: str
    MotoConnConfigurationFileStatus: str
    MotoConnConnectivityComment: str
    MotoConnConnectivityStatus: str
    MotoConnDSComment: str
    MotoConnDSFreq: str
    MotoConnSecurityComment: str
    MotoConnSecurityStatus: str


class _GetMotoStatusUpstreamChannelInfoResponse(TypedDict):
    GetMotoStatusUpstreamChannelInfoResult: str
    """
    Format is same as `MotoConnDownstreamChannel` but columns are:
        - Channel
        - Lock Status
        - Channel Type
        - Channel ID
        - Symb. Rate (Ksym/sec)
        - Freq. (MHz)
        - Pwr (dBmV)
    """
    MotoConnUpstreamChannel: str


class _GetMotoStatusLogResponse(TypedDict):
    GetMotoStatusLogResult: str
    # Table but row delimiter is `}-{`.
    MotoStatusLogList: str


class _GetMotoStatusLogXXXResponse(XXXResponse, TypedDict):
    GetMotoStatusLogXXXResult: str


class _GetMotoStatusSecXXXResponse(XXXResponse, TypedDict):
    GetMotoStatusSecXXXResult: str


class _GetMotoStatusSecAccountResponse(TypedDict):
    """
    All values other than ``GetMotoStatusSecAccountResult`` are AES-128 encrypted.

    The key is the ``PrivateKey`` assigned at login.
    """
    CurrentLogin: str
    CurrentNameAdmin: str
    CurrentNameUser: str
    CurrentPwAdmin: str
    CurrentPwUser: str
    GetMotoStatusSecAccountResult: str


class _GetMultipleHNAPsResponseTop(TypedDict):
    GetHomeAddressResponse: NotRequired[GetHomeAddressResponse]
    GetHomeConnectionResponse: NotRequired[_GetHomeConnectionResponse]
    GetMotoLagStatusResponse: NotRequired[_GetMotoLagStatusResponse]
    GetMotoStatusConnectionInfoResponse: NotRequired[_GetMotoStatusConnectionInfoResponse]
    GetMotoStatusDownstreamChannelInfoResponse: NotRequired[
        _GetMotoStatusDownstreamChannelInfoResponse]
    GetMotoStatusLogResponse: NotRequired[_GetMotoStatusLogResponse]
    GetMotoStatusLogXXXResponse: NotRequired[_GetMotoStatusLogXXXResponse]
    GetMotoStatusSecAccountResponse: NotRequired[_GetMotoStatusSecAccountResponse]
    GetMotoStatusSecXXXResponse: NotRequired[_GetMotoStatusSecXXXResponse]
    GetMotoStatusSoftwareResponse: NotRequired[_GetMotoStatusSoftwareResponse]
    GetMotoStatusStartupSequenceResponse: NotRequired[_GetMotoStatusStartupSequenceResponse]
    GetMotoStatusUpstreamChannelInfoResponse: NotRequired[_GetMotoStatusUpstreamChannelInfoResponse]
    GetMotoStatusXXXResponse: NotRequired[_GetMotoStatusXXXResponse]
    GetMultipleHNAPsResult: Literal['OK', 'UN-AUTH']


class GetMultipleHNAPsResponse(TypedDict):
    """Multiple HNAPs response."""
    GetMultipleHNAPsResponse: _GetMultipleHNAPsResponseTop
