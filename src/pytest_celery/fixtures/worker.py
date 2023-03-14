import pytest

from pytest_celery.api.components.worker import CeleryTestWorker
from pytest_celery.api.components.worker import CeleryWorkerCluster
from pytest_celery.defaults import FUNCTION_WORKERS
from pytest_celery.defaults import SESSION_WORKERS


@pytest.fixture(params=FUNCTION_WORKERS)
def celery_worker(request: pytest.FixtureRequest) -> CeleryTestWorker:
    return CeleryTestWorker(request.getfixturevalue(request.param))


@pytest.fixture(params=SESSION_WORKERS)
def celery_session_worker(request: pytest.FixtureRequest) -> CeleryTestWorker:
    return CeleryTestWorker(request.getfixturevalue(request.param))


@pytest.fixture
def celery_worker_cluster(celery_test_worker: CeleryTestWorker) -> CeleryWorkerCluster:
    return CeleryWorkerCluster(celery_test_worker)


@pytest.fixture
def celery_session_worker_cluster(celery_session_worker: CeleryTestWorker) -> CeleryWorkerCluster:
    return CeleryWorkerCluster(celery_session_worker)
