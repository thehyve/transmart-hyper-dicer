from typing import List, Optional

from transmart_loader.transmart import Concept, TreeNode, StudyNode, Study, ConceptNode

from dicer.mappers.mapper_helper import observed_value_type_to_value_type
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

    def map_tree_node_children(self, node: TreeNode, tree_node_obj):
        for child in tree_node_obj.children:
            child_node = self.map_tree_node(TreeNodeObject(**child))
            if child_node:
                node.add_child(child_node)

    def map_concept_node(self, tree_node_obj: TreeNodeObject) -> Optional[ConceptNode]:
        concept_id = next((i for i, c in enumerate(self.concepts)
                           if c.concept_code == tree_node_obj.conceptCode), None)
        if concept_id is not None:
            self.concepts[concept_id].value_type = observed_value_type_to_value_type(tree_node_obj.type)
            return ConceptNode(self.concepts[concept_id])
        return None

    def map_study_node(self, tree_node_obj: TreeNodeObject) -> Optional[StudyNode]:
        study = next(filter(lambda x: x.study_id == tree_node_obj.studyId, self.studies), None)
        if study:
            return StudyNode(study)
        return None

    def map_tree_node(self, tree_node_obj: TreeNodeObject) -> TreeNode:
        if tree_node_obj.type is ObservedValueType.Study:
            node = self.map_study_node(tree_node_obj)
        elif tree_node_obj.conceptCode:
            node = self.map_concept_node(tree_node_obj)
        else:
            node = TreeNode(tree_node_obj.name)
        if node is not None:
            self.map_tree_node_children(node, tree_node_obj)
        return node

    def map_tree_nodes(self, tree_node_objects: List[TreeNodeObject]):
        tree_nodes = []
        for node_object in tree_node_objects:
            node = self.map_tree_node(node_object)
            if node is not None:
                tree_nodes.append(node)
        return tree_nodes

    def map_concepts(self, concepts_dim_elements: List[Value]) -> List[Concept]:
        self.concepts = list(map(lambda x: self.map_concept(ConceptDimensionElement(**x)), concepts_dim_elements))
        return self.concepts
