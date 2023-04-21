from typing import Tuple

import pytest

# from pytest_celery import defaults
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.components.worker.node import CeleryTestWorker
from tests.common.celery4.fixtures import *  # noqa

# from retry.api import retry_call


@pytest.fixture(
    # Each param item is a list of workers to be used in the cluster
    params=[
        ["celery_setup_worker"],
        # ["celery4_worker"],
        # ["celery_setup_worker", "celery4_worker"],
    ]
)
def celery_worker_cluster(request: pytest.FixtureRequest) -> CeleryWorkerCluster:
    # nodes: Tuple[CeleryTestWorker] = tuple(
    #     retry_call(
    #         lambda: [request.getfixturevalue(worker) for worker in request.param],
    #         exceptions=defaults.COMPONENT_RETRYABLE_ERRORS,  # + (Exception,),
    #         max_delay=defaults.COMPONENT_RETRYABLE_DELAY,
    #     )
    # )
    nodes: Tuple[CeleryTestWorker] = [request.getfixturevalue(worker) for worker in request.param]
    cluster = CeleryWorkerCluster(*nodes)
    cluster.ready()
    yield cluster
    cluster.teardown()
