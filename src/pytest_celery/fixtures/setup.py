import pytest
from celery import Celery

from pytest_celery.api.components.backend.cluster import CeleryBackendCluster
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.setup import CeleryTestSetup


@pytest.fixture
def celery_setup_app(celery_worker_config: dict) -> Celery:
    celery_broker_config = celery_worker_config["celery_broker_config"]
    celery_backend_config = celery_worker_config["celery_backend_config"]
    app = Celery("celery_test_app")
    app.config_from_object(
        {
            "broker_url": celery_broker_config["local_url"],
            "result_backend": celery_backend_config["local_url"],
        }
    )
    return app


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
    setup.ready()
    return setup
