from collections import Sequence
from typing import List

from dicer.query_results import QueryResults
from dicer.transmart \
    import ConceptDimensionElement, PatientDimensionElement, RelationType as RelationTypeObject, \
    Dimension as DimensionObject
from transmart_loader.transmart import Concept, ValueType, Patient, RelationType, IdentifierMapping, DataCollection, \
    Dimension, Modifier


class DataInconsistencyException(Exception):
    pass


def map_concept(concept_dimension_element: ConceptDimensionElement) -> Concept:
    return Concept(
        concept_dimension_element.conceptCode,
        concept_dimension_element.name,
        concept_dimension_element.conceptPath,
        ValueType.Categorical
    )


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


def map_dimension(dimension: DimensionObject, modifiers: List[Modifier]) -> Dimension:
    modifier = next(filter(lambda x: x.modifier_code == dimension.name,  modifiers))
    return Dimension(
        dimension.name,
        modifier,
        dimension.dimensionType,
        dimension.sortIndex
    )


def map_query_results(query_results: QueryResults) -> DataCollection:
    patient_dim_elements = query_results.observations.dimensionElements['patient']
    patients = list(map(lambda x: map_patient(PatientDimensionElement(**x)), patient_dim_elements))

    modifiers: List[Modifier] = []

    dimension_elements = query_results.dimensions.dimensions
    dimensions = list(map(lambda x: map_dimension(x, modifiers), dimension_elements))

    concepts = []
    studies = []
    trial_visits = []
    visits = []
    ontology = []
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

