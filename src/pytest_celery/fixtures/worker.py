import pytest

from pytest_celery import defaults
from pytest_celery.api.components.worker import CeleryTestWorker
from pytest_celery.api.components.worker import CeleryWorkerCluster
from pytest_celery.utils import resilient_getfixturevalue


@pytest.fixture(params=defaults.ALL_CELERY_WORKERS)
def celery_worker(request: pytest.FixtureRequest) -> CeleryTestWorker:
    return resilient_getfixturevalue(request)


@pytest.fixture
def celery_worker_cluster(celery_worker: CeleryTestWorker) -> CeleryWorkerCluster:
    cluster = CeleryWorkerCluster(celery_worker)  # type: ignore
    cluster.ready()
    return cluster


@pytest.fixture
def celery_worker_cluster_config(celery_broker_cluster_config: dict, celery_backend_cluster_config: dict) -> dict:
    return {
        "celery_broker_cluster_config": celery_broker_cluster_config,
        "celery_backend_cluster_config": celery_backend_cluster_config,
    }
