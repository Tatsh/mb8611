"""Main command."""
import json
import warnings
from typing import Any, Final, Literal, cast

import click
from urllib3.exceptions import InsecureRequestWarning

from .api import Action, Response
from .client import Client
from .constants import ROW_DELIMITERS, TABLE_KEYS
from .utils import parse_table_str, setup_logging

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
TopKey = Literal['GetMultipleHNAPsResponse', 'LoginResponse']


@click.command()
@click.argument('action', type=click.Choice(list(ACTION_ALIAS_MAPPING.keys())))
@click.option('-H', '--host', help='Host to connect to.', default='192.168.100.1')
@click.option('-d', '--debug', is_flag=True, help='Enable debug level logging.')
@click.option('-j',
              '--output-json',
              is_flag=True,
              help='Only output JSON. Encoded lists (tables) will still be parsed.')
@click.option('-p', '--password', required=True, help='Administrator password.')
@click.option('-u', '--username', default='admin', help='Administrator username.')
def main(action: ActionAlias,
         host: str,
         password: str,
         debug: bool = False,
         output_json: bool = False,
         username: str = 'admin') -> None:
    """Main CLI."""
    # Unfortunately, we have to ignore certificate warnings as there is no way to install a good
    # certificate on the device.
    warnings.filterwarnings(action='ignore', category=InsecureRequestWarning)
    setup_logging(debug)
    with Client(password, host, username) as client:
        response: Response
        if action == 'clear-log':
            response = client.call_hnap(
                'SetStatusLogSettings',
                {'SetStatusLogSettings': {
                    'MotoStatusLogAction': '1',
                    'MotoStatusLogXXX': 'XXX'
                }},
                check=not output_json)
        elif action == 'reboot':
            response = client.call_hnap('SetStatusSecuritySettings',
                                        {'SetStatusSecuritySettings': {
                                            'MotoStatusSecXXX': 'XXX'
                                        }},
                                        check=not output_json)
        else:
            response = client.call_hnap(ACTION_ALIAS_MAPPING[action], check=not output_json)
        top_key = f'{ACTION_ALIAS_MAPPING[action]}Response'
        result_key = f'{ACTION_ALIAS_MAPPING[action]}Result'
        res_d = cast(dict[str, Any], response)
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
                        list(parse_table_str(value, row_delimiter=ROW_DELIMITERS.get(k, '|+|'))))
        else:
            for k, value in res_d[top_key].items():
                if k in TABLE_KEYS:
                    res_d[top_key][k] = list(
                        parse_table_str(value, row_delimiter=ROW_DELIMITERS.get(k, '|+|')))
            click.echo(json.dumps(res_d[top_key], indent=2))
