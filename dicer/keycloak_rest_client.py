import requests
from pydantic import BaseModel


class KeycloakException(Exception):
    pass


class KeycloakConfiguration(BaseModel):
    url: str
    client_id: str
    offline_token: str


class KeycloakRestClient(object):

    def __init__(self, config: KeycloakConfiguration):
        self.token = None
        self.config = config

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
        url = self.config.url + '/protocol/openid-connect/token'
        params = {
            'grant_type': 'refresh_token',
            'scope': 'offline_access',
            'client_id': self.config.client_id,
            'refresh_token': self.config.offline_token
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
