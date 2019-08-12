from typing import List, Optional, Dict

from transmart_loader.transmart import Concept as TLConcept, TreeNode as TLTreeNode, StudyNode as TLStudyNode, \
    Study as TLStudy, ConceptNode as TLConceptNode, TreeNodeMetadata

from dicer.mappers.mapper_helper import observed_value_type_to_value_type
from dicer.transmart import ConceptDimensionElement, Value, TreeNode, ObservedValueType


class OntologyMapper:
    """
    Map concepts and tree nodes from query results to transmart-loader objects
    """

    def __init__(self, study_id_to_study: Dict[str, TLStudy], concept_dim_elements: List[Value]):
        self.study_id_to_study = study_id_to_study
        self.concept_code_to_concept: Dict[str, TLConcept] = {}
        self.create_concept_to_concept_code_dict(concept_dim_elements)

    def create_concept_to_concept_code_dict(self, concepts_dim_elements: List[Value]):
        for concepts_dim_element in concepts_dim_elements:
            self.map_concept(ConceptDimensionElement(**concepts_dim_element))

    def map_concept(self, concept_dim_element: ConceptDimensionElement):
        concept = TLConcept(
            concept_dim_element.conceptCode,
            concept_dim_element.name,
            concept_dim_element.conceptPath,
            None
        )
        self.concept_code_to_concept[concept_dim_element.conceptCode] = concept

    def map_tree_node_children(self, node: TLTreeNode, tree_node_obj):
        for child in tree_node_obj.children:
            child_node = self.map_tree_node(TreeNode(**child))
            if child_node:
                node.add_child(child_node)

    def map_concept_node(self, tree_node_obj: TreeNode) -> Optional[TLConceptNode]:
        concept = self.concept_code_to_concept.get(tree_node_obj.conceptCode)
        if concept is not None:
            # update concept value type (not available in ConceptDimensionElement)
            concept.value_type = observed_value_type_to_value_type(tree_node_obj.type)
            return TLConceptNode(concept)
        return None

    def map_study_node(self, tree_node_obj: TreeNode) -> Optional[TLStudyNode]:
        study = self.study_id_to_study.get(tree_node_obj.studyId)
        if study:
            return TLStudyNode(study)
        return None

    def map_tree_node(self, tree_node_obj: TreeNode) -> TLTreeNode:
        if tree_node_obj.type is ObservedValueType.Study:
            node = self.map_study_node(tree_node_obj)
        elif tree_node_obj.conceptCode:
            node = self.map_concept_node(tree_node_obj)
        else:
            node = TLTreeNode(tree_node_obj.name)
        if node is not None:
            if tree_node_obj.metadata is not None:
                node.metadata = TreeNodeMetadata(tree_node_obj.metadata)
            self.map_tree_node_children(node, tree_node_obj)
        return node

    def map_tree_nodes(self, tree_node_objects: List[TreeNode]) -> List[TLTreeNode]:
        tree_nodes: List[TLTreeNode] = []
        for node_object in tree_node_objects:
            node = self.map_tree_node(node_object)
            if node is not None:
                tree_nodes.append(node)
        return tree_nodes
