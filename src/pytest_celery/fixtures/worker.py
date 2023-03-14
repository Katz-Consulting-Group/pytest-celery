import pytest

from pytest_celery import defaults
from pytest_celery.api.components.worker import CeleryTestWorker
from pytest_celery.api.components.worker import CeleryWorkerCluster


@pytest.fixture(params=defaults.ALL_CELERY_WORKERS)
def celery_worker(request: pytest.FixtureRequest) -> CeleryTestWorker:
    return request.getfixturevalue(request.param)


@pytest.fixture
def celery_worker_cluster(celery_worker: CeleryTestWorker) -> CeleryWorkerCluster:
    return CeleryWorkerCluster(celery_worker)


@pytest.fixture
def celery_worker_config(celery_broker_config, celery_backend_config) -> dict:
    celery_broker_config = celery_broker_config or {"broker_url": defaults.WORKER_ENV["CELERY_BROKER_URL"]}
    celery_backend_config = celery_backend_config or {"result_backend": defaults.WORKER_ENV["CELERY_RESULT_BACKEND"]}

    return {
        "CELERY_BROKER_URL": celery_broker_config["broker_url"],
        "CELERY_RESULT_BACKEND": celery_backend_config["result_backend"],
    }
