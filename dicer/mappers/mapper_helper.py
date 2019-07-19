from typing import List

from transmart_loader.transmart import ValueType, RelationType, Dimension, Modifier, Study, TrialVisit, \
    CategoricalValue, NumericalValue, Value, DateValue, TextValue, \
    DimensionType

from dicer.transmart import RelationType as RelationTypeObject, \
    Dimension as DimensionObject, Study as StudyObject, TrialVisitDimensionElement, \
    ValueType as ValueTypeObject, ObservedValueType, \
    DimensionType as DimensionTypeObject


class DataInconsistencyException(Exception):
    pass


def dimension_type_object_to_dimension_type(dim_type_obj: DimensionTypeObject) -> DimensionType:
    if dim_type_obj is DimensionTypeObject.Subject:
        return DimensionType.Subject
    elif dim_type_obj is DimensionTypeObject.Attribute:
        return DimensionType.Attribute


def value_type_object_to_value_type(type_obj: ValueTypeObject) -> ValueType:
    if type_obj is ValueTypeObject.String:
        return ValueType.Categorical
    elif type_obj in [ValueTypeObject.Double, ValueTypeObject.Int]:
        return ValueType.Numeric
    elif type_obj is ValueTypeObject.Timestamp:
        return ValueType.Date
    elif type_obj is ValueTypeObject.Map:
        return ValueType.Text #TODO ?


def observed_value_type_to_value_type(obs_value_type: ObservedValueType) -> ValueType:
    if obs_value_type in [ObservedValueType.Categorical, ObservedValueType.CategoricalOption]:
        return ValueType.Categorical
    elif obs_value_type is ObservedValueType.Numeric:
        return ValueType.Numeric
    elif obs_value_type is ObservedValueType.Date:
        return ValueType.Date
    else:
        return ValueType.Text #TODO ?


def value_by_value_type(value, value_type: ValueType) -> Value:
    if value_type is ValueType.Categorical:
        return CategoricalValue(value)
    elif value_type is ValueType.Numeric:
        return NumericalValue(value)
    elif value_type is ValueType.Date:
        return DateValue(value)
    elif value_type is ValueType.Text:
        return TextValue(value)


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
        value_type_object_to_value_type(modifier_dimension.valueType)
    )


def map_dimension(dimension: DimensionObject, modifiers: List[Modifier]) -> Dimension:
    modifier = next(filter(lambda x: x.modifier_code == dimension.modifierCode,  modifiers), None)
    return Dimension(
        dimension.name,
        modifier,
        dimension_type_object_to_dimension_type(dimension.dimensionType),
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


def map_study(study: StudyObject) -> Study:
    return Study(
        study.studyId,
        study.studyId
    )
