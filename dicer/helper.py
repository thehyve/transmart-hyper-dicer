import json
import logging
import sys
from pathlib import Path


def read_tm_query_from_file(input_file: Path) -> dict:
    try:
        with input_file.open() as json_file:
            logging.info('Reading constraint from file {} ...'.format(input_file))
            contents = json.load(json_file)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    return contents
