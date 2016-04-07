"""
This module contains the BambooAPIClient, used for communicating with the
Bamboo server web service API.
"""
import logging

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger()


class BambooAPIClient(object):
    """
    Adapter for Bamboo's web service API.
    """
    # Default host is local
    DEFAULT_HOST = 'http://localhost'
    DEFAULT_PORT = 8085

    # Endpoints
    BUILD_SERVICE = '/rest/api/latest/result'
    DEPLOY_SERVICE = '/rest/api/latest/deploy/project'
    ENVIRONMENT_SERVICE = '/rest/api/latest/deploy/environment/{env_id}/results'

    @property
    def build_url(self):
        """
        URL to the builds service.
        """
        return '{}:{}{}'.format(self._host, self._port, self.BUILD_SERVICE)

    @property
    def deployment_url(self):
        """
        URL to the deployment service.
        """
        return '{}:{}{}'.format(self._host, self._port, self.DEPLOY_SERVICE)

    @property
    def environment_url(self):
        """
        URL to the environment service.
        """
        return '{}:{}{}'.format(self._host, self._port, self.ENVIRONMENT_SERVICE)

    def __init__(self, host=None, port=None, user=None, password=None):
        """
        Set connection and auth information (if user+password were provided).
        """
        self._host = host or self.DEFAULT_HOST
        self._port = port or self.DEFAULT_PORT
        self._call_params = {}
        if user and password:
            self._call_params['auth'] = HTTPBasicAuth(user, password)

    def _get_response(self, url, params=None):
        """
        Make the call to the service with the given queryset and whatever params
        were set initially (auth).
        """
        res = requests.get(url,  params=params or {}, headers={'Accept': 'application/json'}, **self._call_params)
        if res.status_code != 200:
            raise Exception(res.reason)
        return res

    def get_builds(self, plan_key=None, expand=False):
        """
        Get the builds in the Bamboo server.

        :param plan_key: str
        :param expand: boolean
        :return: Generator
        """
        # Build starting qs params
        qs = {'max-result': 25, 'start-index': 0}
        if expand:
            qs['expand'] = 'results.result'

        # Get url: do we want build for a specific plan
        if plan_key:
            # Yes, just one plan
            url = '{}/{}'.format(self.build_url, plan_key)
        else:
            # I see you like to live dangerously...
            url = self.build_url
            logger.warning("Getting all builds for all plans, which can be a lot!")

        # Cycle through paged results
        size = 1
        while qs['start-index'] < size:
            # Get page, update page size and yield results
            response = self._get_response(url, qs).json()
            results = response['results']
            size = results['size']
            for r in results['result']:
                yield r

            # Update paging info
            # Note: do this here to keep it current with yields
            qs['start-index'] += results['max-result']

    def get_deployments(self, project_key=None):
        """
        Returns the list of deployment projects set up on the Bamboo server.
        :param project_key: str
        :return: Generator
        """
        url = "{}/{}".format(self.deployment_url, project_key or 'all')
        response = self._get_response(url).json()
        for r in response:
            yield r

    def get_environment_results(self, environment_id):
        """
        Returns the list of environment results.
        :param environment_id: int
        :return: Generator
        """
        # Build starting qs params
        qs = {'max-result': 25, 'start-index': 0}

        # Get url for results
        url = self.environment_url.format(env_id=environment_id)

        # Cycle through paged results
        size = 1
        while qs['start-index'] < size:
            # Get page, update page size and yield results
            response = self._get_response(url, qs).json()
            size = response['size']
            for r in response['results']:
                yield r

            # Update paging info
            # Note: do this here to keep it current with yields
            qs['start-index'] += response['max-result']

