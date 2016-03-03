"""
This module contains the BambooAPIClient, used for communicating with the
Bamboo server web service API.
"""

import requests
from requests.auth import HTTPBasicAuth


class BambooAPIClient(object):
    """
    Adapter for Bamboo's web service API.
    """
    # Default host is local
    DEFAULT_HOST = 'http://localhost'
    DEFAULT_PORT = 8085

    # Endpoints
    BUILD_SERVICE = '/rest/api/latest/result'

    @property
    def build_url(self):
        """
        URL to the builds service.
        """
        return '{}:{}{}'.format(self._host, self._port, self.BUILD_SERVICE)

    def __init__(self, host=None, port=None, user=None, password=None):
        """
        Set connection and auth information (if user+password were provided).
        """
        self._host = host or self.DEFAULT_HOST
        self._port = port or self.DEFAULT_PORT
        self._call_params = {}
        if user and password:
            self._call_params['auth'] = HTTPBasicAuth(user, password)

    def _get_response(self, url, queryset=None):
        """
        Make the call to the service with the given queryset and whatever params
        were set initially (auth).
        """
        res = requests.get(url, data=queryset or {}, **self._call_params)
        if res.status_code != 200:
            raise Exception(res.reason)
        return res

    def get_builds(self, project_key=None, expand=False):
        """
        Returns the list of builds set up on the Bamboo server.
        :param project_key: str
        :param expand: boolean
        :return: List
        """

        qs = None
        if expand:
            qs = {'expand': 'results[1:]'}
        url = self.build_url
        if project_key is not None:
            url = "{}/{}".format(url, project_key)

        res = self._get_response(url, qs).json()
        # Yield response
        for result in res['results']['result']:
            yield result
