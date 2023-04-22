# mypy: disable-error-code="misc"

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr
from retry import retry

from pytest_celery import CeleryTestSetup
from pytest_celery import defaults
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker
from pytest_celery.containers.rabbitmq import RabbitMQContainer
from tests.common.tasks import identity

failover_broker = container(
    image="{default_rabbitmq_broker_image}",
    ports=fxtr("default_rabbitmq_broker_ports"),
    environment=fxtr("default_rabbitmq_broker_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture
def failover_rabbitmq_broker(failover_broker: RabbitMQContainer) -> RabbitMQTestBroker:
    broker = RabbitMQTestBroker(failover_broker)
    broker.ready()
    yield broker
    broker.teardown()


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture
def celery_broker_cluster(
    celery_rabbitmq_broker: RabbitMQTestBroker,
    failover_rabbitmq_broker: RabbitMQTestBroker,
) -> CeleryBrokerCluster:
    cluster = CeleryBrokerCluster(celery_rabbitmq_broker, failover_rabbitmq_broker)
    cluster.ready()
    yield cluster
    cluster.teardown()


class test_failover:
    def test_broker_failover(self, celery_setup: CeleryTestSetup):
        assert 3 <= len(celery_setup) <= 6
        assert len(celery_setup.broker_cluster) == 2
        celery_setup.broker_cluster[0].kill()
        for worker in celery_setup.worker_cluster:
            expected = "test_broker_failover"
            res = identity.s(expected).apply_async(queue=worker.worker_queue)
            assert res.get() == expected
