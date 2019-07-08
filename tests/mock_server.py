import json
import socket
import time
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import requests
from functools import wraps

from dicer.keycloak_rest_client import KeycloakRestClient
from dicer.transmart_rest_client import TransmartRestClient
from tests.mock_responses import GET_JSON_RESPONSES, POST_JSON_RESPONSES


class MockServerRequestHandler(BaseHTTPRequestHandler):

    def general(self, data):

        # Process an HTTP GET request and return a response with an HTTP 200 status.
        self.send_response(requests.codes.ok)

        # Add response headers.
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()

        # Add response content.
        handle = self.path.split('?')[0]
        response_content = json.dumps(data[handle])
        self.wfile.write(response_content.encode('utf-8'))

    def do_GET(self):
        self.general(GET_JSON_RESPONSES)
        return

    def do_POST(self):
        self.general(POST_JSON_RESPONSES)
        return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('', 0))
    address, port = s.getsockname()
    s.close()
    return port


class TestServer(HTTPServer):
    def shutdown(self):
        self.socket.close()
        super().shutdown()


def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(1, 5):
            try:
                return func(*args, **kwargs)

            except requests.exceptions.ChunkedEncodingError:
                print('Failed connection: waiting and retrying.')
                time.sleep(i / 4)
    return wrapper


def get_client(host, port):
    client = TransmartRestClient()
    client.url = 'http://{}:{}'.format(host, port)
    client.verify = False
    keycloak = KeycloakRestClient()
    keycloak.url = '{}/auth/realms/test'.format(client.url)
    keycloak.client_id = "client_id"
    keycloak.offline_token = "offline_token"
    client.keycloak = keycloak
    return client


class TestMockServer(unittest.TestCase):
    """
    Server that mocks both tranSMART and Keycloak.
    To simplify testing, it assumes tranSMART and Keycloak have the same URL, so only one mock server is required.
    """
    interactive = False
    version = 2

    @classmethod
    def setUpClass(cls):
        cls.host = 'localhost'

        cls.mock_server_port = get_free_port()
        # Configure mock server.
        cls.mock_server = TestServer((cls.host, cls.mock_server_port), MockServerRequestHandler)

        # Start running mock server in a separate thread.
        # Daemon threads automatically shut down when the main process exits.
        cls.mock_server_thread = Thread(target=cls.mock_server.serve_forever)
        cls.mock_server_thread.setDaemon(True)
        cls.mock_server_thread.start()

        time.sleep(2)

        start = lambda: get_client(cls.host, cls.mock_server_port)
        cls.api = retry(start)()

    @classmethod
    def tearDownClass(cls):
        cls.mock_server.shutdown()
