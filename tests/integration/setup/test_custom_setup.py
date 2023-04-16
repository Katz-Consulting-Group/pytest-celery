from typing import Any
from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.api.setup import CeleryTestSetup
from pytest_celery.containers.worker import CeleryWorkerContainer
from pytest_celery.utils import cached_property
from tests.common.celery4.api import Worker4Container
from tests.common.celery4.fixtures import *  # noqa
from tests.common.tasks import identity
from tests.common.test_setup import shared_celery_test_setup_suite


class Celery5WorkerContainer(CeleryWorkerContainer):
    @cached_property
    def client(self) -> Any:
        # Overriding the worker container until we have a proper client class
        return self

    @classmethod
    def version(cls) -> str:
        return "5.2.7"

    @classmethod
    def log_level(cls) -> str:
        return "DEBUG"

    @classmethod
    def worker_queue(cls) -> str:
        return "celery5"


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
    return Celery5WorkerContainer


default_worker_container = container(
    image="{celery_base_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=Celery5WorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture
def default_worker_tasks() -> set:
    from tests.common import tasks

    return {tasks}


@pytest.fixture
def celery_worker_cluster(
    celery_worker: CeleryTestWorker,
    celery4_worker: CeleryTestWorker,
) -> CeleryWorkerCluster:
    cluster = CeleryWorkerCluster(
        celery_worker,
        celery4_worker,
    )
    cluster.ready()
    return cluster


class test_custom_setup(shared_celery_test_setup_suite):
    def test_celery_setup_override(self, celery_setup: CeleryTestSetup):
        assert celery_setup.app
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            expected = "test_celery_setup_override"
            queue = worker.worker_queue
            sig = identity.s(expected)
            res = sig.apply_async(queue=queue)
            assert res.get(timeout=defaults.RESULT_TIMEOUT) == expected

    def test_custom_cluster_version(self, celery_setup: CeleryTestSetup, default_worker_celery_version: str):
        assert len(celery_setup.worker_cluster) == 2
        assert celery_setup.worker_cluster.versions == {
            default_worker_celery_version,
            Worker4Container.version(),
        }
