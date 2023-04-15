from typing import Any
from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.api.setup import CeleryTestSetup
from pytest_celery.containers.worker import CeleryWorkerContainer


class IntegrationWorkerContainer(CeleryWorkerContainer):
    def client(self, max_tries: int = defaults.DEFAULT_READY_MAX_RETRIES) -> Any:
        return self


@pytest.fixture
def default_worker_cls() -> Type[CeleryWorkerContainer]:
    return IntegrationWorkerContainer


default_worker = container(
    image="{celery_base_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=IntegrationWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


class IntegrationTestsSetup(CeleryTestSetup):
    def ready(self, *args: tuple, **kwargs: dict) -> bool:
        kwargs["ping"] = True
        return super().ready(*args, **kwargs)


@pytest.fixture
def celery_setup_cls() -> Type[CeleryTestSetup]:
    return IntegrationTestsSetup
