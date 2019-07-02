import os
import sys
import yaml
import click
import logging

from dicer.config import logging_config
from .transmart_rest_client import TransmartRestClient


def setup_logging(default_level=logging.INFO):
    """
    Setup logging configuration
    :param default_level: default logging level
    """
    path = logging_config.get('path', 'dicer/logging.yaml')
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def run(input_file: str):
    """
    TODO Sample usage - getting observations from tranSMART and outputting the response to the console.
    :param input_file: path to the file containing constraint in JSON format
            to be used in tranSMART call
    :return
    """
    logging.info('Starting...')
    try:
        contents = {}
        with open(input_file, 'r') as f:
            logging.info('Reading constraint from file {} ...'.format(input_file))
            contents = f.read()
        transmart_client = TransmartRestClient()
        json_response = transmart_client.get_observations(contents)
        logging.info('Received response: {}'.format(json_response))
        logging.info('Done.')
    except Exception as e:
        logging.error(e)
        sys.exit(1)


@click.command()
@click.argument('input_file')
def dicer(input_file: str):
    setup_logging()
    run(input_file)


def main():
    dicer()


if __name__ == '__main__':
    main()
