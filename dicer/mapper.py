from typing import List

from dicer.query_results import QueryResults
from dicer.transmart \
    import ConceptDimensionElement, PatientDimensionElement, RelationType as RelationTypeObject, \
    Dimension as DimensionObject, TreeNode as TreeNodeObject, Study as StudyObject
from transmart_loader.transmart import Concept, ValueType, Patient, RelationType, IdentifierMapping, DataCollection, \
    Dimension, Modifier, TreeNode, Study


class DataInconsistencyException(Exception):
    pass


def map_concept(concept_dimension_element: ConceptDimensionElement) -> Concept:
    return Concept(
        concept_dimension_element.conceptCode,
        concept_dimension_element.name,
        concept_dimension_element.conceptPath,
        ValueType.Categorical
    ) # TODO


def map_patient(patient_dimension_element: PatientDimensionElement) -> Patient:
    if not patient_dimension_element.subjectIds or 'SUBJ_ID' not in patient_dimension_element.subjectIds:
        raise DataInconsistencyException
    return Patient(
        patient_dimension_element.subjectIds['SUBJ_ID'],
        patient_dimension_element.sex,
        list(map(lambda kv: IdentifierMapping(kv[0], kv[1]), patient_dimension_element.subjectIds.items()))
    )


def map_relation_type(relation_type: RelationTypeObject) -> RelationType:
    return RelationType(
        relation_type.label,
        relation_type.description,
        relation_type.symmetrical,
        relation_type.biological
    )


def map_modifiers(modifier_dimension: DimensionObject) -> Modifier:
    return Modifier(
        modifier_dimension.modifierCode,
        modifier_dimension.name,
        modifier_dimension.modifierCode,
        modifier_dimension.valueType
    )


def map_dimension(dimension: DimensionObject, modifiers: List[Modifier]) -> Dimension:
    modifier = next(filter(lambda x: x.modifier_code == dimension.name,  modifiers))
    return Dimension(
        dimension.name,
        modifier,
        dimension.dimensionType,
        dimension.sortIndex
    )


def map_tree_node(tree_node: TreeNodeObject) -> TreeNode:
    node = TreeNode(
        tree_node.name
    )
    # TODO recursive mapping
    return node


def map_study(study: StudyObject) -> Study:
    return Study(
        study.studyId,
        study.s
    )


def map_query_results(query_results: QueryResults) -> DataCollection:
    patient_dim_elements = query_results.observations.dimensionElements['patient']
    patients = list(map(lambda x: map_patient(PatientDimensionElement(**x)), patient_dim_elements))

    dimension_objects = query_results.dimensions.dimensions
    modifier_objects =  list(filter(lambda x: x.modifierCode, dimension_objects))
    modifiers = list(map(lambda x: map_modifiers(x), modifier_objects))
    dimensions = list(map(lambda x: map_dimension(x, modifiers), dimension_objects))

    study_objects = query_results.observations.dimensionElements['study']
    all_studies = query_results.studies.studies
    studies = [] # TODO combine

    tree_node_objects = query_results.tree_nodes.tree_nodes
    ontology = list(map(lambda x: map_tree_node(x), tree_node_objects))
    concepts = []

    trial_visits = []
    visits = []
    observations = []

    relation_type_elements = query_results.relation_types.relationTypes
    relation_types = list(map(lambda x: map_relation_type(x), relation_type_elements))

    relations = []

    return DataCollection(concepts,
                          modifiers,
                          dimensions,
                          studies,
                          trial_visits,
                          visits,
                          ontology,
                          patients,
                          observations,
                          relation_types,
                          relations)
