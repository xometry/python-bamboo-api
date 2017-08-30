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

[https://jira.atlassian.com/browse/BAM-18428](BMA-18428)
The REST API can return master builds by label, passing in an array of labels

    labels = ['lab1','lab2']
    for build in bamboo.get_builds(labels=labels, max_result=25):
        # do something with builds by label

If you want to return a list of master and branch builds, one way is to use the label/viewBuildsForLabel.action endpoint. Unfortunately this is a HTML interface. We can scrape behind the scenes to provide a callabel interface. You can then pass to get_build, get_results etc as usual:

    builds = bamboo.get_builds_by_label(labels=labels)
    for key in set(map(lambda x: x['planKey'], builds)):
        results = bamboo.get_results(project_key=key)

The following keys are supported
- buildKey
- planKey
- projectKey

## Supported Methods

The supported methods are:

* get_builds: generator that yields builds
* get_deployments: generator that yields deployment projects
* get_environment_results: generator that yields deployment results
* get_plans: generator that yields plans
