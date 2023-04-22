# from typing import Any
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
from retry.api import retry_call

from pytest_celery import defaults
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.components.backend.redis.api import RedisTestBackend
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker
from pytest_celery.components.broker.redis.api import RedisTestBroker
from pytest_celery.containers.rabbitmq import RabbitMQContainer
from pytest_celery.containers.redis import RedisContainer
from pytest_celery.containers.worker import CeleryWorkerContainer
from tests.unit.docker.api import UnitTestContainer
from tests.unit.docker.api import UnitWorkerContainer


# @retry(BaseException)
# def parallel_network():
#     return network(scope="session")
def parallel_network():
    n = retry_call(
        f=network,
        fkwargs={"scope": "session"},
        exceptions=defaults.NETWORK_RETRYABLE_ERRORS,
    )
    return n


# unit_tests_network = parallel_network()
unit_tests_network = network(scope="session")

unit_tests_image = build(
    path="tests/unit/docker",
    tag="pytest-celery/tests/unit:latest",
)

unit_tests_container = container(
    image="{unit_tests_image.id}",
    scope="session",
    network="{unit_tests_network.name}",
    wrapper_class=UnitTestContainer,
)

local_test_container = container(
    image="{unit_tests_image.id}",
    network="{unit_tests_network.name}",
    wrapper_class=UnitTestContainer,
)

celery_unit_worker_image = build(
    path="src/pytest_celery/components/worker",
    tag="pytest-celery/components/worker:unit",
    buildargs=UnitWorkerContainer.buildargs(),
)

worker_test_container_volume = volume(
    initial_content=fxtr("worker_test_container_initial_content"),
    scope="session",
)


@pytest.fixture(scope="session")
def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return UnitWorkerContainer


@pytest.fixture(scope="session")
def worker_test_container_initial_content(
    default_worker_container_cls: Type[CeleryWorkerContainer],
    worker_test_container_tasks: set,
) -> dict:
    yield default_worker_container_cls.initial_content(worker_test_container_tasks)


@pytest.fixture(scope="session")
def worker_test_container_tasks(default_worker_container_cls: Type[CeleryWorkerContainer]) -> set:
    yield default_worker_container_cls.tasks_modules()


worker_test_container = container(
    image="{celery_unit_worker_image.id}",
    scope="session",
    environment=defaults.DEFAULT_WORKER_ENV,
    network="{unit_tests_network.name}",
    volumes={"{worker_test_container_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=UnitWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture
def celery_setup_worker(
    worker_test_container: UnitWorkerContainer,
    celery_setup_app: Celery,
) -> CeleryTestWorker:
    worker = CeleryTestWorker(
        container=worker_test_container,
        app=celery_setup_app,
    )
    worker.ready()
    yield worker
    worker.teardown()


class RedisSessionContainer(RedisContainer):
    def teardown(self) -> None:
        pass


redis_image = fetch(repository=defaults.REDIS_IMAGE)
redis_test_container = container(
    image="{redis_image.id}",
    scope="session",
    ports=defaults.REDIS_PORTS,
    environment=defaults.REDIS_ENV,
    network="{unit_tests_network.name}",
    wrapper_class=RedisSessionContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
    command=RedisSessionContainer.command(),  # TODO: use fxtr
)
redis_backend_container = container(
    image="{redis_image.id}",
    scope="session",
    ports=defaults.REDIS_PORTS,
    environment=defaults.REDIS_ENV,
    network="{unit_tests_network.name}",
    wrapper_class=RedisSessionContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
    command=RedisSessionContainer.command(),  # TODO: use fxtr
)
redis_broker_container = container(
    image="{redis_image.id}",
    scope="session",
    ports=defaults.REDIS_PORTS,
    environment=defaults.REDIS_ENV,
    network="{unit_tests_network.name}",
    wrapper_class=RedisSessionContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
    command=RedisSessionContainer.command(),  # TODO: use fxtr
)


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture
def celery_redis_backend(redis_backend_container: RedisSessionContainer) -> RedisTestBackend:
    backend = RedisTestBackend(redis_backend_container)
    backend.ready()
    yield backend
    backend.teardown()


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture
def celery_redis_broker(redis_broker_container: RedisSessionContainer) -> RedisTestBroker:
    broker = RedisTestBroker(redis_broker_container)
    broker.ready()
    yield broker
    broker.teardown()


class RabbitMQSessionContainer(RabbitMQContainer):
    def teardown(self) -> None:
        pass


rabbitmq_image = fetch(repository=defaults.RABBITMQ_IMAGE)
rabbitmq_test_container = container(
    image="{rabbitmq_image.id}",
    scope="session",
    ports=defaults.RABBITMQ_PORTS,
    environment=defaults.RABBITMQ_ENV,
    network="{unit_tests_network.name}",
    wrapper_class=RabbitMQSessionContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture
def celery_rabbitmq_broker(rabbitmq_test_container: RabbitMQSessionContainer) -> RabbitMQTestBroker:
    broker = RabbitMQTestBroker(rabbitmq_test_container)
    broker.ready()
    yield broker
    broker.teardown()
