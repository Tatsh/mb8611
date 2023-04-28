"""Main command."""
from typing import Any
import json
import warnings

from urllib3.exceptions import InsecureRequestWarning
import click

from .client import Client
from .constants import ROW_DELIMITERS, TABLE_KEYS
from .utils import parse_table_str, setup_logging

ACTION_ALIAS_MAPPING = {
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
def main(action: str,
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
        resp: dict[str, Any]
        if action == 'clear-log':
            resp = client.call_hnap(
                'SetStatusLogSettings',
                dict(SetStatusLogSettings=dict(MotoStatusLogAction='1', MotoStatusLogXXX='XXX')),
                check=not output_json)
        elif action == 'reboot':
            resp = client.call_hnap('SetStatusSecuritySettings',
                                    dict(SetStatusSecuritySettings=dict(MotoStatusSecXXX='XXX')),
                                    check=not output_json)
        else:
            resp = client.call_hnap(ACTION_ALIAS_MAPPING[action], check=not output_json)
        top_key = f'{ACTION_ALIAS_MAPPING[action]}Response'
        result_key = f'{ACTION_ALIAS_MAPPING[action]}Result'
        if not output_json:
            assert resp[top_key][result_key] == 'OK'
        assert top_key in resp
        if not output_json:
            for k, value in sorted(resp[top_key].items()):
                if k == result_key:
                    continue
                if k not in TABLE_KEYS:
                    click.echo(f'{k}: {value}')
                else:
                    click.echo(
                        list(parse_table_str(value, row_delimiter=ROW_DELIMITERS.get(k, '|+|'))))
        else:
            for k, value in resp[top_key].items():
                if k in TABLE_KEYS:
                    resp[top_key][k] = list(
                        parse_table_str(value, row_delimiter=ROW_DELIMITERS.get(k, '|+|')))
            click.echo(json.dumps(resp[top_key], indent=2))
