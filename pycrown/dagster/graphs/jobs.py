from dagster import graph

from pycrown.dagster.ops import treecrown
from pycrown.dagster.resources.config import values_resource

@graph
def pycrown_run():

    treecrown.run()



pycrown_run_job = pycrown_run.to_job(resource_defs={"inputs": values_resource})