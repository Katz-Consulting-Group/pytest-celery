import pytest
from integration.shared.celery4.api import Celery4TestWorker
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery.containers.worker import CeleryWorkerContainer
from pytest_celery.defaults import DEFAULT_NETWORK  # noqa

celery4_worker_image = build(
    path="tests/integration/shared/celery4/docker",
    tag="pytest-celery/components/worker:celery4",
    buildargs={
        "CELERY_VERSION": "4.4.7",
    },
)


@pytest.fixture
def celery4_test_worker(celery4_worker: CeleryWorkerContainer) -> Celery4TestWorker:
    return Celery4TestWorker(celery4_worker)


celery4_worker = container(
    image="{celery4_worker_image.id}",
    environment=fxtr("function_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=CeleryWorkerContainer,
)
