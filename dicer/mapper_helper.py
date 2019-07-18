from typing import List

from dicer.transmart \
    import ConceptDimensionElement, TreeNode as TreeNodeObject, PatientDimensionElement, \
    RelationType as RelationTypeObject, Relation as RelationObject, \
    Dimension as DimensionObject, Study as StudyObject, TrialVisitDimensionElement, \
    VisitDimensionElement, Hypercube, DimensionDeclaration, ValueType as ValueTypeObject, VisualAttributes, \
    ObservedValueType
from transmart_loader.transmart import Concept, ValueType, Patient, RelationType, IdentifierMapping, \
    Dimension, Modifier, TreeNode, Study, TrialVisit, Relation, Visit, Observation, ObservationMetadata, \
    CategoricalValue, NumericalValue, Value, DateValue, TextValue, StudyNode, ConceptNode


class DataInconsistencyException(Exception):
    pass


def get_id_by_dimension_name(inline_dimensions: List[DimensionDeclaration], name: str):
    return next(i for i, dim in enumerate(inline_dimensions) if dim.name == name)


def map_value_type(type_obj: ValueTypeObject) -> ValueType:
    if type_obj.String:
        return ValueType.Categorical
    elif type_obj.Double or type_obj.Int:
        return ValueType.Numeric
    elif type_obj.Timestamp:
        return ValueType.Date
    elif type_obj.Map:
        return ValueType.Text #TODO ?


def value_by_value_type(value, type: ValueType) -> Value:
    if type is ValueType.Categorical:
        return CategoricalValue(value)
    elif type is ValueType.Numeric:
        return NumericalValue(value)
    elif type is ValueType.Date:
        return DateValue(value)
    elif type is ValueType.Text:
        return TextValue(value)


