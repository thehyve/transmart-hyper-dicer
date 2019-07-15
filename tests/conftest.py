import json
import pytest
import responses

from dicer.keycloak_rest_client import KeycloakConfiguration
from dicer.transmart_rest_client import TransmartConfiguration
from tests.mock_responses import POST_JSON_RESPONSES, GET_JSON_RESPONSES


@pytest.fixture
def mocked_config() -> TransmartConfiguration:
    return TransmartConfiguration(
        url='https://example.com',
        keycloak_config=KeycloakConfiguration(
            url='https://example.com/auth/realms/test',
            client_id='transmart-client',
            offline_token='dummy token'
        )
    )


@pytest.fixture
def mocked_responses():
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
        yield rsps
