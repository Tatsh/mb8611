"""Client class."""
import contextlib
import hmac
import logging
from collections.abc import Collection
from types import TracebackType
from typing import Any, Literal, cast, overload

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

logger = logging.getLogger(__name__)


class CallHNAPError(Exception):
    def __init__(self, response: Response) -> None:
        super().__init__(f'HNAP error: {response}')


class LockedError(Exception):
    def __init__(self) -> None:
        super().__init__('The modem interface is most likely locked due to failed login attempts. '
                         'Wait at least five minutes before attempting again.')


class LoginFailed(RuntimeError):
    pass


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
        """Login. This is 99% the same as what happens in a browser but is not fully correct."""
        response = self.call_hnap('Login', {
            'Login': {
                'Action': 'request',
                'Username': self.username,
                'LoginPassword': '',
                'Captcha': '',
                'PrivateLogin': 'LoginPassword'
            }
        },
                                  check=False)
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
        response = self.call_hnap('Login', {
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
        },
                                  check=False)
        if response['LoginResponse']['LoginResult'] != 'OK':
            raise LoginFailed

    @overload
    def call_hnap(self,
                  action: Literal['GetMultipleHNAPs'],
                  payload: GetMultipleHNAPsPayload,
                  check: bool = ...) -> GetMultipleHNAPsResponse:  # pragma: no cover
        ...

    @overload
    def call_hnap(self,
                  action: Literal['GetNetworkModeSettings'],
                  payload: GetNetworkModeSettingsPayload,
                  check: bool = ...) -> GetNetworkModeSettingsResponse:  # pragma: no cover
        ...

    @overload
    def call_hnap(self,
                  action: Literal['Login'],
                  payload: LoginPayload,
                  check: bool = ...) -> LoginResponse:  # pragma: no cover
        ...

    @overload
    def call_hnap(self,
                  action: Literal['SetMotoLagStatus'],
                  payload: SetMotoLagStatusPayload,
                  check: bool = ...) -> SetMotoLagStatusResponse:  # pragma: no cover
        ...

    @overload
    def call_hnap(self,
                  action: Literal['SetStatusLogSettings'],
                  payload: SetStatusLogSettingsPayload,
                  check: bool = ...) -> SetStatusLogSettingsResponse:  # pragma: no cover
        ...

    @overload
    def call_hnap(self,
                  action: Literal['SetStatusSecuritySettings'],
                  payload: SetStatusSecuritySettingsPayload | RebootPayload,
                  check: bool = ...) -> SetStatusLogSettingsResponse:  # pragma: no cover
        ...

    @overload
    def call_hnap(self,
                  action: Action,
                  payload: Literal[None] = ...,
                  check: bool = ...) -> Response:  # pragma: no cover
        ...

    @overload
    def call_hnap(self,
                  action: str,
                  payload: Any = ...,
                  check: bool = ...) -> Response:  # pragma: no cover
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
        logger.debug('Calling %s', action)
        headers = dict(HNAP_AUTH=make_hnap_auth(action, self.private_key),
                       SOAPACTION=make_soap_action_uri(action))
        logger.debug('Headers: %s', headers)
        logger.debug('Cookies: %s',
                     self.session.cookies.get_dict())  # type: ignore[no-untyped-call]
        logger.debug('Payload: %s', payload)
        r = self.session.post(self.hnap1_endpoint, headers=headers, json=payload, verify=False)
        r.raise_for_status()
        res = r.json()
        logger.debug('Response: %s', res)
        if check and res[f'{action}Response'][f'{action}Result'] != 'OK':
            raise CallHNAPError(res)
        return cast(Response, res)

    def call_multiple_hnaps(self,
                            actions: Collection[MultipleHNAPAction],
                            check: bool = True) -> GetMultipleHNAPsResponse:
        """
        Call multiple HNAPs. Equivalent to calling ``call_hnap`` with action ``'GetMultipleHNAPs'``
        and the correct payload. Some actions must be called this way even if they are the only
        action.
        """
        return self.call_hnap('GetMultipleHNAPs',
                              cast(GetMultipleHNAPsPayload,
                                   {'GetMultipleHNAPs': {
                                       action: ''
                                       for action in actions
                                   }}),
                              check=check)

    def __enter__(self) -> 'Client':
        """Logs in and returns a client."""
        self.login()
        return self

    def __exit__(self, exc_cls: type[BaseException] | None, base_exc: BaseException | None,
                 traceback: TracebackType | None) -> None:
        """Performs logout action."""
        self.session.get(f'https://{self.host}/Logout.html')
