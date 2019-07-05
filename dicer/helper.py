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


def format_observations(observations_result: dict):
    output_cells = []
    indexed_dimensions = []
    inline_dimensions = []

    for dimension in observations_result['dimensionDeclarations']:
        if 'inline' in dimension and dimension['inline']:
            inline_dimensions.append(dimension)
        else:
            indexed_dimensions.append(dimension)

    for dimension in indexed_dimensions:
        dimension['values'] = observations_result['dimensionElements'][dimension['name']]

    for cell in observations_result['cells']:
        output_cell = {}

        i = 0
        for index in cell['dimensionIndexes']:
            if index is not None:
                output_cell[indexed_dimensions[i]['name']] = indexed_dimensions[i]['values'][int(index)]
            i += 1

        i = 0
        for index in cell['inlineDimensions']:
            output_cell[inline_dimensions[i]['name']] = index
            i += 1

        if 'stringValue' in cell:
            output_cell['stringValue'] = cell['stringValue']
        if 'numericValue' in cell:
            output_cell['numericValue'] = cell['numericValue']
        output_cells.append(output_cell)
    return output_cells
