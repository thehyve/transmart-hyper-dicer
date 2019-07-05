import logging

import pandas as pd
from pandas import DataFrame

from dicer.staging.tm_copy_staging_table import TmCopyStagingTable


class ConceptDimension(TmCopyStagingTable):
    out_file_name = 'concept_dimension.tsv'
    col_rename_dict = {'conceptCode': 'concept_cd',
                       'conceptPath': 'concept_path',
                       'name': 'name_char'}

    def __init__(self, query_results: dict):
        self.query_results = query_results

    def build_transmart_copy_df(self) -> DataFrame:
        logging.info('Creating concept dimension df')
        json_observations = self.query_results['observations']
        concepts_df = pd.DataFrame(json_observations['dimensionElements']['concept'])
        concepts_df.rename(columns=self.col_rename_dict, inplace=True)
        return concepts_df
