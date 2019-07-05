import logging.config
import os
from pathlib import Path

import click
import yaml

from dicer.config import logging_config
from dicer.hyper_dicer import HyperDicer


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


@click.command()
@click.argument('input_file', type=click.Path(dir_okay=False, exists=True, readable=True))
@click.argument('output_dir', type=click.Path(file_okay=False, writable=True))
def dicer(input_file: Path, output_dir: Path):
    setup_logging()
    hyper_dicer = HyperDicer(Path(input_file), Path(output_dir))
    hyper_dicer.run()


def main():
    dicer()


if __name__ == '__main__':
    main()
