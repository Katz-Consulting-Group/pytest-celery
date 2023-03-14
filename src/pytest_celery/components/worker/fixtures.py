import pytest
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.worker.api import BaseTestWorker
from pytest_celery.containers.worker import CeleryWorkerContainer
from pytest_celery.defaults import DEFAULT_NETWORK  # noqa

celery_base_worker_image = build(
    path="src/pytest_celery/components/worker/docker",
    tag="pytest-celery/components/worker:base",
    buildargs={
        "CELERY_VERSION": fxtr("function_worker_celery_version"),
    },
)


@pytest.fixture
def celery_test_worker(function_worker: CeleryWorkerContainer) -> BaseTestWorker:
    return BaseTestWorker(function_worker)


function_worker = container(
    image="{celery_base_worker_image.id}",
    environment=fxtr("function_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=CeleryWorkerContainer,
)


@pytest.fixture(scope="session")
def function_worker_celery_version() -> str:
    return defaults.WORKER_CELERY_VERSION


@pytest.fixture
def function_worker_env(celery_worker_config) -> dict:
    return {**defaults.FUNCTION_WORKER_ENV, **celery_worker_config}
