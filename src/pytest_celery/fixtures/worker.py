# mypy: disable-error-code="misc"

import pytest
from retry import retry

from pytest_celery import defaults
from pytest_celery.api.components.worker import CeleryTestWorker
from pytest_celery.api.components.worker import CeleryWorkerCluster


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture(params=defaults.ALL_CELERY_WORKERS)
def celery_worker(request: pytest.FixtureRequest) -> CeleryTestWorker:  # type: ignore
    worker: CeleryTestWorker = request.getfixturevalue(request.param)
    worker.ready()
    yield worker
    worker.teardown()


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture
def celery_worker_cluster(celery_worker: CeleryTestWorker) -> CeleryWorkerCluster:  # type: ignore
    cluster = CeleryWorkerCluster(celery_worker)  # type: ignore
    cluster.ready()
    yield cluster
    cluster.teardown()


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture
def celery_worker_cluster_config(celery_broker_cluster_config: dict, celery_backend_cluster_config: dict) -> dict:
    return {
        "celery_broker_cluster_config": celery_broker_cluster_config,
        "celery_backend_cluster_config": celery_backend_cluster_config,
    }
