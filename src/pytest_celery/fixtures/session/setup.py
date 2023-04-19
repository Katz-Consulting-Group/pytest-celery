# mypy: disable-error-code="misc"

from typing import Type

import pytest
from celery import Celery

from pytest_celery.api.components.backend.cluster import CeleryBackendCluster
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.setup import CeleryTestSetup


@pytest.fixture(scope="session")
def celery_session_setup_name() -> str:
    yield CeleryTestSetup.name()


@pytest.fixture(scope="session")
def celery_session_setup_config(celery_session_worker_cluster_config: dict) -> dict:
    yield CeleryTestSetup.config(
        celery_session_worker_cluster_config=celery_session_worker_cluster_config,
    )


@pytest.fixture(scope="session")
def celery_session_setup_app(celery_session_setup_config: dict, celery_session_setup_name: str) -> Celery:
    yield CeleryTestSetup.create_setup_app(
        celery_session_setup_config=celery_session_setup_config,
        celery_session_setup_app_name=celery_session_setup_name,
    )


@pytest.fixture(scope="session")
def celery_session_setup_cls() -> Type[CeleryTestSetup]:
    return CeleryTestSetup


@pytest.fixture(scope="session")
def celery_session_setup(
    celery_session_setup_cls: Type[CeleryTestSetup],
    celery_session_worker_cluster: CeleryWorkerCluster,
    celery_broker_cluster: CeleryBrokerCluster,
    celery_backend_cluster: CeleryBackendCluster,
    celery_session_setup_app: Celery,
) -> CeleryTestSetup:
    setup = celery_session_setup_cls(
        worker_cluster=celery_session_worker_cluster,
        broker_cluster=celery_broker_cluster,
        backend_cluster=celery_backend_cluster,
        app=celery_session_setup_app,
    )
    setup.ready()
    yield setup
    setup.teardown()
