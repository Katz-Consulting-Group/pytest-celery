import pytest

from pytest_celery.api.components.backend.cluster import CeleryBackendCluster
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.setup import CeleryTestSetup


@pytest.fixture
def celery_setup(
    celery_worker_cluster: CeleryWorkerCluster,
    celery_broker_cluster: CeleryBrokerCluster,
    celery_backend_cluster: CeleryBackendCluster,
) -> CeleryTestSetup:
    setup = CeleryTestSetup(
        worker_cluster=celery_worker_cluster,
        broker_cluster=celery_broker_cluster,
        backend_cluster=celery_backend_cluster,
    )
    setup.ready()
    return setup
