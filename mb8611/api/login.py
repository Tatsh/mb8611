# pylint: disable=invalid-name
from typing import Literal, TypedDict

from typing_extensions import NotRequired


class _LoginPayloadLogin(TypedDict):
    Action: Literal['login', 'request']
    Captcha: str
    LoginPassword: str
    PrivateLogin: Literal['LoginPassword']
    Username: str


class LoginPayload(TypedDict):
    """
    POST to /HNAP1/.

    When Action=='login':

    HNAP_AUTH:
        SOAP_NAMESPACE = 'http://purenetworks.com/HNAP1/'
        soapActionURI = '"'+SOAP_NAMESPACE + aSoapAction + '"'
        current_time = now()
        current_time = str(floor(current_time) % 2000000000000)
        auth = hmac_hd5(private_key, current_time + soapActionURI).hexdigest().upper()
    LoginPassword:
        hmac_md5(private_key, prior_response['LoginResponse']['Challenge']).hexdigest().upper()

    """
    Login: _LoginPayloadLogin


class _LoginResponseLoginResponse(TypedDict):
    Challenge: NotRequired[str]
    Cookie: NotRequired[str]
    LoginResult: Literal['OK', 'FAILED', 'ERROR']
    PublicKey: NotRequired[str]


class LoginResponse(TypedDict):
    """
    PrivateKey cookie:
        hmac_md5(response['LoginResponse']['PublicKey'] + password,
                 response['LoginResponse']['Challenge']).hexdigest().upper()
    uid cookie:
        response['LoginResponse']['Cookie'] at '/'
    """
    LoginResponse: _LoginResponseLoginResponse
