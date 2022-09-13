import asyncio
from tornado.web import Application
from stochss_compute.server.run import RunHandler
from stochss_compute.server.status import StatusHandler
from stochss_compute.server.results import ResultsHandler
import os

def make_app(dask_host, dask_scheduler_port, cache):
    scheduler_address = f'{dask_host}:{dask_scheduler_port}'
    return Application([
        (r"/api/v2/simulation/gillespy2/run", RunHandler, {'scheduler_address': scheduler_address, 'cache_dir': cache}),
        (r"/api/v2/simulation/gillespy2/(?P<results_id>.*?)/status", StatusHandler, {'scheduler_address': scheduler_address, 'cache_dir': cache}),
        (r"/api/v2/simulation/gillespy2/(?P<results_id>.*?)/results", ResultsHandler, {'cache_dir': cache}),
    ])

async def start_api(
        port = 29681, 
        cache = 'cache/',
        dask_host = 'localhost',
        dask_scheduler_port = 8786,
        ):
    
    """
    Start the REST API with the following arguments.

    :param port: The port to listen on.
    :type port: int

    :param cache: The cache directory path.
    :type cache: str

    :param dask_host: The address of the dask cluster.
    :type dask_host: str

    :param dask_scheduler_port: The port the dask cluster.
    :type dask_scheduler_port: int
    """
    if os.path.exists(cache):
        # load cache ?
        pass
    else:
        os.mkdir(cache)
        
    app = make_app(dask_host, dask_scheduler_port, cache)
    app.listen(port)
    await asyncio.Event().wait()
