from typing import Any
from typing import Type

import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fetch
from pytest_docker_tools import fxtr
from pytest_docker_tools import network
from pytest_docker_tools import volume
from retry import retry

from pytest_celery import defaults
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.components.backend.redis.api import RedisTestBackend
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker
from pytest_celery.components.broker.redis.api import RedisTestBroker
from pytest_celery.containers.rabbitmq import RabbitMQContainer
from pytest_celery.containers.redis import RedisContainer
from pytest_celery.containers.worker import CeleryWorkerContainer
from tests.smoke.conftest import SmokeWorkerContainer


class SanityWorkerContainer(SmokeWorkerContainer):
    @classmethod
    def worker_name(cls) -> str:
        return CeleryWorkerContainer.worker_name() + "-session-worker"

    @classmethod
    def worker_queue(cls) -> str:
        return CeleryWorkerContainer.worker_queue() + "-smoke-tests-session-queue"


@retry(
    defaults.RETRY_ERRORS,
    tries=defaults.MAX_TRIES,
    delay=defaults.DELAY_SECONDS,
    max_delay=defaults.MAX_DELAY_SECONDS,
)
def session_network_with_retry() -> Any:
    try:
        return network(scope="session")
    except defaults.RETRY_ERRORS:
        # This is a workaround when running out of IPv4 addresses
        # that causes the network fixture to fail when running tests in parallel.
        return network(scope="session")


sanity_tests_network = session_network_with_retry()


celery_sanity_worker_image = build(
    path="src/pytest_celery/components/worker",
    tag="pytest-celery/components/worker:sanity",
    buildargs={
        "CELERY_VERSION": fxtr("default_worker_celery_version"),
        "CELERY_LOG_LEVEL": fxtr("default_worker_celery_log_level"),
        "CELERY_WORKER_NAME": fxtr("default_worker_celery_worker_name"),
        "CELERY_WORKER_QUEUE": fxtr("default_worker_celerky_worker_queue"),
    },
)

session_worker_test_container_volume = volume(
    initial_content=fxtr("session_worker_test_container_initial_content"),
    scope="session",
)


@pytest.fixture(scope="session")
def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return SanityWorkerContainer


@pytest.fixture(scope="session")
def session_worker_test_container_initial_content(
    default_worker_container_cls: Type[CeleryWorkerContainer],
    session_worker_test_container_tasks: set,
) -> dict:
    yield default_worker_container_cls.initial_content(session_worker_test_container_tasks)


@pytest.fixture(scope="session")
def session_worker_test_container_tasks(default_worker_container_cls: Type[CeleryWorkerContainer]) -> set:
    yield default_worker_container_cls.tasks_modules()


session_worker_test_container = container(
    image="{celery_sanity_worker_image.id}",
    scope="session",
    environment=defaults.DEFAULT_WORKER_ENV,
    network="{sanity_tests_network.name}",
    volumes={"{session_worker_test_container_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=SanityWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery_setup_worker(
    session_worker_test_container: SanityWorkerContainer,
    celery_setup_app: Celery,
) -> CeleryTestWorker:
    worker = CeleryTestWorker(
        container=session_worker_test_container,
        app=celery_setup_app,
    )
    worker.ready()
    yield worker
    worker.teardown()


session_redis_backend = container(
    image="{default_redis_backend_image}",
    ports=fxtr("default_redis_backend_ports"),
    environment=fxtr("default_redis_backend_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)
session_redis_broker = container(
    image="{default_redis_broker_image}",
    ports=fxtr("default_redis_broker_ports"),
    environment=fxtr("default_redis_broker_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)
redis_backend_container = container(
    image="{redis_image.id}",
    scope="session",
    ports=defaults.REDIS_PORTS,
    environment=defaults.REDIS_ENV,
    network="{sanity_tests_network.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)
redis_broker_container = container(
    image="{redis_image.id}",
    scope="session",
    ports=defaults.REDIS_PORTS,
    environment=defaults.REDIS_ENV,
    network="{sanity_tests_network.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery_redis_backend(redis_backend_container: RedisContainer) -> RedisTestBackend:
    backend = RedisTestBackend(redis_backend_container)
    backend.ready()
    yield backend
    backend.teardown()


@pytest.fixture
def celery_redis_broker(redis_broker_container: RedisContainer) -> RedisTestBroker:
    broker = RedisTestBroker(redis_broker_container)
    broker.ready()
    yield broker
    broker.teardown()


session_rabbitmq_broker = container(
    image="{default_rabbitmq_broker_image}",
    scope="session",
    ports=fxtr("default_rabbitmq_broker_ports"),
    environment=fxtr("default_rabbitmq_broker_env"),
    network="{sanity_tests_network.name}",
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)
rabbitmq_test_container = container(
    image="{rabbitmq_image.id}",
    ports=defaults.RABBITMQ_PORTS,
    environment=defaults.RABBITMQ_ENV,
    network="{sanity_tests_network.name}",
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery_rabbitmq_broker(rabbitmq_test_container: RabbitMQContainer) -> RabbitMQTestBroker:
    broker = RabbitMQTestBroker(rabbitmq_test_container)
    broker.ready()
    yield broker
    broker.teardown()
