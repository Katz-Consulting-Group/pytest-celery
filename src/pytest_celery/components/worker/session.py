# mypy: disable-error-code="misc"

from typing import Type

import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr
from pytest_docker_tools import volume

from pytest_celery import defaults
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.containers.worker import CeleryWorkerContainer


@pytest.fixture(scope="session")
def default_session_worker_cls() -> Type[CeleryTestWorker]:
    return CeleryTestWorker


@pytest.fixture(scope="session")
def celery_session_setup_worker(
    default_session_worker_cls: Type[CeleryTestWorker],
    default_session_worker_container: CeleryWorkerContainer,
    celery_session_setup_app: Celery,
) -> CeleryTestWorker:
    worker = default_session_worker_cls(
        container=default_session_worker_container,
        app=celery_session_setup_app,
    )
    worker.ready()
    yield worker
    worker.teardown()


@pytest.fixture(scope="session")
def default_session_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return CeleryWorkerContainer


@pytest.fixture(scope="session")(scope="session")
def default_session_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
    return CeleryWorkerContainer


default_session_worker_container = container(
    image="{celery_base_worker_image.id}",
    environment=fxtr("default_session_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_session_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=CeleryWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)

celery_base_worker_image = build(
    path="src/pytest_celery/components/worker",
    tag="pytest-celery/components/worker:session",
    buildargs={
        "CELERY_VERSION": fxtr("default_session_worker_celery_version"),
        "CELERY_LOG_LEVEL": fxtr("default_session_worker_celery_log_level"),
        "CELERY_WORKER_NAME": fxtr("default_session_worker_celery_worker_name"),
        "CELERY_WORKER_QUEUE": fxtr("default_session_worker_celerky_worker_queue"),
    },
)

default_session_worker_volume = volume(
    initial_content=fxtr("default_session_worker_initial_content"),
)


@pytest.fixture(scope="session")(scope="session")
def default_session_worker_celery_version(
    default_session_worker_container_session_cls: Type[CeleryWorkerContainer],
) -> str:
    yield default_session_worker_container_session_cls.version()


@pytest.fixture(scope="session")(scope="session")
def default_session_worker_celery_log_level(
    default_session_worker_container_session_cls: Type[CeleryWorkerContainer],
) -> str:
    yield default_session_worker_container_session_cls.log_level()


@pytest.fixture(scope="session")(scope="session")
def default_session_worker_celery_worker_name(
    default_session_worker_container_session_cls: Type[CeleryWorkerContainer],
) -> str:
    yield default_session_worker_container_session_cls.worker_name()


@pytest.fixture(scope="session")(scope="session")
def default_session_worker_celerky_worker_queue(
    default_session_worker_container_session_cls: Type[CeleryWorkerContainer],
) -> str:
    yield default_session_worker_container_session_cls.worker_queue()


@pytest.fixture(scope="session")
def default_session_worker_env(
    default_session_worker_container_cls: Type[CeleryWorkerContainer],
    celery_worker_cluster_config: dict,
) -> dict:
    yield default_session_worker_container_cls.env(celery_worker_cluster_config)


@pytest.fixture(scope="session")
def default_session_worker_initial_content(
    default_session_worker_container_cls: Type[CeleryWorkerContainer],
    default_session_worker_tasks: set,
    default_session_worker_signals: set,
) -> dict:
    yield default_session_worker_container_cls.initial_content(
        worker_tasks=default_session_worker_tasks,
        worker_signals=default_session_worker_signals,
    )


@pytest.fixture(scope="session")
def default_session_worker_tasks(default_session_worker_container_cls: Type[CeleryWorkerContainer]) -> set:
    yield default_session_worker_container_cls.tasks_modules()


@pytest.fixture(scope="session")
def default_session_worker_signals(default_session_worker_container_cls: Type[CeleryWorkerContainer]) -> set:
    yield default_session_worker_container_cls.signals_modules()
