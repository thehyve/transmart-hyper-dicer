#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from dicer.transmart_rest_client import TransmartRestClient
from tests.mock_server import retry, TestMockServer


class TransmartRestClientTestCase(TestMockServer):
    """Tests for the tranSMART REST API client.
    """

    @retry
    def test_get_api(self):
        assert isinstance(self.api, TransmartRestClient)

    @retry
    def test_get_observations(self):
        constraint = {'type': 'true'}
        response = self.api.get_observations(constraint)
        dimension_declaration = response.get('dimensionDeclarations')
        cells = response.get('cells')
        dimension_elements = response.get('dimensionElements')
        self.assertEqual(11, len(dimension_declaration))
        self.assertEqual(3, len(cells))
        self.assertEqual(8, len(dimension_elements))


if __name__ == '__main__':
    unittest.main()
