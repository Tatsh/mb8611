from typing import Literal, NotRequired, TypedDict


class _LoginPayloadLogin(TypedDict):
    Action: Literal['login', 'request']
    Captcha: str
    LoginPassword: str
    PrivateLogin: Literal['LoginPassword']
    Username: str


class LoginPayload(TypedDict):
    """Login payload."""
    Login: _LoginPayloadLogin


class _LoginResponseLoginResponse(TypedDict):
    Challenge: NotRequired[str]
    Cookie: NotRequired[str]
    LoginResult: Literal['OK', 'FAILED', 'ERROR']
    PublicKey: NotRequired[str]


class LoginResponse(TypedDict):
    """Login response."""
    LoginResponse: _LoginResponseLoginResponse
    """Login response."""
