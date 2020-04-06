import urllib.parse

import flask.testing
import requests


class JsonApiConnector:
    def make_json_request(self, method :str, endpoint :str, json_payload=None):
        raise NotImplementedError("This function must be overridden by a subclass")


class RequestsJsonApiConnector(JsonApiConnector):
    _server_url       :str
    _requests_session :requests.Session

    def __init__(self, server_url :str, requests_session :requests.Session = None):
        if requests_session is None:
            requests_session = requests.Session()

        self._server_url = server_url
        self._requests_session = requests_session

    def make_json_request(self, method :str, endpoint :str, json_payload=None):
        endpoint_url = urllib.parse.urljoin(self._server_url, endpoint)

        response = self._requests_session.request(method, endpoint_url, json=json_payload)
        response.raise_for_status()

        return response.json()


class FlaskTestClientJsonApiConnector:
    app_test_client: flask.testing.FlaskClient

    class ServerError(Exception):
        pass

    def __init__(self, app_test_client :flask.testing.FlaskClient):
        self.app_test_client :flask.testing.FlaskClient = app_test_client

    def make_json_request(
        self,
        method :str,
        endpoint :str,
        json_payload=None,
    ):
        response = self.app_test_client.open(endpoint, method=method, json=json_payload)

        if response.status_code != 200:
            raise self.ServerError(f"Application responded with status code {response.status_code}")

        return response.get_json()
