import pytest
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.worker.api import BaseTestWorker
from pytest_celery.containers.worker import CeleryWorkerContainer

celery_base_worker_image = build(
    path="src/pytest_celery/components/worker/docker",
    tag="localhost/pytest-celery/components/worker:base",
)


@pytest.fixture
def celery_test_worker(session_worker: CeleryWorkerContainer) -> BaseTestWorker:
    return BaseTestWorker(session_worker)


function_worker = container(
    image="{celery_base_worker_image.id}",
    environment=fxtr("function_worker_env"),
    wrapper_class=CeleryWorkerContainer,
)


@pytest.fixture
def function_worker_env() -> dict:
    return defaults.FUNCTION_WORKER_ENV


session_worker = container(
    image="{celery_base_worker_image.id}",
    scope="session",
    environment=fxtr("session_worker_env"),
    wrapper_class=CeleryWorkerContainer,
)


@pytest.fixture(scope="session")
def session_worker_env() -> dict:
    return defaults.SESSION_WORKER_ENV
