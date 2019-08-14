from typing import List, Dict

from transmart_loader.transmart import ValueType as TLValueType, RelationType as TLRelationType, \
    Dimension as TLDimension, Modifier as TLModifier, Study as TLStudy, TrialVisit as TLTrialVisit, \
    CategoricalValue as TLCategoricalValue, NumericalValue as TLNumericalValue, Value as TLValue, \
    DateValue as TLDateValue, TextValue as TLTextValue, DimensionType as TLDimensionType

from dicer.transmart import RelationType, Dimension as DimensionObject, Study, TrialVisitDimensionElement, \
    ValueType, ObservedValueType, DimensionType, StudyDimensionElement, Value


def dimension_type_object_to_dimension_type(dim_type_obj: DimensionType) -> TLDimensionType:
    if dim_type_obj is DimensionType.Subject:
        return TLDimensionType.Subject
    elif dim_type_obj is DimensionType.Attribute:
        return TLDimensionType.Attribute


def value_type_object_to_value_type(type_obj: ValueType) -> TLValueType:
    if type_obj is ValueType.String:
        return TLValueType.Categorical
    elif type_obj in [ValueType.Double, ValueType.Int]:
        return TLValueType.Numeric
    elif type_obj is ValueType.Timestamp:
        return TLValueType.Date
    elif type_obj is ValueType.Map:
        return TLValueType.Text #TODO ?


def observed_value_type_to_value_type(obs_value_type: ObservedValueType) -> TLValueType:
    if obs_value_type in [ObservedValueType.Categorical, ObservedValueType.CategoricalOption]:
        return TLValueType.Categorical
    elif obs_value_type is ObservedValueType.Numeric:
        return TLValueType.Numeric
    elif obs_value_type is ObservedValueType.Date:
        return TLValueType.Date
    else:
        return TLValueType.Text #TODO ?


def value_by_value_type(value, value_type: TLValueType) -> TLValue:
    if value_type is TLValueType.Categorical:
        return TLCategoricalValue(value)
    elif value_type is TLValueType.Numeric:
        return TLNumericalValue(value)
    elif value_type is TLValueType.Date:
        return TLDateValue(value)
    elif value_type is TLValueType.Text:
        return TLTextValue(value)


def map_relation_type(relation_type: RelationType) -> TLRelationType:
    return TLRelationType(
        relation_type.label,
        relation_type.description,
        relation_type.symmetrical,
        relation_type.biological
    )


def map_modifier(modifier_dimension: DimensionObject) -> TLModifier:
    return TLModifier(
        modifier_dimension.modifierCode,
        modifier_dimension.name,
        modifier_dimension.modifierCode,
        value_type_object_to_value_type(modifier_dimension.valueType)
    )


def map_dimension(dimension: DimensionObject, modifiers: List[TLModifier]) -> TLDimension:
    modifier = next(filter(lambda x: x.modifier_code == dimension.modifierCode,  modifiers), None)
    return TLDimension(
        dimension.name,
        modifier,
        dimension_type_object_to_dimension_type(dimension.dimensionType),
        dimension.sortIndex
    )
