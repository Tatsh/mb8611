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
    Login: _LoginPayloadLogin


class _LoginResponseLoginResponse(TypedDict):
    Challenge: NotRequired[str]
    Cookie: NotRequired[str]
    LoginResult: Literal['OK', 'FAILED', 'ERROR']
    PublicKey: NotRequired[str]


class LoginResponse(TypedDict):
    LoginResponse: _LoginResponseLoginResponse
