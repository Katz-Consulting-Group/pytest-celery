import pytest
from integration.shared.celery4.api import Celery4TestWorker
from integration.shared.celery4.fixtures import *  # noqa

from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.api.setup import CeleryTestSetup


@pytest.fixture(scope="session")
def function_worker_celery_version() -> str:
    return "5.2.7"


@pytest.fixture
def celery_worker_cluster(
    celery_worker: CeleryTestWorker,
    celery4_test_worker: Celery4TestWorker,
) -> CeleryWorkerCluster:
    return CeleryWorkerCluster(celery_worker, celery4_test_worker)


class test_custom_setup:
    def test_celery_setup_override(self, celery_setup: CeleryTestSetup):
        assert celery_setup.ready()
