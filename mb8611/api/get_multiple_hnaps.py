# pylint: disable=invalid-name
from typing import Iterator, Literal, Sequence, TypedDict

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
    """
    Pass header: `SOAPACTION: "http://purenetworks.com/HNAP1/GetMultipleHNAPs"`
    """
    GetMultipleHNAPs: _GetMultipleHNAPsPayloadGetMultipleHNAPs


class _GetHomeAddressResponse(TypedDict):
    GetHomeAddressResult: str
    MotoHomeIpAddress: str
    MotoHomeIpv6Address: str
    MotoHomeMacAddress: str
    MotoHomeSfVer: str


class _GetHomeConnectionResponse(TypedDict):
    GetHomeConnectionResult: str
    MotoHomeOnline: str  # 'Connected'
    #: Number of channels connected
    #: Downstream
    MotoHomeDownNum: str
    #: Upstream
    MotoHomeUpNum: str


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


def parse_table_str(s: str, row_delimiter: str = '|+|') -> Iterator[Sequence[str]]:
    yield from (r.split('^') for r in s.split(row_delimiter))


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
    GetMotoStatusSecAccountResult: str
    # All values here are AES-128 encrypted
    CurrentLogin: str
    CurrentNameAdmin: str
    CurrentNameUser: str
    CurrentPwAdmin: str
    CurrentPwUser: str


class _GetMultipleHNAPsResponseTop(TypedDict):
    GetHomeAddressResponse: NotRequired[_GetHomeAddressResponse]
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
    GetMultipleHNAPsResult: str


class GetMultipleHNAPsResponse(TypedDict):
    GetMultipleHNAPsResponse: _GetMultipleHNAPsResponseTop
