from typing import Any
from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.containers.worker import CeleryWorkerContainer
from pytest_celery.utils import cached_property
from tests.common.celery4.fixtures import *  # noqa


class SmokeWorkerContainer(CeleryWorkerContainer):
    @cached_property
    def client(self) -> Any:
        # Overriding the worker container until we have a proper client class
        # to return. This will be applied only to the integration & smoke tests.
        # Unit tests have their own worker container.
        return self


@pytest.fixture
def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return SmokeWorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
    return SmokeWorkerContainer


default_worker_container = container(
    image="{celery_base_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=SmokeWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture(
    # Each param item is a list of workers to be used in the cluster
    params=[
        ["celery_setup_worker"],
        ["celery4_worker"],
        ["celery_setup_worker", "celery4_worker"],
    ]
)
def celery_worker_cluster(request: pytest.FixtureRequest) -> CeleryWorkerCluster:
    return CeleryWorkerCluster(*[request.getfixturevalue(worker) for worker in request.param])


@pytest.fixture
def default_worker_tasks() -> set:
    from tests.common import tasks as common_tasks
    from tests.smoke import tasks as smoke_tasks

    return {
        common_tasks,
        smoke_tasks,
    }
