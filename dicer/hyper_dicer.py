from pathlib import Path
from typing import Dict

from transmart_loader.console import Console
from transmart_loader.copy_writer import TransmartCopyWriter
from transmart_loader.transmart import DataCollection

from dicer.mappers.transmart_loader_mapper import TransmartLoaderMapper
from dicer.query_results import QueryResults
from dicer.transmart_rest_client import TransmartRestClient, TransmartConfiguration


class HyperDicer:

    def __init__(self, config: TransmartConfiguration):
        self.config = config

    def copy_slice(self,
                   constraint: Dict,
                   output_dir: Path) -> None:
        """
        Reads data from a TranSMART instance using the input constraint
        and writes transmart-copy staging files to the output directory.

        :param constraint the constraint to use when reading data
        :param output_dir the directory to write staging files to
        """
        Console.info('Reading data from tranSMART...')
        transmart_client = TransmartRestClient(self.config)
        query_results = QueryResults(
            transmart_client.get_observations(constraint),
            transmart_client.get_tree_nodes(depth=0, tags=True),
            transmart_client.get_dimensions(),
            transmart_client.get_studies(),
            transmart_client.get_relation_types(),
            transmart_client.get_relations()
        )

        collection: DataCollection = TransmartLoaderMapper().map_query_results(query_results)

        Console.info('Writing files to {}'.format(output_dir))
        copy_writer = TransmartCopyWriter(str(output_dir))
        copy_writer.write_collection(collection)
        Console.info('Done.')
