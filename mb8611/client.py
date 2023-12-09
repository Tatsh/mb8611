"""Client class."""
import contextlib
import hmac
from collections.abc import Collection
from types import TracebackType
from typing import Any, Literal, cast, overload

from loguru import logger
from requests import Session

from .api import (
    Action,
    GetMultipleHNAPsPayload,
    GetMultipleHNAPsResponse,
    LoginPayload,
    LoginResponse,
    MultipleHNAPAction,
    Payload,
    Response,
)
from .api.settings import (
    GetNetworkModeSettingsPayload,
    GetNetworkModeSettingsResponse,
    RebootPayload,
    SetMotoLagStatusPayload,
    SetMotoLagStatusResponse,
    SetStatusLogSettingsPayload,
    SetStatusLogSettingsResponse,
    SetStatusSecuritySettingsPayload,
)
from .constants import MUST_BE_CALLED_FROM_MULTIPLE, SHARED_HEADERS
from .utils import make_hnap_auth, make_soap_action_uri


class CallHNAPError(Exception):
    pass


class LockedError(Exception):
    def __init__(self) -> None:
        super().__init__('The modem interface is most likely locked due to failed login attempts. '
                         'Wait at least five minutes before attempting again.')


class MustUseCallHNAPError(Exception):
    def __init__(self) -> None:
        super().__init__('Actions list should have at least 2 elements. Use call_hnap() for a '
                         'single action.')


class Client:
    """Client implementation."""
    def __init__(self, password: str, host: str = '192.168.100.1', username: str = 'admin') -> None:
        self.hnap1_endpoint = f'https://{host}/HNAP1/'
        self.host = host
        self.password = password
        self.username = username
        self.session = Session()
        self.session.headers.update(SHARED_HEADERS)
        self.private_key = 'withoutloginkey'

    def login(self) -> None:
        """Login."""
        response: LoginResponse = self.call_hnap(
            'Login', {
                'Login': {
                    'Action': 'request',
                    'Username': self.username,
                    'LoginPassword': '',
                    'Captcha': '',
                    'PrivateLogin': 'LoginPassword'
                }
            })
        if response['LoginResponse']['LoginResult'] == 'FAILED':
            raise LockedError
        assert 'PublicKey' in response['LoginResponse']
        assert 'Challenge' in response['LoginResponse']
        public_key = response['LoginResponse']['PublicKey']
        challenge = response['LoginResponse']['Challenge']
        if 'Cookie' in response['LoginResponse']:
            self.session.cookies.set('uid',
                                     response['LoginResponse']['Cookie'],
                                     path='/',
                                     domain=self.host)  # type: ignore[no-untyped-call]
        self.private_key = hmac.new((public_key + self.password).encode(), challenge.encode(),
                                    'md5').hexdigest().upper()
        self.session.cookies.set('PrivateKey', self.private_key, path='/',
                                 domain=self.host)  # type: ignore[no-untyped-call]
        for path in ('/font', '/js/SOAP', '/js', '/css', '/', '/image', '/HNAP1'):
            self.session.cookies.set('',
                                     'Secure',
                                     path=path,
                                     domain=self.host,
                                     rest={'HttpOnly': True})  # type: ignore[no-untyped-call]
        response = self.call_hnap(
            'Login', {
                'Login': {
                    'Action':
                        'request',
                    'Username':
                        self.username,
                    'LoginPassword':
                        hmac.new(self.private_key.encode(), challenge.encode(),
                                 'md5').hexdigest().upper(),
                    'Captcha':
                        '',
                    'PrivateLogin':
                        'LoginPassword'
                }
            })
        assert response['LoginResponse']['LoginResult'] == 'OK'

    @overload
    def call_hnap(self,
                  action: Literal['GetMultipleHNAPs'],
                  payload: GetMultipleHNAPsPayload,
                  check: bool = ...) -> GetMultipleHNAPsResponse:
        ...

    @overload
    def call_hnap(self,
                  action: Literal['GetNetworkModeSettings'],
                  payload: GetNetworkModeSettingsPayload,
                  check: bool = ...) -> GetNetworkModeSettingsResponse:
        ...

    @overload
    def call_hnap(self,
                  action: Literal['Login'],
                  payload: LoginPayload,
                  check: bool = ...) -> LoginResponse:
        ...

    @overload
    def call_hnap(self,
                  action: Literal['SetMotoLagStatus'],
                  payload: SetMotoLagStatusPayload,
                  check: bool = ...) -> SetMotoLagStatusResponse:
        ...

    @overload
    def call_hnap(self,
                  action: Literal['SetStatusLogSettings'],
                  payload: SetStatusLogSettingsPayload,
                  check: bool = ...) -> SetStatusLogSettingsResponse:
        ...

    @overload
    def call_hnap(self,
                  action: Literal['SetStatusSecuritySettings'],
                  payload: SetStatusSecuritySettingsPayload | RebootPayload,
                  check: bool = ...) -> SetStatusLogSettingsResponse:
        ...

    @overload
    def call_hnap(self,
                  action: Action,
                  payload: Literal[None] = ...,
                  check: bool = ...) -> Response:
        ...

    @overload
    def call_hnap(self, action: str, payload: Any = ..., check: bool = ...) -> Response:
        ...

    def call_hnap(self,
                  action: Action | str,
                  payload: Payload | None = None,
                  check: bool = True) -> Response:
        """Invoke an action."""
        # Clear invalid cookie. Chrome interprets this set-cookie header as having a key '' and
        # value 'Secure'. requests.cookies interprets this in the opposite manner.
        with contextlib.suppress(KeyError):
            self.session.cookies.clear(self.host, '/HNAP1', 'Secure')
        if action in MUST_BE_CALLED_FROM_MULTIPLE:
            return self.call_multiple_hnaps((cast(MultipleHNAPAction, action),), check=False)
        logger.debug(f'Calling {action}')
        headers = dict(HNAP_AUTH=make_hnap_auth(action, self.private_key),
                       SOAPACTION=make_soap_action_uri(action))
        logger.debug(f'Headers: {headers}')
        logger.debug(f'Cookies: {self.session.cookies.get_dict()}')  # type: ignore[no-untyped-call]
        logger.debug(f'Payload: {payload}')
        r = self.session.post(self.hnap1_endpoint, headers=headers, json=payload, verify=False)
        r.raise_for_status()
        res = r.json()
        logger.debug(f'Response: {res}')
        if check and res[f'{action}Response'][f'{action}Result'] != 'OK':
            raise CallHNAPError
        return cast(Response, res)

    def call_multiple_hnaps(self,
                            actions: Collection[MultipleHNAPAction],
                            check: bool = True) -> GetMultipleHNAPsResponse:
        """
        Call multiple HNAPs. Equivalent to calling ``call_hnap`` with action ``'GetMultipleHNAPs'``
        and the correct payload. Some actions must be called this way in any case.
        """
        return self.call_hnap('GetMultipleHNAPs',
                              cast(GetMultipleHNAPsPayload,
                                   {'GetMultipleHNAPs': {
                                       action: ''
                                       for action in actions
                                   }}),
                              check=check)

    def logout(self) -> Any:
        """Logout."""
        return self.call_hnap('Logout')

    def __enter__(self) -> 'Client':
        """Logs in and returns a client."""
        self.login()
        return self

    def __exit__(self, exc_cls: type[BaseException] | None, base_exc: BaseException | None,
                 traceback: TracebackType | None) -> None:
        """Performs logout action."""
        self.session.get(f'https://{self.host}/Logout.html')
