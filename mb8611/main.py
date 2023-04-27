"""Main command."""
from loguru import logger
import click


@click.command()
@click.option('-d', '--debug', is_flag=True, help='Enable debug level logging')
def main(debug: bool = False) -> None:
    setup_logging(debug)
