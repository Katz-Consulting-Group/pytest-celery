# mypy: disable-error-code="misc"

import pytest
from retry.api import retry_call

from pytest_celery import defaults
from pytest_celery.api.components.worker import CeleryTestWorker
from pytest_celery.api.components.worker import CeleryWorkerCluster


@pytest.fixture(params=defaults.ALL_CELERY_WORKERS)
def celery_worker(request: pytest.FixtureRequest) -> CeleryTestWorker:  # type: ignore
    worker: CeleryTestWorker = retry_call(
        lambda: request.getfixturevalue(request.param),
        exceptions=defaults.COMPONENT_RETRYABLE_ERRORS,
        tries=defaults.MAX_TRIES,
        delay=defaults.DELAY_SECONDS,
        max_delay=defaults.MAX_DELAY_SECONDS,
    )
    worker.ready()
    yield worker
    worker.teardown()


@pytest.fixture
def celery_worker_cluster(celery_worker: CeleryTestWorker) -> CeleryWorkerCluster:  # type: ignore
    cluster = CeleryWorkerCluster(celery_worker)  # type: ignore
    cluster.ready()
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_worker_cluster_config(celery_broker_cluster_config: dict, celery_backend_cluster_config: dict) -> dict:
    return {
        "celery_broker_cluster_config": celery_broker_cluster_config,
        "celery_backend_cluster_config": celery_backend_cluster_config,
    }
