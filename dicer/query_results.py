from dicer.transmart import Hypercube, TreeNodes, Dimensions, Studies, RelationTypes, Relations


class QueryResults:
    def __init__(self,
                 observations: Hypercube,
                 tree_nodes: TreeNodes,
                 dimensions: Dimensions,
                 studies: Studies,
                 relation_types: RelationTypes,
                 relations: Relations):
        self.observations = observations
        self.tree_nodes = tree_nodes
        self.dimensions = dimensions
        self.studies = studies
        self.relation_types = relation_types
        self.relations = relations
