import sys
from pathlib import Path

from transmart_loader.console import Console
from transmart_loader.copy_writer import TransmartCopyWriter
from transmart_loader.loader_exception import LoaderException
from transmart_loader.transmart import DataCollection

from dicer.helper import read_tm_query_from_file
from dicer.mapper import map_query_results
from dicer.query_results import QueryResults
from dicer.transmart_rest_client import TransmartRestClient, TransmartConfiguration


class HyperDicer:

    def __init__(self, config: TransmartConfiguration,
                 input_file: Path, output_dir: Path):
        self.config = config
        self.json_query = read_tm_query_from_file(input_file)
        self.output_root_dir = output_dir

    def run(self) -> None:
        """
        Construct and write all transmart-copy staging files based on the input query
        :return: None
        """
        Console.title('TranSMART Hyper Dicer')
        try:
            Console.info('Reading data from tranSMART...')
            transmart_client = TransmartRestClient(self.config)
            query_results = QueryResults(
                transmart_client.get_observations(self.json_query),
                transmart_client.get_tree_nodes(depth=0, tags=True),
                transmart_client.get_dimensions(),
                transmart_client.get_studies(),
                transmart_client.get_relation_types(),
                transmart_client.get_relations()
            )

            collection: DataCollection = map_query_results(query_results)

            Console.info('Writing files to {}'.format(self.output_root_dir))
            copy_writer = TransmartCopyWriter(str(self.output_root_dir))
            copy_writer.write_collection(collection)
            Console.info('Done.')
        except LoaderException as e:
            Console.error(e)
            sys.exit(1)