def map_concept(concept: ConceptDimensionElement) -> Concept:
    return Concept(
        concept.conceptCode,
        concept.name,
        concept.conceptPath,
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


def map_relation(relation: RelationObject, patients: List[Patient], relation_types: List[RelationType]) -> Relation:
    left = next((x for x in patients if x.identifier == relation.leftSubjectId))
    right = next((x for x in patients if x.identifier == relation.rightSubjectId))
    relation_type = next((x for x in relation_types if x.label == relation.relationTypeLabel))

    return Relation(
        left,
        relation_type,
        right,
        relation.biological,
        relation.shareHousehold
    )


def map_modifiers(modifier_dimension: DimensionObject) -> Modifier:
    return Modifier(
        modifier_dimension.modifierCode,
        modifier_dimension.name,
        modifier_dimension.modifierCode,
        map_value_type(modifier_dimension.valueType)
    )


def map_dimension(dimension: DimensionObject, modifiers: List[Modifier]) -> Dimension:
    modifier = next(filter(lambda x: x.modifier_code == dimension.modifierCode,  modifiers), None)
    return Dimension(
        dimension.name,
        modifier,
        dimension.dimensionType,
        dimension.sortIndex
    )


def map_trial_visit(trial_visit: TrialVisitDimensionElement, studies: List[Study]) -> TrialVisit:
    study = next(filter(lambda x: x.study_id == trial_visit.studyId, studies))
    return TrialVisit(
        study,
        trial_visit.relTimeLabel,
        trial_visit.relTimeUnit,
        trial_visit.relTime
    )


def map_visit(visit: VisitDimensionElement, patients: List[Patient]) -> Visit:
    if not visit.encounterIds or 'VISIT_ID' not in visit.encounterIds:
        raise DataInconsistencyException
    patient = next(filter(lambda x: x.identifier == visit.patientId, patients))
    return Visit(
        patient,
        visit.encounterIds['VISIT_ID'],
        visit.active_status,
        visit.start_date,
        visit.end_date,
        visit.inout,
        visit.location,
        visit.length_of_stay,
        list(map(lambda kv: IdentifierMapping(kv[0], kv[1]), visit.encounterIds.items()))
    )


def map_tree_node(tree_node: TreeNodeObject, studies: List[Study], concepts: List[Concept]) -> TreeNode:
    if tree_node.studyId and tree_node.type is ObservedValueType.Study:
        study = next(filter(lambda x: x.study_id == tree_node.studyId, studies))
        node = StudyNode(study)
    elif tree_node.conceptCode:
        concept = next(filter(lambda x: x.concept_code == tree_node.conceptCode, concepts))
        concept.value_type = tree_node.type
        node = ConceptNode(concept)
    else:
        node = TreeNode(tree_node.name)
    for child in tree_node.children:
        node.add_child(map_tree_node(TreeNodeObject(**child), studies, concepts))
    return node


def map_study(study: StudyObject) -> Study:
    return Study(
        study.studyId,
        study.studyId
    )


def map_observations(hypercube: Hypercube,
                     patients: List[Patient],
                     concepts: List[Concept],
                     visits: List[Visit],
                     trial_visits: List[TrialVisit],
                     modifiers: List[Modifier]) -> List[Observation]:
    observations = []
    inline_dimensions = list(filter(lambda d: d.inline, hypercube.dimensionDeclarations))
    indexed_dimensions = list(filter(lambda d: d not in inline_dimensions, list(hypercube.dimensionDeclarations)))
    modifier_dimensions = list(filter(lambda d: d.modifierCode, list(hypercube.dimensionDeclarations)))

    start_time_dimension_id = get_id_by_dimension_name(inline_dimensions, 'start time')
    end_time_dimension_id = get_id_by_dimension_name(inline_dimensions, 'end time')
    patient_dimension_id = get_id_by_dimension_name(indexed_dimensions, 'patient')
    concept_dimension_id = get_id_by_dimension_name(indexed_dimensions, 'concept')
    visit_dimension_id = get_id_by_dimension_name(indexed_dimensions, 'visit')
    trial_visits_dimension_id = get_id_by_dimension_name(indexed_dimensions, 'trial visit')

    for cell in hypercube.cells:
        patient_dim_element = PatientDimensionElement(
            **hypercube.dimensionElements['patient'][cell.dimensionIndexes[patient_dimension_id]])
        patient = next(filter(lambda x: x.identifier == patient_dim_element.subjectIds['SUBJ_ID'], patients))

        concept_dim_element = ConceptDimensionElement(
            **hypercube.dimensionElements['concept'][cell.dimensionIndexes[concept_dimension_id]])
        concept = next(filter(lambda x: x.concept_code == concept_dim_element.conceptCode, concepts))

        visit = None
        visit_dim_element_id = cell.dimensionIndexes[visit_dimension_id]
        if visit_dim_element_id is not None:
            visit_dim_element = VisitDimensionElement(**hypercube.dimensionElements['visit'][visit_dim_element_id])
            visit = next(filter(lambda x: x.identifier == visit_dim_element.encounterNum, visits))

        trial_visit = None
        trial_visit_dim_element_id = cell.dimensionIndexes[trial_visits_dimension_id]
        if trial_visit_dim_element_id is not None:
            trial_visit_dim_element = TrialVisitDimensionElement(
                **hypercube.dimensionElements['trial visit'][trial_visit_dim_element_id])
            trial_visit = next(filter(lambda x:
                                      (x.study.study_id, x.rel_time_label) == (trial_visit_dim_element.studyId,
                                                                               trial_visit_dim_element.relTimeLabel),
                                      trial_visits))

        metadata = None
        for modifier_dim in modifier_dimensions:
            metadata_values = dict()
            modifier_dimension_id = get_id_by_dimension_name(indexed_dimensions, modifier_dim.name)
            modifier_dimension_element_id = cell.dimensionIndexes[modifier_dimension_id]
            if modifier_dimension_element_id is not None:
                modifier = next(filter(lambda x: x.modifier_code == modifier_dim.modifierCode, modifiers))
                modifier_values = hypercube.dimensionElements[modifier_dim.name][modifier_dimension_element_id]
                for v in modifier_values:
                    metadata_values[modifier] = value_by_value_type(v, modifier.value_type)
            metadata = ObservationMetadata(metadata_values)

        value = CategoricalValue(cell.stringValue) if cell.stringValue else NumericalValue(cell.numericValue) #TODO DateValue

        observations.append(Observation(
            patient,
            concept,
            visit,
            trial_visit,
            cell.inlineDimensions[start_time_dimension_id],
            cell.inlineDimensions[end_time_dimension_id],
            value,
            metadata
        ))

    return observations
