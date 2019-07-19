from typing import List

from transmart_loader.console import Console
from transmart_loader.transmart import Concept, TreeNode, StudyNode, Study, ConceptNode

from dicer.mappers.mapper_helper import observed_value_type_to_value_type, DataInconsistencyException
from dicer.transmart import ConceptDimensionElement, Value, TreeNode as TreeNodeObject, ObservedValueType


class OntologyMapper:
    """
    Map concepts and tree nodes from query results to transmart-loader objects
    """

    def __init__(self, studies: List[Study]):
        self.studies = studies
        self.concepts = []

    @staticmethod
    def map_concept(concept: ConceptDimensionElement) -> Concept:
        return Concept(
            concept.conceptCode,
            concept.name,
            concept.conceptPath,
            None
        )

    def map_tree_node(self, tree_node: TreeNodeObject) -> TreeNode:

        if tree_node.type is ObservedValueType.Study:
            study = next(filter(lambda x: x.study_id == tree_node.studyId, self.studies), None)
            if not study:
                # skipping study node
                return None
            node = StudyNode(study)
        elif tree_node.conceptCode:
            concept_id = next(i for i, c in enumerate(self.concepts) if c.concept_code == tree_node.conceptCode)
            self.concepts[concept_id].value_type = observed_value_type_to_value_type(tree_node.type)
            node = ConceptNode(self.concepts[concept_id])
        else:
            node = TreeNode(tree_node.name)

        for child in tree_node.children:
            try:
                child_node = self.map_tree_node(TreeNodeObject(**child))
                node.add_child(child_node)
            except Exception as e:
                Console.info('Tree node mapping error: {}'. format(e))

        return node

    def map_concepts(self, concepts_dim_elements: List[Value]) -> List[Concept]:
        self.concepts = list(map(lambda x: self.map_concept(ConceptDimensionElement(**x)), concepts_dim_elements))
        return self.concepts

    def map_tree_nodes(self, tree_node_objects: List[TreeNodeObject]):
        tree_nodes = []
        for node_object in tree_node_objects:
            node = self.map_tree_node(node_object)
            if node:
                tree_nodes.append(node)
        return tree_nodes
