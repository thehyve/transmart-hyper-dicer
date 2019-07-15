#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the tranSMART REST API client.
"""
import pytest

from dicer.transmart import Hypercube
from dicer.transmart_rest_client import TransmartRestClient


@pytest.mark.usefixtures('mocked_config', 'mocked_responses')
def test_get_observations(mocked_config, mocked_responses):
    constraint = {'type': 'true'}
    api = TransmartRestClient(mocked_config)
    response: Hypercube = api.get_observations(constraint)
    dimension_declaration = response.dimensionDeclarations
    cells = response.cells
    dimension_elements = response.dimensionElements
    assert len(dimension_declaration) == 11
    assert len(cells) == 3
    assert len(dimension_elements) == 8
