#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the tranSMART REST API client.
"""
import pytest

from dicer.transmart import Hypercube, TreeNodes, TreeNode, Dimensions, Studies, Relations, RelationTypes
from dicer.transmart_rest_client import TransmartRestClient


@pytest.mark.usefixtures('mocked_config', 'mocked_responses')
def test_get_observations(mocked_config, mocked_responses):
    constraint = {'type': 'true'}
    api = TransmartRestClient(mocked_config)
    response: Hypercube = api.get_observations(constraint)
    dimension_declaration = response.dimensionDeclarations
    cells = response.cells
    dimension_elements = response.dimensionElements
    assert len(dimension_declaration) == 12
    assert len(cells) == 3
    assert len(dimension_elements) == 9


@pytest.mark.usefixtures('mocked_config', 'mocked_responses')
def test_get_tree_nodes(mocked_config, mocked_responses):
    api = TransmartRestClient(mocked_config)
    response: TreeNodes = api.get_tree_nodes()
    assert len(response.tree_nodes) == 1
    assert len(response.tree_nodes[0].children) == 1
    assert len(TreeNode(**response.tree_nodes[0].children[0]).children) == 3


@pytest.mark.usefixtures('mocked_config', 'mocked_responses')
def test_get_dimensions(mocked_config, mocked_responses):
    api = TransmartRestClient(mocked_config)
    response: Dimensions = api.get_dimensions()
    assert len(response.dimensions) == 10


@pytest.mark.usefixtures('mocked_config', 'mocked_responses')
def test_get_studies(mocked_config, mocked_responses):
    api = TransmartRestClient(mocked_config)
    response: Studies = api.get_studies()
    assert len(response.studies) == 1


@pytest.mark.usefixtures('mocked_config', 'mocked_responses')
def test_get_relations(mocked_config, mocked_responses):
    api = TransmartRestClient(mocked_config)
    response: Relations = api.get_relations()
    assert len(response.relations) == 1


@pytest.mark.usefixtures('mocked_config', 'mocked_responses')
def test_get_relation_types(mocked_config, mocked_responses):
    api = TransmartRestClient(mocked_config)
    response: RelationTypes = api.get_relation_types()
    assert len(response.relationTypes) == 7
