"""Main command."""
from typing import Any, Final, Literal, cast
import json
import logging
import warnings

from urllib3.exceptions import InsecureRequestWarning
import click

from .api import Action
from .api.settings import RebootPayload, SetStatusLogSettingsPayload
from .client import CallHNAPError, Client, LoginFailed
from .constants import ROW_DELIMITERS, TABLE_KEYS
from .utils import parse_table_str

ActionAlias = Literal['addr', 'address', 'clear-log', 'conn', 'connection', 'connection-info',
                      'conninfo', 'down', 'downstream', 'lag', 'lag-status', 'log', 'reboot',
                      'software', 'software-status', 'startup', 'startup-sequence', 'up',
                      'upstream']
ACTION_ALIAS_MAPPING: Final[dict[ActionAlias, Action]] = {
    'addr': 'GetHomeAddress',
    'address': 'GetHomeAddress',
    'clear-log': 'SetStatusLogSettings',
    'conn': 'GetHomeConnection',
    'connection': 'GetHomeConnection',
    'connection-info': 'GetMotoStatusConnectionInfo',
    'conninfo': 'GetMotoStatusConnectionInfo',
    'down': 'GetMotoStatusDownstreamChannelInfo',
    'downstream': 'GetMotoStatusDownstreamChannelInfo',
    'lag': 'GetMotoLagStatus',
    'lag-status': 'GetMotoLagStatus',
    'log': 'GetMotoStatusLog',
    'reboot': 'SetStatusSecuritySettings',
    'software': 'GetMotoStatusSoftware',
    'software-status': 'GetMotoStatusSoftware',
    'startup': 'GetMotoStatusStartupSequence',
    'startup-sequence': 'GetMotoStatusStartupSequence',
    'up': 'GetMotoStatusUpstreamChannelInfo',
    'upstream': 'GetMotoStatusUpstreamChannelInfo',
}
ACTION_PAYLOAD_MAPPING: Final[dict[ActionAlias, SetStatusLogSettingsPayload | RebootPayload]] = {
    'clear-log': {
        'SetStatusLogSettings': {
            'MotoStatusLogAction': '1',
            'MotoStatusLogXXX': 'XXX'
        }
    },
    'reboot': {
        'SetStatusSecuritySettings': {
            'MotoStatusSecXXX': 'XXX'
        }
    }
}


@click.command()
@click.argument('action', type=click.Choice(list(ACTION_ALIAS_MAPPING.keys())))
@click.option('-H', '--host', help='Host to connect to.', default='192.168.100.1')
@click.option('-d', '--debug', is_flag=True, help='Enable debug level logging.')
@click.option('-j',
              '--json',
              'output_json',
              is_flag=True,
              help='Only output JSON. Encoded lists (tables) will still be parsed.')
@click.option('-p', '--password', default='', help='Administrator password.')
@click.option('-u', '--username', default='admin', help='Administrator username.')
def main(action: ActionAlias,
         host: str,
         password: str = '',
         username: str = 'admin',
         *,
         debug: bool = False,
         output_json: bool = False) -> None:
    """Manage a MB8611 series modem."""
    # Unfortunately, we have to ignore certificate warnings as there is no way to install a good
    # certificate on the device.
    warnings.filterwarnings(action='ignore', category=InsecureRequestWarning)
    logging.basicConfig(level=logging.DEBUG if debug else logging.ERROR)
    try:
        with Client(password, host, username) as client:
            try:
                response = client.call_hnap(ACTION_ALIAS_MAPPING[action],
                                            ACTION_PAYLOAD_MAPPING.get(action),
                                            check=not output_json)
            except CallHNAPError as e:
                click.echo(str(e), err=True)
                raise click.Abort from e
            top_key = f'{ACTION_ALIAS_MAPPING[action]}Response'
            result_key = f'{ACTION_ALIAS_MAPPING[action]}Result'
            res_d = cast('dict[str, Any]', response)
            if not output_json:
                assert res_d[top_key][result_key] == 'OK'
            assert top_key in response
            if not output_json:
                for k, value in sorted(res_d[top_key].items()):
                    if k == result_key:
                        continue
                    if k not in TABLE_KEYS:
                        click.echo(f'{k}: {value}')
                    else:
                        click.echo(
                            list(parse_table_str(value, row_delimiter=ROW_DELIMITERS.get(k,
                                                                                         '|+|'))))
            else:
                for k, value in res_d[top_key].items():
                    if k in TABLE_KEYS:
                        res_d[top_key][k] = list(
                            parse_table_str(value, row_delimiter=ROW_DELIMITERS.get(k, '|+|')))
                click.echo(json.dumps(res_d[top_key], indent=2))
    except LoginFailed as e:
        click.echo('Login failed.', err=True)
        raise click.Abort from e
