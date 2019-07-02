import requests

from .config import keycloak_config


class KeycloakException(Exception):
    pass


class KeycloakRestClient(object):

    def __init__(self):
        self.token = None
        self.url = keycloak_config.get("oidc_server_url")
        self.client_id = keycloak_config.get("client_id")
        self.offline_token = keycloak_config.get("offline_token")

    def get_token(self):
        """
        Returns the access token for accessing the server.
        Retrieves a token from the server, if that has not been done earlier this session.
        :return: the access token.
        """
        if self.token is None:
            self.token = self.retrieve_token()
        return self.token

    def retrieve_token(self):
        """
        Retrieve an access token from Keycloak based on the client_id and the offline token,
        which is stored in the config.
        """
        headers = {'Accept': 'application/json',
                   'Contect-Type': 'application/x-www-form-urlencoded'
                   }
        url = self.url + '/protocol/openid-connect/token'
        params = {
            'grant_type': 'refresh_token',
            'scope': 'offline_access',
            'client_id': self.client_id,
            'refresh_token': self.offline_token
        }
        try:
            response = requests.post(url, params, headers=headers)
            if not response.ok:
                response.raise_for_status()
            data = response.json()
            token = data['access_token']
        except Exception as e:
            raise KeycloakException('Could not retrieve access token for %s: %s' % (url, e))

        return token
