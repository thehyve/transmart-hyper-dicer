import logging.config
import os
from pathlib import Path

import click
import yaml

from dicer.config import logging_config
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


def read_config() -> TransmartConfiguration:
    """
    Reads connnection configuration from environment variables.
    :return: Transmart configuration object
    """
    keycloak_config = KeycloakConfiguration(
        oidc_server_url='{}/auth/realms/{}'.format(
            os.environ.get('KEYCLOAK_SERVER_URL'), os.environ.get('KEYCLOAK_REALM')),
        client_id=os.environ.get('KEYCLOAK_CLIENT_ID', 'transmart-client'),
        offline_token=os.environ.get('OFFLINE_TOKEN')
    )
    config = TransmartConfiguration(
        url=os.environ.get('TRANSMART_URL'),
        keycloak_config=keycloak_config
    )
    return config


@click.command()
@click.argument('input_file', type=click.Path(dir_okay=False, exists=True, readable=True))
@click.argument('output_dir', type=click.Path(file_okay=False, writable=True))
@click.version_option()
def dicer(input_file: Path, output_dir: Path):
    setup_logging()
    hyper_dicer = HyperDicer(read_config(), Path(input_file), Path(output_dir))
    hyper_dicer.run()


def main():
    dicer()


if __name__ == '__main__':
    main()
