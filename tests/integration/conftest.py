import pytest
from celery import Celery

from pytest_celery.api.components.backend.cluster import CeleryBackendCluster
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.setup import CeleryTestSetup

# @pytest.fixture
# def celery_setup(celery_setup: CeleryTestSetup) -> CeleryTestSetup:
#     celery_setup.ready(ping=True)
# class IntegrationTestsSetup(CeleryTestSetup):
#     def ready(self) -> bool:
#         return super().ready(ping=True)


# @pytest.fixture
# def celery_setup(celery_setup: CeleryTestSetup) -> IntegrationTestsSetup:
#     celery_setup = IntegrationTestsSetup(
#         worker_cluster=celery_setup.worker_cluster,
#         broker_cluster=celery_setup.broker_cluster,
#         backend_cluster=celery_setup.backend_cluster,
#         app=celery_setup.app,
#     )
#     celery_setup.ready()
@pytest.fixture
def celery_setup(
    celery_worker_cluster: CeleryWorkerCluster,
    celery_broker_cluster: CeleryBrokerCluster,
    celery_backend_cluster: CeleryBackendCluster,
    celery_setup_app: Celery,
) -> CeleryTestSetup:
    setup = CeleryTestSetup(
        worker_cluster=celery_worker_cluster,
        broker_cluster=celery_broker_cluster,
        backend_cluster=celery_backend_cluster,
        app=celery_setup_app,
    )
    setup.ready(ping=True)
    return setup
