"""Main command."""
import hmac
import warnings

from urllib3.exceptions import InsecureRequestWarning
import click
import requests

from .api.get_multiple_hnaps import GetMultipleHNAPsResponse
from .api.login import LoginResponse
from .constants import SHARED_HEADERS
from .utils import make_hnap_auth, make_soap_action_uri, setup_logging


@click.command()
@click.option('-H', '--host', required=True)
@click.option('-d', '--debug', is_flag=True, help='Enable debug level logging')
@click.option('-u', '--username', default='admin')
@click.option('-p', '--password', required=True)
def main(host: str, password: str, username: str = 'admin', debug: bool = False) -> None:
    # Unfortunately, we have to ignore certificate warnings as there is no way to install a good
    # certificate on the device.
    warnings.filterwarnings(action='ignore', category=InsecureRequestWarning)
    setup_logging(debug)
    session = requests.Session()
    session.headers.update(SHARED_HEADERS)
    hnap1_endpoint = f'https://{host}/HNAP1/'
    #region Login
    soap_action_uri = make_soap_action_uri('Login')
    r = session.post(hnap1_endpoint,
                     headers={
                         'HNAP_AUTH': make_hnap_auth('Login'),
                         'Referer': f'https://{host}/Login.html',
                         'SOAPAction': soap_action_uri
                     },
                     json=dict(Login=dict(Action='request',
                                          Username=username,
                                          LoginPassword='',
                                          Captcha='',
                                          PrivateLogin='LoginPassword')),
                     verify=False)
    r.raise_for_status()
    resp: LoginResponse = r.json()
    if resp['LoginResponse']['LoginResult'] == 'FAILED':
        click.echo('The modem interface is most likely locked due to failed login attempts. Wait '
                   'at least five minutes before attempting again.')
        raise click.Abort()
    assert 'PublicKey' in resp['LoginResponse']
    assert 'Challenge' in resp['LoginResponse']
    public_key = resp['LoginResponse']['PublicKey']
    challenge = resp['LoginResponse']['Challenge']
    if 'Cookie' in resp['LoginResponse']:
        session.cookies.set('uid', resp['LoginResponse']['Cookie'])  # type: ignore[no-untyped-call]
    private_key = hmac.new((public_key + password).encode(), challenge.encode(),
                           'md5').hexdigest().upper()
    session.cookies.set('PrivateKey', private_key, path='/')  # type: ignore[no-untyped-call]
    session.cookies.set('Secure', '')  # type: ignore[no-untyped-call]
    r = session.post(
        hnap1_endpoint,
        headers={
            'HNAP_AUTH': make_hnap_auth('Login', private_key),
            'Referer': f'https://{host}/Login.html',
            'SOAPAction': soap_action_uri
        },
        # I have seen Action='login' used for this step but it fails here
        json=dict(Login=dict(Action='request',
                             Username=username,
                             LoginPassword=hmac.new(private_key.encode(), challenge.encode(),
                                                    'md5').hexdigest().upper(),
                             Captcha='',
                             PrivateLogin='LoginPassword')),
        verify=False)
    r.raise_for_status()
    resp = r.json()
    assert resp['LoginResponse']['LoginResult'] == 'OK'
    #endregion
    #region Example API call with GetMultipleHNAPs
    r = session.post(hnap1_endpoint,
                     headers={
                         'HNAP_AUTH': make_hnap_auth('GetMultipleHNAPs', private_key),
                         'SOAPAction': make_soap_action_uri('GetMultipleHNAPs')
                     },
                     json={
                         'GetMultipleHNAPs': {
                             'GetMotoStatusSoftware': '',
                             'GetMotoStatusXXX': ''
                         },
                     },
                     verify=False)
    r.raise_for_status()
    multi_hnaps_resp: GetMultipleHNAPsResponse = r.json()
    assert multi_hnaps_resp['GetMultipleHNAPsResponse']['GetMultipleHNAPsResult'] == 'OK'
    click.echo(multi_hnaps_resp)
    #endregion
