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
class TestTransmartLoaderMapper:

    qr_collection = None

    def setup(self):
        api = TransmartRestClient(self.mocked_config)
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
        self.qr_collection = mapper.map_query_results(test_query_result)

    def test_patients_mapping(self):
        patients = self.qr_collection.patients
        assert len(patients) == 2
        assert patients[0].identifier == 'CV:40'
        assert patients[0].sex == 'female'
        assert len(patients[0].mappings) == 1
        assert patients[0].mappings[0].source == 'SUBJ_ID'
        assert patients[0].mappings[0].identifier == 'CV:40'
        assert patients[1].identifier == 'CV:12'
        assert patients[1].sex == 'male'
        assert len(patients[1].mappings) == 1
        assert patients[1].mappings[0].source == 'SUBJ_ID'
        assert patients[1].mappings[0].identifier == 'CV:12'

    def test_concepts_mapping(self):
        concepts = self.qr_collection.concepts
        assert len(concepts) == 3
        assert list(map(lambda c: c.concept_code, concepts)) == ['CV:DEM:AGE', 'CV:DEM:RACE', 'CV:DEM:SEX:F']
        assert list(map(lambda c: c.name, concepts)) == ['Age', 'Race', 'Female']
        assert list(map(lambda c: c.concept_path, concepts)) == [
            '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Age\\',
            '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Race\\',
            '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Gender\\Female\\']
        assert concepts[0].value_type == ValueType.Numeric
        assert concepts[1].value_type == ValueType.Categorical
        assert concepts[2].value_type == ValueType.Categorical

    def test_modifiers_mapping(self):
        modifiers = self.qr_collection.modifiers
        assert len(modifiers) == 3
        assert list(map(lambda m: m.modifier_code, modifiers)) == [
            'CSR_DIAGNOSIS_MOD', 'CSR_BIOMATERIAL_MOD', 'CSR_BIOSOURCE_MOD']
        assert list(map(lambda m: m.name, modifiers)) == [
            'Diagnosis ID', 'Biomaterial ID', 'Biosource ID']
        assert list(map(lambda m: m.modifier_path, modifiers)) == [
            'CSR_DIAGNOSIS_MOD', 'CSR_BIOMATERIAL_MOD', 'CSR_BIOSOURCE_MOD']
        assert list(map(lambda m: m.value_type, modifiers)) == [
                ValueType.Categorical, ValueType.Categorical, ValueType.Categorical]

    def test_dimensions_mapping(self):
        dimensions = self.qr_collection.dimensions
        assert len(dimensions) == 10
        assert list(map(lambda d: d.name, dimensions)) == [
            'study', 'patient', 'concept', 'trial visit', 'start time', 'visit', 'end time',
            'Diagnosis ID', 'Biomaterial ID', 'Biosource ID']
        assert list(map(lambda d: d.modifier.name if d.modifier else None, dimensions)) == [
            None, None, None, None, None, None, None,
            'Diagnosis ID', 'Biomaterial ID', 'Biosource ID']
        assert list(map(lambda d: d.dimension_type, dimensions)) == [
            DimensionType.Attribute, DimensionType.Subject, DimensionType.Attribute, DimensionType.Attribute,
            DimensionType.Attribute,DimensionType.Attribute,DimensionType.Attribute,
            DimensionType.Subject,DimensionType.Subject,DimensionType.Subject]
        assert list(map(lambda d: d.sort_index, dimensions)) == [
            None, 1, None, None, None, None, None, 2, 4, 3]

    def test_studies_mapping(self):
        studies = self.qr_collection.studies
        assert len(studies) == 1
        assert studies[0].name == 'CATEGORICAL_VALUES'
        assert studies[0].study_id == 'CATEGORICAL_VALUES'

    def test_trial_visits_mapping(self):
        trial_visits = self.qr_collection.trial_visits
        assert len(trial_visits) == 1
        assert trial_visits[0].study.name == 'CATEGORICAL_VALUES'
        assert trial_visits[0].rel_time_unit is None
        assert trial_visits[0].rel_time_label == '1'
        assert trial_visits[0].rel_time is None

    def test_visits_mapping(self):
        visits = self.qr_collection.visits
        assert len(visits) == 1
        assert visits[0].patient.identifier == 'CV:40'
        assert visits[0].identifier == 'EHR:62:1'
        assert visits[0].active_status is None
        assert format_date(visits[0].start_date) == '2016-03-29 09:00:00'
        assert format_date(visits[0].end_date) == '2016-03-29 11:00:00'
        assert visits[0].inout is None
        assert visits[0].location is None
        assert visits[0].mappings[0].source == 'VISIT_ID'
        assert visits[0].mappings[0].identifier == 'EHR:62:1'

    def test_ontology_mapping(self):
        ontology = self.qr_collection.ontology
        assert len(ontology) == 1
        assert isinstance(ontology[0], StudyNode)
        assert ontology[0].name == 'CATEGORICAL_VALUES'
        assert ontology[0].study.study_id == 'CATEGORICAL_VALUES'
        assert len(ontology[0].children) == 1
        assert ontology[0].children[0].name == 'Demography'
        assert len(ontology[0].children[0].children) == 3
        assert ontology[0].children[0].children[0].name == 'Age'
        assert isinstance(ontology[0].children[0].children[0], ConceptNode)
        assert ontology[0].children[0].children[0].concept.concept_code == 'CV:DEM:AGE'
        assert isinstance(ontology[0].children[0].children[1], TreeNode)
        assert ontology[0].children[0].children[1].name == 'Gender'
        assert len(ontology[0].children[0].children[1].children) == 1
        assert ontology[0].children[0].children[1].children[0].name == 'Female'
        assert isinstance(ontology[0].children[0].children[1].children[0], ConceptNode)
        assert ontology[0].children[0].children[1].children[0].concept.concept_code == 'CV:DEM:SEX:F'
        assert ontology[0].children[0].children[2].name == 'Race'
        assert isinstance(ontology[0].children[0].children[2], ConceptNode)
        assert ontology[0].children[0].children[2].concept.concept_code == 'CV:DEM:RACE'

    def test_observations_mapping(self):
        observations = self.qr_collection.observations
        assert len(observations) == 3
        assert list(map(lambda o: o.patient.identifier, observations)) == [
            'CV:12', 'CV:40', 'CV:40']
        assert list(map(lambda o: o.concept.concept_code, observations)) == [
            'CV:DEM:AGE', 'CV:DEM:RACE', 'CV:DEM:SEX:F']
        assert list(map(lambda o: o.visit.identifier if o.visit else None, observations)) == [
            'EHR:62:1', None, None]
        assert list(map(lambda o: o.trial_visit.rel_time_label, observations)) == ['1', '1', '1']
        assert list(map(lambda o: o.trial_visit.study.study_id, observations)) == [
            'CATEGORICAL_VALUES', 'CATEGORICAL_VALUES', 'CATEGORICAL_VALUES']
        assert list(map(lambda o: o.start_date, observations)) == [
            '2019-05-05 11:11:11', '2019-07-22 12:00:00', None]
        assert list(map(lambda o: o.end_date, observations)) == [
            '2019-07-05 11:11:11', None, None]
        assert list(map(lambda o: o.value.value, observations)) == [
            20, 'Caucasian', 'Female']
        assert list(map(lambda o: o.value.value_type, observations)) == [
            ValueType.Numeric, ValueType.Categorical, ValueType.Categorical]
        assert len(observations[0].metadata.values) == 1
        assert observations[0].metadata.values.get(self.qr_collection.modifiers[0]).value == 'D1'
        assert observations[1].metadata is None
        assert observations[2].metadata is None

    def test_relation_types_mapping(self):
        relation_types = self.qr_collection.relation_types
        assert len(relation_types) == 7
        assert list(map(lambda rt: rt.label, relation_types)) == [
            'PAR', 'SPO', 'SIB', 'MZ', 'DZ', 'COT', 'CHI']
        assert list(map(lambda rt: rt.description, relation_types)) == [
            'Parent', 'Spouse', 'Sibling', 'Monozygotic twin', 'Dizygotic twin', 'Twin with unknown zygosity', 'Child']
        assert list(map(lambda rt: rt.symmetrical, relation_types)) == [
            False, True, True, True, True, True, False]
        assert list(map(lambda rt: rt.biological, relation_types)) == [
            False, False, False, True, True, True, False]

    def test_relations_mapping(self):
        relations = self.qr_collection.relations
        assert len(relations) == 1
        assert relations[0].left.identifier == 'CV:40'
        assert relations[0].right.identifier == 'CV:12'
        assert relations[0].relation_type.label == 'SPO'
        assert relations[0].biological is False
        assert relations[0].share_household is False
