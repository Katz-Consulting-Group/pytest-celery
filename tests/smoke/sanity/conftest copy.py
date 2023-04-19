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
from pytest_celery.api.components.backend.cluster import CeleryBackendCluster
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.components.backend.redis.api import RedisTestBackend
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker
from pytest_celery.components.broker.redis.api import RedisTestBroker
from pytest_celery.containers.rabbitmq import RabbitMQContainer
from pytest_celery.containers.redis import RedisContainer
from pytest_celery.containers.worker import CeleryWorkerContainer
from tests.common.celery4.fixtures import Celery4WorkerContainer
from tests.common.celery4.fixtures import celery4_sanity_worker_image  # noqa
from tests.smoke.conftest import SmokeWorkerContainer


@retry(
    defaults.RETRY_ERRORS,
    tries=defaults.MAX_TRIES,
    delay=defaults.DELAY_SECONDS,
    max_delay=defaults.MAX_DELAY_SECONDS,
)
def sanity_network_with_retry() -> Any:
    try:
        return network(scope="session")
    except defaults.RETRY_ERRORS:
        # This is a workaround when running out of IPv4 addresses
        # that causes the network fixture to fail when running tests in parallel.
        return network(scope="session")


sanity_tests_network = sanity_network_with_retry()


class SanityWorkerContainer(SmokeWorkerContainer):
    @classmethod
    def worker_name(cls) -> str:
        return CeleryWorkerContainer.worker_name() + "-sanity-worker"

    @classmethod
    def worker_queue(cls) -> str:
        return CeleryWorkerContainer.worker_queue() + "-smoke-tests-sanity-queue"


@pytest.fixture(scope="session")
def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return SanityWorkerContainer


@pytest.fixture(scope="session")
def default_worker_signals(default_worker_container_cls: Type[CeleryWorkerContainer]) -> set:
    yield default_worker_container_cls.signals_modules()


@pytest.fixture(scope="session")
def sanity_worker_container_tasks(default_worker_container_cls: Type[CeleryWorkerContainer]) -> set:
    yield default_worker_container_cls.tasks_modules()


sanity_worker_image = build(
    path="src/pytest_celery/components/worker",
    tag="pytest-celery/components/worker:sanity",
    buildargs={
        "CELERY_VERSION": fxtr("default_worker_celery_version"),
        "CELERY_LOG_LEVEL": fxtr("default_worker_celery_log_level"),
        "CELERY_WORKER_NAME": fxtr("default_worker_celery_worker_name"),
        "CELERY_WORKER_QUEUE": fxtr("default_worker_celerky_worker_queue"),
    },
)


@pytest.fixture(scope="session")
def sanity_worker_container_initial_content(
    default_worker_container_cls: Type[CeleryWorkerContainer],
    sanity_worker_container_tasks: set,
) -> dict:
    yield default_worker_container_cls.initial_content(sanity_worker_container_tasks)


sanity_worker_container_volume = volume(
    initial_content=fxtr("sanity_worker_container_initial_content"),
    scope="session",
)


sanity_worker_container = container(
    image="{sanity_worker_image.id}",
    scope="session",
    environment=fxtr("default_worker_env"),
    network="{sanity_tests_network.name}",
    volumes={"{sanity_worker_container_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=SanityWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery_setup_worker(
    sanity_worker_container: SanityWorkerContainer,
    celery_setup_app: Celery,
) -> CeleryTestWorker:
    worker = CeleryTestWorker(
        container=sanity_worker_container,
        app=celery_setup_app,
    )
    worker.ready()
    yield worker
    worker.teardown()


celery4_sanity_worker_container = container(
    image="{celery4_sanity_worker_image.id}",
    scope="session",
    environment=fxtr("default_worker_env"),
    network="{sanity_tests_network.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=Celery4WorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture(scope="session")
def celery4_sanity_worker(
    celery4_sanity_worker_container: CeleryWorkerContainer,
    celery_setup_app: Celery,
) -> CeleryTestWorker:
    worker = CeleryTestWorker(
        celery4_sanity_worker_container,
        app=celery_setup_app,
    )
    worker.ready()
    yield worker


sanity_redis_backend_container = container(
    image="{default_redis_backend_image}",
    scope="session",
    ports=defaults.REDIS_PORTS,
    environment=defaults.REDIS_ENV,
    network="{sanity_tests_network.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)
sanity_redis_broker_container = container(
    image="{default_redis_broker_image}",
    scope="session",
    ports=defaults.REDIS_PORTS,
    environment=defaults.REDIS_ENV,
    network="{sanity_tests_network.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery_redis_backend(sanity_redis_backend_container: RedisContainer) -> RedisTestBackend:
    backend = RedisTestBackend(sanity_redis_backend_container)
    backend.ready()
    yield backend
    backend.teardown()


@pytest.fixture
def celery_redis_broker(sanity_redis_broker_container: RedisContainer) -> RedisTestBroker:
    broker = RedisTestBroker(sanity_redis_broker_container)
    broker.ready()
    yield broker
    broker.teardown()


rabbitmq_image = fetch(repository=defaults.RABBITMQ_IMAGE)
sanity_rabbitmq_container = container(
    image="{rabbitmq_image.id}",
    scope="session",
    ports=defaults.RABBITMQ_PORTS,
    environment=defaults.RABBITMQ_ENV,
    network="{sanity_tests_network.name}",
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery_rabbitmq_broker(sanity_rabbitmq_container: RabbitMQContainer) -> RabbitMQTestBroker:
    broker = RabbitMQTestBroker(sanity_rabbitmq_container)
    broker.ready()
    yield broker
    broker.teardown()


@pytest.fixture
def celery_backend_cluster(celery_backend: CeleryTestBackend) -> CeleryBackendCluster:  # type: ignore
    cluster = CeleryBackendCluster(celery_backend)  # type: ignore
    cluster.ready()
    yield cluster
    cluster.teardown()


@pytest.fixture(scope="session")
def celery_backend_cluster_config(celery_backend_cluster: CeleryBackendCluster) -> dict:
    celery_backend_cluster.ready()
    return celery_backend_cluster.config()


@pytest.fixture(scope="session")
def celery_broker_cluster_config(
    request: pytest.FixtureRequest,
) -> dict:
    cluster: CeleryBrokerCluster = request.getfixturevalue(defaults.CELERY_BROKER_CLUSTER)
    cluster.ready()
    return cluster.config()


@pytest.fixture(scope="session")
def celery_worker_cluster_config(celery_broker_cluster_config: dict, celery_backend_cluster_config: dict) -> dict:
    return {
        "celery_broker_cluster_config": celery_broker_cluster_config,
        "celery_backend_cluster_config": celery_backend_cluster_config,
    }
