import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr
from pytest_docker_tools import volume

from pytest_celery import defaults
from pytest_celery.components.worker.api import BaseTestWorker
from pytest_celery.containers.worker import CeleryWorkerContainer


@pytest.fixture
def celery_test_worker(function_worker: CeleryWorkerContainer, celery_setup_app: Celery) -> BaseTestWorker:
    return BaseTestWorker(
        container=function_worker,
        app=celery_setup_app,
    )


function_worker = container(
    image="{celery_base_worker_image.id}",
    environment=fxtr("function_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{function_worker_volume.name}": {"bind": "/app", "mode": "rw"}},
    wrapper_class=CeleryWorkerContainer,
    timeout=defaults.FUNCTION_WORKER_CONTAINER_TIMEOUT,
)

celery_base_worker_image = build(
    path="src/pytest_celery/components/worker",
    tag="pytest-celery/components/worker:base",
    buildargs={
        "CELERY_VERSION": fxtr("function_worker_celery_version"),
    },
)

function_worker_volume = volume(
    initial_content=fxtr("function_worker_initial_content"),
)


@pytest.fixture(scope="session")
def function_worker_celery_version() -> str:
    return CeleryWorkerContainer.version()


@pytest.fixture
def function_worker_env(celery_worker_config: dict) -> dict:
    return CeleryWorkerContainer.env(celery_worker_config)


@pytest.fixture
def function_worker_initial_content(function_worker_tasks: set) -> dict:
    return CeleryWorkerContainer.initial_content(function_worker_tasks)


@pytest.fixture
def function_worker_tasks() -> set:
    return CeleryWorkerContainer.tasks_modules()
