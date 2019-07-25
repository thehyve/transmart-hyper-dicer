import json

import pytest
import responses

from dicer.keycloak_rest_client import KeycloakConfiguration
from dicer.transmart_rest_client import TransmartConfiguration
from tests.mock_responses import POST_JSON_RESPONSES, GET_JSON_RESPONSES


@pytest.fixture(scope='class')
def mocked_config(request) -> TransmartConfiguration:
    mocked_config = TransmartConfiguration(
        url='https://example.com',
        keycloak_config=KeycloakConfiguration(
            url='https://example.com/auth/realms/test',
            client_id='transmart-client',
            offline_token='dummy token'
        )
    )
    if request.cls is not None:
        request.cls.mocked_config = mocked_config
    return mocked_config


@pytest.fixture(scope='class')
def mocked_responses(request):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
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
        if request.cls is not None:
            request.cls.mocked_responses = rsps
        yield rsps
