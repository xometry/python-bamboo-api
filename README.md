# Python Bamboo API

Client for Bamboo REST API, providing basic authentication and a few methods to fetch
builds and deployments.


## Installation

Install from this repository:

    pip install -e git+git@github.com:liocuevas/python-bamboo-api.git#egg=bamboo_api


## Usage

Example use:

    from bamboo_api import BambooAPIClient

    bamboo = BambooAPIClient(user='admin', password='admin')
    for build in bamboo.get_builds():
        # do something with builds results...

You can also specify a single project to fetch by default it will return the latest builds
but you can get all the builds using the expand arg:

    bamboo = BambooAPIClient(user='admin', password='admin')
    for build in bamboo.get_builds(project_key='MYPRJ-KEY', expand=True):
        # do something with builds results...



## Supported Methods

The supported methods are:

* get_builds: List of builds

