import logging.config
import json
import os
import sys
import traceback
from pathlib import Path

import click
from dotenv import load_dotenv
import yaml
from transmart_loader.console import Console

from dicer.hyper_dicer import HyperDicer
from dicer.keycloak_rest_client import KeycloakConfiguration
from dicer.transmart_rest_client import TransmartConfiguration


def setup_logging(default_level=logging.INFO):
    """
    Setup logging configuration
    :param default_level: default logging level
    """
    path = os.environ.get('LOG_CFG', 'dicer/logging.yaml')
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def read_env_variable(variable_name: str) -> str:
    res = os.environ.get(variable_name)
    if res is None or len(res) == 0:
        logging.error(f'Please configure environment variable {variable_name}')
        sys.exit(1)
    return res


def read_config() -> TransmartConfiguration:
    """
    Reads connnection configuration from environment variables.
    :return: Transmart configuration object
    """
    keycloak_config = KeycloakConfiguration(
        url='{}/auth/realms/{}'.format(
            read_env_variable('KEYCLOAK_SERVER_URL'), read_env_variable('KEYCLOAK_REALM')),
        client_id=os.environ.get('KEYCLOAK_CLIENT_ID', 'transmart-client'),
        offline_token=read_env_variable('OFFLINE_TOKEN')
    )
    config = TransmartConfiguration(
        url=read_env_variable('TRANSMART_URL'),
        keycloak_config=keycloak_config,
        verify_cert=os.environ.get('VERIFY_CERT', True)
    )
    return config


def read_constraint_from_file(input_file: Path) -> dict:
    with input_file.open() as json_file:
        Console.info('Reading constraint from file {} ...'.format(input_file))
        return json.load(json_file)


@click.command()
@click.argument('input_file', type=click.Path(dir_okay=False, exists=True, readable=True))
@click.argument('output_dir', type=click.Path(file_okay=False, writable=True))
@click.option('--debug', is_flag=True, help='Print more verbose messages')
@click.version_option()
def dicer(input_file: Path, output_dir: Path, debug: bool):
    """Reads data from a TranSMART server using the constraint in INPUT_FILE (in JSON format)
       and writes staging files for transmart-copy to the empty directory OUTPUT_DIR.
       \f
       :param input_file: Data constraint in JSON format
       :param output_dir: Empty output directory where staging files are written
    """
    try:
        load_dotenv(os.path.join(os.getcwd(), '.env'))
        setup_logging(logging.DEBUG if debug else logging.INFO)
        Console.title('TranSMART Hyper Dicer')
        hyper_dicer = HyperDicer(read_config())
        constraint = read_constraint_from_file(Path(input_file))
        hyper_dicer.copy_slice(constraint, Path(output_dir))
    except Exception as e:
        Console.error(e)
        if debug:
            traceback.print_exc()
        sys.exit(1)


def main():
    dicer()


if __name__ == '__main__':
    main()
