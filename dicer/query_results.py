from typing import Any

from dicer.transmart import Hypercube


class QueryResults:
    def __init__(self, observations: Hypercube, tree_nodes: Any):
        self.observations = observations
        self.tree_nodes = tree_nodes
