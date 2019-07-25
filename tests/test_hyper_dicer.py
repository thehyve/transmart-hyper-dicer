#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the hyper_dicer tool.
"""
from os import path
import pytest

from dicer.hyper_dicer import HyperDicer


@pytest.mark.usefixtures('mocked_config', 'mocked_responses')
def test_hyper_dicer(tmp_path, mocked_config, mocked_responses):
    hyper_dicer = HyperDicer(mocked_config)
    hyper_dicer.copy_slice({'type': 'true'}, tmp_path)
    target_path = tmp_path.as_posix()
    assert path.exists(target_path + '/i2b2metadata/study_dimension_descriptions.tsv')
    assert path.exists(target_path + '/i2b2metadata/dimension_description.tsv')
    assert path.exists(target_path + '/i2b2metadata/i2b2_secure.tsv')
    assert path.exists(target_path + '/i2b2demodata/concept_dimension.tsv')
    assert path.exists(target_path + '/i2b2demodata/encounter_mapping.tsv')
    assert path.exists(target_path + '/i2b2demodata/modifier_dimension.tsv')
    assert path.exists(target_path + '/i2b2demodata/observation_fact.tsv')
    assert path.exists(target_path + '/i2b2demodata/patient_dimension.tsv')
    assert path.exists(target_path + '/i2b2demodata/patient_mapping.tsv')
    assert path.exists(target_path + '/i2b2demodata/relation_types.tsv')
    assert path.exists(target_path + '/i2b2demodata/relations.tsv')
    assert path.exists(target_path + '/i2b2demodata/study.tsv')
    assert path.exists(target_path + '/i2b2demodata/trial_visit_dimension.tsv')
    assert path.exists(target_path + '/i2b2demodata/visit_dimension.tsv')
