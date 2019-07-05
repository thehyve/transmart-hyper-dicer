import logging
from pathlib import Path

from dicer.helper import read_tm_query_from_file
from dicer.staging.i2b2demodata.concept_dimension import ConceptDimension
from dicer.staging.i2b2demodata.patient_dimension import PatientDimension
from dicer.staging.i2b2metadata.i2b2_secure import I2b2Secure
from dicer.transmart_rest_client import TransmartRestClient


class HyperDicer:

    def __init__(self, input_file: Path, output_dir: Path):
        self.json_query = read_tm_query_from_file(input_file)
        self.output_root_dir = output_dir

        self.create_output_dirs()
        self.transmart_client = TransmartRestClient()
        self.query_results = {
            'observations': self.transmart_client.get_observations(self.json_query),
            'tree_nodes': self.transmart_client.get_tree_nodes(depth=0, tags=True),
            # TODO Add other api queries that are needed
        }
        self.output_tables = [
            PatientDimension,
            ConceptDimension,
            I2b2Secure,
            # TODO add remaining tm_copy staging files
        ]

    def run(self) -> None:
        """
        Construct and write all transmart-copy staging files based on the input query
        :return: None
        """
        for tm_copy_table in self.output_tables:
            table = tm_copy_table(self.query_results)
            df = table.build_transmart_copy_df()
            table.write_to_file(df, self.output_root_dir)
        logging.info('Done.')

    def create_output_dirs(self) -> None:
        i2b2demodata_dir = self.output_root_dir / 'i2b2demodata'
        i2b2metadata_dir = self.output_root_dir / 'i2b2metadata'
        i2b2demodata_dir.mkdir(parents=True, exist_ok=True)
        i2b2metadata_dir.mkdir(parents=True, exist_ok=True)
