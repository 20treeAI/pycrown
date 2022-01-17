from dagster import repository

from pycrown.graphs.jobs import pycrown_run_job


@repository
def pycrown():
    """
    The repository definition for this data Dagster repository.
    For hints on building your Dagster repository, see our documentation overview on Repositories:
    https://docs.dagster.io/overview/repositories-workspaces/repositories
    """
    jobs = [pycrown_run_job]


    return jobs