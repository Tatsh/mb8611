from mb8611.client import CallHNAPError, Client, LockedError, LoginFailed
import pytest
import requests_mock as req_mock

HOST = '192.168.12.1'


def test_login_locked(requests_mock: req_mock.Mocker) -> None:
    client = Client('pass', HOST)
    requests_mock.post(f'https://{HOST}/HNAP1/', json={'LoginResponse': {'LoginResult': 'FAILED'}})
    with pytest.raises(LockedError):
        client.login()


def test_login_failed(requests_mock: req_mock.Mocker) -> None:
    client = Client('pass', HOST)
    requests_mock.post(f'https://{HOST}/HNAP1/', [{
        'json': {
            'LoginResponse': {
                'Challenge': 'a',
                'Cookie': 'uid',
                'LoginResult': 'OK',
                'PublicKey': 'a'
            }
        }
    }, {
        'json': {
            'LoginResponse': {
                'LoginResult': 'FAILED'
            }
        }
    }])
    with pytest.raises(LoginFailed):
        client.login()
    assert 'uid' in client.session.cookies
    assert 'PrivateKey' in client.session.cookies


def test_login_failed_no_cookie(requests_mock: req_mock.Mocker) -> None:
    client = Client('pass', HOST)
    requests_mock.post(f'https://{HOST}/HNAP1/', [{
        'json': {
            'LoginResponse': {
                'Challenge': 'a',
                'LoginResult': 'OK',
                'PublicKey': 'a'
            }
        }
    }, {
        'json': {
            'LoginResponse': {
                'LoginResult': 'FAILED'
            }
        }
    }])
    with pytest.raises(LoginFailed):
        client.login()
    assert 'uid' not in client.session.cookies


def test_login(requests_mock: req_mock.Mocker) -> None:
    client = Client('pass', HOST)
    requests_mock.post(f'https://{HOST}/HNAP1/', [{
        'json': {
            'LoginResponse': {
                'Challenge': 'a',
                'Cookie': 'uid',
                'LoginResult': 'OK',
                'PublicKey': 'a'
            }
        }
    }, {
        'json': {
            'LoginResponse': {
                'LoginResult': 'OK'
            }
        }
    }])
    try:
        client.login()
    except LoginFailed:
        pytest.fail('Unexpected exception')
    assert 'uid' in client.session.cookies
    assert 'PrivateKey' in client.session.cookies


def test_call_hnap_single(requests_mock: req_mock.Mocker) -> None:
    client = Client('pass', HOST)
    requests_mock.post(f'https://{HOST}/HNAP1/', json={'LoginResponse': {'LoginResult': 'FAILED'}})
    with pytest.raises(CallHNAPError):
        client.call_hnap('Login', {})


def test_with_and_call_multiple_hnaps(requests_mock: req_mock.Mocker) -> None:
    requests_mock.get(f'https://{HOST}/Logout.html')
    requests_mock.post(f'https://{HOST}/HNAP1/', [{
        'json': {
            'LoginResponse': {
                'Challenge': 'a',
                'Cookie': 'uid',
                'LoginResult': 'OK',
                'PublicKey': 'a'
            }
        }
    }, {
        'json': {
            'LoginResponse': {
                'LoginResult': 'OK'
            }
        }
    }, {
        'json': {
            'GetMultipleHNAPsResponse': {
                'GetMultipleHNAPsResult': 'OK'
            }
        }
    }])
    with Client('pass', HOST) as client:
        res = client.call_hnap('GetHomeAddress', {})
        assert 'GetMultipleHNAPsResponse' in res
