import logging

import pandas as pd
from pandas import DataFrame

from dicer.staging.tm_copy_staging_table import TmCopyStagingTable


class PatientDimension(TmCopyStagingTable):
    out_file_name = 'patient_dimension.tsv'
    col_rename_dict = {'age': 'age_in_years_num',
                       'birthDate': 'birth_date',
                       'deathDate': 'death_date',
                       'id': 'patient_num',
                       'maritalStatus': 'marital_status_cd',
                       'race': 'race_cd',
                       'religion': 'religion_cd',
                       'sexCd': 'sex_cd',
                       'trial': 'sourcesystem_cd'
                       }

    cols_to_drop = {'inTrialId', 'subjectIds', 'sex'}

    def __init__(self, query_results: dict):
        self.query_results = query_results

    def build_transmart_copy_df(self) -> DataFrame:
        logging.info('Creating patient dimension df')
        json_observations = self.query_results['observations']
        patients_df = pd.DataFrame(json_observations['dimensionElements']['patient'])
        patients_df.drop(labels=self.cols_to_drop, axis=1, inplace=True)
        patients_df.rename(columns=self.col_rename_dict, inplace=True)
        return patients_df
