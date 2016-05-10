# Python Bamboo API

Client for Bamboo REST API, providing basic authentication and a few methods 
to fetch plans, builds and deployments.


## Installation

Install from pypi:

    pip install bamboo_api


## Usage

Example use:

    from bamboo_api import BambooAPIClient

    bamboo = BambooAPIClient(user='admin', password='admin')
    for build in bamboo.get_builds():
        # do something with builds results...

By default it will return the latest build for every plan, but you can 
also specify a single plan to fetch all the builds for it, and expand 
to get more detailed information:

    bamboo = BambooAPIClient(user='admin', password='admin')
    for build in bamboo.get_builds(project_key='MYPRJ-KEY', expand=True):
        # do something with builds results...



## Supported Methods

The supported methods are:

* get_builds: generator that yields builds
* get_deployments: generator that yields deployment projects
* get_environment_results: generator that yields deployment results
* get_plans: generator that yields plans
