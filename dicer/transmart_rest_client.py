import requests
import logging

from dicer.transmart import Hypercube
from .keycloak_rest_client import KeycloakRestClient

from .config import transmart_config


class TransmartException(Exception):
    pass


class TransmartRestClient(object):

    def __init__(self):
        self.url = transmart_config.get("host")
        self.verify = transmart_config.get("verify_cert")
        self.keycloak = KeycloakRestClient()

    def get_observations(self, constraint: dict) -> Hypercube:
        """
        Get observations call
        :param constraint: transmart API constraint to request
        :return: The Hypercube response of the observations call of the transmart API
        """
        path = '/v2/observations'
        body = {'type': 'clinical', 'constraint': constraint}
        response: dict = self.post(path, body)
        return Hypercube(**response)

    def get_tree_nodes(self, depth=0, tags=True, counts=False):
        """
        Get tree nodes call
        :param depth: maximum tree node depth
        :param tags: include metadata tags
        :param counts: include counts
        :return: response body (json) of the tree nodes call of the transmart API
        """
        path = '/v2/tree_nodes'
        return self.get(path, depth=depth, tags=tags, counts=counts)

    def get_headers(self):
        token = self.keycloak.get_token()
        return {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + str(token)
        }

    def get_response_json(self, response: requests.Response):
        """
        Handle the server's response to an HTTP request
        :param response: server's response
        :return: json-encoded content of a response, if any
        """
        if response.status_code == 401:
            logging.error('Request failed. Unauthorized.')
            raise TransmartException()
        if response.status_code not in [200, 201]:
            logging.error(f'Request failed. Error occurred. Response status {response.status_code}')
            raise TransmartException()
        return response.json()

    def get(self, path: str, **kwargs):
        """
        GET call to the tranSMART server.
        :param path: the API path to call.
        :return: the response.
        """
        url = f'{self.url}{path}'
        logging.info('Making a GET call to: %s' % url)
        r = requests.get(url=url,
                         params=kwargs,
                         headers=self.get_headers(),
                         verify=self.verify)
        return self.get_response_json(r)

    def post(self, path: str, body=None):
        """
        POST call to the tranSMART server.
        :param body: request body in json format
        :param path: the API path to call
        :return: the response.
        """
        url = f'{self.url}{path}'
        logging.info('Making a POST call to: %s' % url)
        r = requests.post(url=url,
                          json=body,
                          headers=self.get_headers(),
                          verify=self.verify)
        return self.get_response_json(r)
