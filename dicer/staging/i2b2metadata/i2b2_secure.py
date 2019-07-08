import logging

import pandas as pd
from pandas import DataFrame

from dicer.query_results import QueryResults
from dicer.staging.tm_copy_staging_table import TmCopyStagingTable


class I2b2Secure(TmCopyStagingTable):
    out_file_name = 'i2b2_secure.tsv'
    col_rename_dict = {'conceptCode': 'concept_cd',
                       'conceptPath': 'concept_path',
                       'name': 'name_char'}

    def __init__(self, query_results: QueryResults):
        self.query_results = query_results

    def build_transmart_copy_df(self) -> DataFrame:
        logging.info('Creating i2b2_secure df')

        concept_codes = self.get_concept_codes()
        selected_tree_nodes = self.filter_tree_nodes(concept_codes)
        i2b2_secure_df = pd.DataFrame(list(selected_tree_nodes.values()))

        # TODO add all missing columns that can be inferred from the current df
        # concepts_df = pd.DataFrame(json_observations['dimensionElements']['concept'])
        # concepts_df.rename(columns=self.col_rename_dict, inplace=True)
        return i2b2_secure_df

    def filter_tree_nodes(self, concept_codes: set):

        def parse_tree(node: dict, parents: list, concept_codes: set, selected_tree_nodes: dict) -> dict:
            parents = parents.copy()
            node_minus_children_property = {k: v for k, v in node.items() if k != 'children'}
            parents.append(node_minus_children_property)
            concept_code = node.get('conceptCode', None)
            if concept_code is not None and concept_code in concept_codes:
                for p_node in parents:
                    selected_tree_nodes[p_node['fullName']] = p_node
            for child_node in node.get('children', []):
                parse_tree(child_node, parents, concept_codes, selected_tree_nodes)
            return selected_tree_nodes

        tree_root = self.query_results.tree_nodes['tree_nodes'][0]
        selected_tree_nodes = parse_tree(node=tree_root, parents=[], concept_codes=concept_codes, selected_tree_nodes={})
        print(selected_tree_nodes)
        return selected_tree_nodes

    def get_concept_codes(self) -> set:
        """
        Get every concept code that was returned by the observations query
        :return: concept code set
        """
        hypercube = self.query_results.observations
        return {c['conceptCode'] for c in hypercube.dimensionElements['concept']}
