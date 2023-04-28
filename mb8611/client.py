"""Client class."""
import hmac
from inspect import Traceback
from typing import Any, Collection, Type

from loguru import logger
from requests import Session

from .api.get_multiple_hnaps import GetMultipleHNAPsResponse

from .api import LoginResponse
from .constants import MUST_BE_CALLED_FROM_MULTIPLE, SHARED_HEADERS
from .utils import make_hnap_auth, make_soap_action_uri


class LockedError(Exception):
    pass


class Client:
    def __init__(self, password: str, host: str = '192.168.100.1', username: str = 'admin') -> None:
        self.hnap1_endpoint = f'https://{host}/HNAP1/'
        self.host = host
        self.password = password
        self.username = username
        self.session = Session()
        self.session.headers.update(SHARED_HEADERS)
        self.private_key = 'withoutloginkey'

    def login(self) -> None:
        resp: LoginResponse = self.call_hnap(
            'Login',
            dict(Login=dict(Action='request',
                            Username=self.username,
                            LoginPassword='',
                            Captcha='',
                            PrivateLogin='LoginPassword')))
        if resp['LoginResponse']['LoginResult'] == 'FAILED':
            raise LockedError(
                'The modem interface is most likely locked due to failed login attempts. Wait '
                'at least five minutes before attempting again.')
        assert 'PublicKey' in resp['LoginResponse']
        assert 'Challenge' in resp['LoginResponse']
        public_key = resp['LoginResponse']['PublicKey']
        challenge = resp['LoginResponse']['Challenge']
        if 'Cookie' in resp['LoginResponse']:
            self.session.cookies.set('uid',
                                     resp['LoginResponse']['Cookie'],
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
        resp = self.call_hnap(
            'Login',
            dict(Login=dict(Action='request',
                            Username=self.username,
                            LoginPassword=hmac.new(self.private_key.encode(), challenge.encode(),
                                                   'md5').hexdigest().upper(),
                            Captcha='',
                            PrivateLogin='LoginPassword')))
        assert resp['LoginResponse']['LoginResult'] == 'OK'

    def call_hnap(self, action: str, payload: Any = None, check: bool = True) -> Any:
        # Clear invalid cookie. Chrome interprets this set-cookie header as having a key '' and
        # value 'Secure'. requests.cookies interprets this in the opposite manner.
        try:
            self.session.cookies.clear(self.host, '/HNAP1', 'Secure')
        except KeyError:
            pass
        if action in MUST_BE_CALLED_FROM_MULTIPLE:
            return self.call_multiple_hnaps((action,), check=False)
        logger.debug(f'Calling {action}')
        headers = dict(HNAP_AUTH=make_hnap_auth(action, self.private_key),
                       SOAPACTION=make_soap_action_uri(action))
        logger.debug(f'Headers: {headers}')
        logger.debug(f'Cookies: {self.session.cookies.get_dict()}')
        logger.debug(f'Payload: {payload}')
        r = self.session.post(self.hnap1_endpoint, headers=headers, json=payload, verify=False)
        r.raise_for_status()
        res = r.json()
        logger.debug(f'Response: {res}')
        if check:
            assert res[f'{action}Response'][f'{action}Result'] == 'OK'
        return res

    def call_multiple_hnaps(self,
                            actions: Collection[str],
                            check: bool = True) -> GetMultipleHNAPsResponse:
        if check and len(actions) < 2:
            raise ValueError(
                'Actions list should have at least 2 elements. Use call_hnap() for a single action.'
            )
        return self.call_hnap('GetMultipleHNAPs',
                              dict(GetMultipleHNAPs={action: ''
                                                     for action in actions}),
                              check=check)

    def logout(self) -> None:
        return self.call_hnap('Logout')

    def __enter__(self) -> 'Client':
        self.login()
        return self

    def __exit__(self, exc_cls: Type[BaseException], base_exc: BaseException,
                 traceback: Traceback) -> None:
        self.session.get(f'https://{self.host}/Logout.html')
