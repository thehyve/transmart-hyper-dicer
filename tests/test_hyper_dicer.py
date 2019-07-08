#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the hyper_dicer tool.
"""
import json
from os import path
from pathlib import Path
import pytest
import responses

from dicer.config import keycloak_config, transmart_config
from dicer.hyper_dicer import HyperDicer
from tests.mock_responses import POST_JSON_RESPONSES, GET_JSON_RESPONSES


@pytest.fixture
def mocked_responses():
    keycloak_config['oidc_server_url'] = 'https://example.com/auth/realms/test'
    transmart_config['host'] = 'https://example.com'
    with responses.RequestsMock() as rsps:
        for url_path, mock_response in POST_JSON_RESPONSES.items():
            rsps.add(responses.POST, "https://example.com{}".format(url_path),
                     body=json.dumps(mock_response),
                     status=200,
                     content_type='application/json')
        for url_path, mock_response in GET_JSON_RESPONSES.items():
            rsps.add(responses.GET, "https://example.com{}".format(url_path),
                     body=json.dumps(mock_response),
                     status=200,
                     content_type='application/json')
        yield rsps


def test_hyper_dicer(tmp_path, mocked_responses):
    hyper_dicer = HyperDicer(Path('./tests/test_query.json'), tmp_path)
    hyper_dicer.run()
    target_path = tmp_path.as_posix()
    assert path.exists(target_path + '/i2b2metadata/i2b2_secure.tsv')
    assert path.exists(target_path + '/i2b2demodata/concept_dimension.tsv')
    assert path.exists(target_path + '/i2b2demodata/patient_dimension.tsv')
