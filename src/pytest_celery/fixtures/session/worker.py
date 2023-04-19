# mypy: disable-error-code="misc"

import pytest

from pytest_celery import defaults
from pytest_celery.api.components.worker import CeleryTestWorker
from pytest_celery.api.components.worker import CeleryWorkerCluster

ALL_CELERY_SESSION_WORKERS = (
    f"{defaults.CELERY_FIXTURES_PREFIX}_session_{worker}" for worker in defaults.ALL_CELERY_WORKERS
)


@pytest.fixture(scope="session", params=ALL_CELERY_SESSION_WORKERS)
def celery_session_worker(request: pytest.FixtureRequest) -> CeleryTestWorker:
    worker: CeleryTestWorker = request.getfixturevalue(request.param)
    worker.ready()
    yield worker
    worker.teardown()


@pytest.fixture(scope="session")
def celery_session_worker_cluster(celery_session_worker: CeleryTestWorker) -> CeleryWorkerCluster:
    cluster = CeleryWorkerCluster(celery_session_worker)
    cluster.ready()
    yield cluster
    cluster.teardown()


@pytest.fixture(scope="session")
def celery_session_worker_cluster_config(
    celery_session_broker_cluster_config: dict,
    celery_session_backend_cluster_config: dict,
) -> dict:
    return {
        "celery_session_broker_cluster_config": celery_session_broker_cluster_config,
        "celery_session_backend_cluster_config": celery_session_backend_cluster_config,
    }
