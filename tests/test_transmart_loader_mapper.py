#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the transmart query results to transmart-loader mappers.
"""
import pytest
from transmart_loader.copy_writer import format_date
from transmart_loader.transmart import ValueType, DimensionType, StudyNode, ConceptNode, TreeNode

from dicer.query_results import QueryResults
from dicer.mappers.transmart_loader_mapper import TransmartLoaderMapper
from dicer.transmart_rest_client import TransmartRestClient


@pytest.mark.usefixtures('mocked_config', 'mocked_responses')
def test_transmart_loader_mapper(mocked_config, mocked_responses):
    api = TransmartRestClient(mocked_config)
    constraint = {'type': 'true'}
    test_query_result = QueryResults(
        api.get_observations(constraint),
        api.get_tree_nodes(),
        api.get_dimensions(),
        api.get_studies(),
        api.get_relation_types(),
        api.get_relations()
    )

    mapper = TransmartLoaderMapper()
    qr_collection = mapper.map_query_results(test_query_result)

    # PATIENTS
    assert len(qr_collection.patients) == 2
    assert qr_collection.patients[0].identifier == 'CV:40'
    assert qr_collection.patients[0].sex == 'female'
    assert len(qr_collection.patients[0].mappings) == 1
    assert qr_collection.patients[0].mappings[0].source == 'SUBJ_ID'
    assert qr_collection.patients[0].mappings[0].identifier == 'CV:40'
    assert qr_collection.patients[1].identifier == 'CV:12'
    assert qr_collection.patients[1].sex == 'male'
    assert len(qr_collection.patients[1].mappings) == 1
    assert qr_collection.patients[1].mappings[0].source == 'SUBJ_ID'
    assert qr_collection.patients[1].mappings[0].identifier == 'CV:12'

    # CONCEPTS
    assert len(qr_collection.concepts) == 3
    assert list(map(lambda c: c.concept_code, qr_collection.concepts)) == ['CV:DEM:AGE', 'CV:DEM:RACE', 'CV:DEM:SEX:F']
    assert list(map(lambda c: c.name, qr_collection.concepts)) == ['Age', 'Race', 'Female']
    assert list(map(lambda c: c.concept_path, qr_collection.concepts)) == [
        '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Age\\',
        '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Race\\',
        '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Gender\\Female\\']
    assert qr_collection.concepts[0].value_type == ValueType.Numeric
    assert qr_collection.concepts[1].value_type == ValueType.Categorical
    assert qr_collection.concepts[2].value_type == ValueType.Categorical

    # MODIFIERS
    assert len(qr_collection.modifiers) == 3
    assert list(map(lambda m: m.modifier_code, qr_collection.modifiers)) == [
        'CSR_DIAGNOSIS_MOD', 'CSR_BIOMATERIAL_MOD', 'CSR_BIOSOURCE_MOD']
    assert list(map(lambda m: m.name, qr_collection.modifiers)) == [
        'Diagnosis ID', 'Biomaterial ID', 'Biosource ID']
    assert list(map(lambda m: m.modifier_path, qr_collection.modifiers)) == [
        'CSR_DIAGNOSIS_MOD', 'CSR_BIOMATERIAL_MOD', 'CSR_BIOSOURCE_MOD']
    assert list(map(lambda m: m.value_type, qr_collection.modifiers)) == [
            ValueType.Categorical, ValueType.Categorical, ValueType.Categorical]

    # DIMENSIONS
    assert len(qr_collection.dimensions) == 10
    assert list(map(lambda d: d.name, qr_collection.dimensions)) == [
        'study', 'patient', 'concept', 'trial visit', 'start time', 'visit', 'end time',
        'Diagnosis ID', 'Biomaterial ID', 'Biosource ID']
    assert list(map(lambda d: d.modifier.name if d.modifier else None, qr_collection.dimensions)) == [
        None, None, None, None, None, None, None,
        'Diagnosis ID', 'Biomaterial ID', 'Biosource ID']
    assert list(map(lambda d: d.dimension_type, qr_collection.dimensions)) == [
        DimensionType.Attribute, DimensionType.Subject, DimensionType.Attribute, DimensionType.Attribute,
        DimensionType.Attribute,DimensionType.Attribute,DimensionType.Attribute,
        DimensionType.Subject,DimensionType.Subject,DimensionType.Subject]
    assert list(map(lambda d: d.sort_index, qr_collection.dimensions)) == [
        None, 1, None, None, None, None, None, 2, 4, 3]

    # STUDIES
    assert len(qr_collection.studies) == 1
    assert qr_collection.studies[0].name == 'CATEGORICAL_VALUES'
    assert qr_collection.studies[0].study_id == 'CATEGORICAL_VALUES'

    # TRIAL VISITS
    assert len(qr_collection.trial_visits) == 1
    assert qr_collection.trial_visits[0].study.name == 'CATEGORICAL_VALUES'
    assert qr_collection.trial_visits[0].rel_time_unit is None
    assert qr_collection.trial_visits[0].rel_time_label == '1'
    assert qr_collection.trial_visits[0].rel_time is None

    # VISITS
    assert len(qr_collection.visits) == 1
    assert qr_collection.visits[0].patient.identifier == 'CV:40'
    assert qr_collection.visits[0].identifier == 'EHR:62:1'
    assert qr_collection.visits[0].active_status is None
    assert format_date(qr_collection.visits[0].start_date) == '2016-03-29 09:00:00'
    assert format_date(qr_collection.visits[0].end_date) == '2016-03-29 11:00:00'
    assert qr_collection.visits[0].inout is None
    assert qr_collection.visits[0].location is None
    assert qr_collection.visits[0].mappings[0].source == 'VISIT_ID'
    assert qr_collection.visits[0].mappings[0].identifier == 'EHR:62:1'

    # ONTOLOGY
    assert len(qr_collection.ontology) == 1
    assert isinstance(qr_collection.ontology[0], StudyNode)
    assert qr_collection.ontology[0].name == 'CATEGORICAL_VALUES'
    assert qr_collection.ontology[0].study.study_id == 'CATEGORICAL_VALUES'
    assert len(qr_collection.ontology[0].children) == 1
    assert qr_collection.ontology[0].children[0].name == 'Demography'
    assert len(qr_collection.ontology[0].children[0].children) == 3
    assert qr_collection.ontology[0].children[0].children[0].name == 'Age'
    assert isinstance(qr_collection.ontology[0].children[0].children[0], ConceptNode)
    assert qr_collection.ontology[0].children[0].children[0].concept.concept_code == 'CV:DEM:AGE'
    assert isinstance(qr_collection.ontology[0].children[0].children[1], TreeNode)
    assert qr_collection.ontology[0].children[0].children[1].name == 'Gender'
    assert len(qr_collection.ontology[0].children[0].children[1].children) == 1
    assert qr_collection.ontology[0].children[0].children[1].children[0].name == 'Female'
    assert isinstance(qr_collection.ontology[0].children[0].children[1].children[0], ConceptNode)
    assert qr_collection.ontology[0].children[0].children[1].children[0].concept.concept_code == 'CV:DEM:SEX:F'
    assert qr_collection.ontology[0].children[0].children[2].name == 'Race'
    assert isinstance(qr_collection.ontology[0].children[0].children[2], ConceptNode)
    assert qr_collection.ontology[0].children[0].children[2].concept.concept_code == 'CV:DEM:RACE'

    # OBSERVATIONS
    assert len(qr_collection.observations) == 3
    assert list(map(lambda o: o.patient.identifier, qr_collection.observations)) == [
        'CV:12', 'CV:40', 'CV:40']
    assert list(map(lambda o: o.concept.concept_code, qr_collection.observations)) == [
        'CV:DEM:AGE', 'CV:DEM:RACE', 'CV:DEM:SEX:F']
    assert list(map(lambda o: o.visit.identifier if o.visit else None, qr_collection.observations)) == [
        'EHR:62:1', None, None]
    assert list(map(lambda o: o.trial_visit.rel_time_label, qr_collection.observations)) == ['1', '1', '1']
    assert list(map(lambda o: o.trial_visit.study.study_id, qr_collection.observations)) == [
        'CATEGORICAL_VALUES', 'CATEGORICAL_VALUES', 'CATEGORICAL_VALUES']
    assert list(map(lambda o: o.start_date, qr_collection.observations)) == [
        '2019-05-05 11:11:11', '2019-07-22 12:00:00', None]
    assert list(map(lambda o: o.end_date, qr_collection.observations)) == [
        '2019-07-05 11:11:11', None, None]
    assert list(map(lambda o: o.value.value, qr_collection.observations)) == [
        20, 'Caucasian', 'Female']
    assert list(map(lambda o: o.value.value_type, qr_collection.observations)) == [
        ValueType.Numeric, ValueType.Categorical, ValueType.Categorical]
    assert len(qr_collection.observations[0].metadata.values) == 1
    assert qr_collection.observations[0].metadata.values.get(qr_collection.modifiers[0]).value == 'D1'
    assert qr_collection.observations[1].metadata is None
    assert qr_collection.observations[2].metadata is None

    # RELATION TYPES
    assert len(qr_collection.relation_types) == 7
    assert list(map(lambda rt: rt.label, qr_collection.relation_types)) == [
        'PAR', 'SPO', 'SIB', 'MZ', 'DZ', 'COT', 'CHI']
    assert list(map(lambda rt: rt.description, qr_collection.relation_types)) == [
        'Parent', 'Spouse', 'Sibling', 'Monozygotic twin', 'Dizygotic twin', 'Twin with unknown zygosity', 'Child']
    assert list(map(lambda rt: rt.symmetrical, qr_collection.relation_types)) == [
        False, True, True, True, True, True, False]
    assert list(map(lambda rt: rt.biological, qr_collection.relation_types)) == [
        False, False, False, True, True, True, False]

    # RELATIONS
    assert len(qr_collection.relations) == 1
    assert qr_collection.relations[0].left.identifier == 'CV:40'
    assert qr_collection.relations[0].right.identifier == 'CV:12'
    assert qr_collection.relations[0].relation_type.label == 'SPO'
    assert qr_collection.relations[0].biological is False
    assert qr_collection.relations[0].share_household is False



