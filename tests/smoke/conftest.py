from typing import Any
from typing import Type

import pytest
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr
from retry.api import retry_call

from pytest_celery import defaults
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.containers.worker import CeleryWorkerContainer
from tests.common.celery4.fixtures import *  # noqa


class SmokeWorkerContainer(CeleryWorkerContainer):
    @property
    def client(self) -> Any:
        # Overriding the worker container until we have a proper client class
        return self

    @classmethod
    def worker_name(cls) -> str:
        return CeleryWorkerContainer.worker_name() + "-smoke-worker"

    @classmethod
    def worker_queue(cls) -> str:
        return CeleryWorkerContainer.worker_queue() + "-smoke-tests-queue"


@pytest.fixture
def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return SmokeWorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
    return SmokeWorkerContainer


smoke_tests_worker_image = build(
    path="src/pytest_celery/components/worker",
    tag="pytest-celery/components/worker:smoke",
    buildargs={
        "CELERY_VERSION": SmokeWorkerContainer.version(),
        "CELERY_LOG_LEVEL": SmokeWorkerContainer.log_level(),
        "CELERY_WORKER_NAME": SmokeWorkerContainer.worker_name(),
        "CELERY_WORKER_QUEUE": SmokeWorkerContainer.worker_queue(),
    },
)


default_worker_container = container(
    image="{smoke_tests_worker_image.id}",
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
    nodes = tuple(
        retry_call(
            lambda: [request.getfixturevalue(worker) for worker in request.param],
            exceptions=defaults.COMPONENT_RETRYABLE_ERRORS,
            delay=defaults.COMPONENT_RETRYABLE_DELAY,
        )
    )
    cluster = CeleryWorkerCluster(*nodes)
    cluster.ready()
    yield cluster
    cluster.teardown()


@pytest.fixture
def default_worker_tasks() -> set:
    from tests.common import tasks as common_tasks
    from tests.smoke import tasks as smoke_tasks

    yield {
        common_tasks,
        smoke_tasks,
    }
