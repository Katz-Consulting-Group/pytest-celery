import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import CeleryTestSetup
from pytest_celery import defaults
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker
from pytest_celery.containers.rabbitmq import RabbitMQContainer
from tests.common.tasks import identity

failover_broker = container(
    image="{rabbitmq_function_broker_image}",
    ports=fxtr("rabbitmq_function_broker_ports"),
    environment=fxtr("rabbitmq_function_broker_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture
def failover_rabbitmq_broker(failover_broker: RabbitMQContainer) -> RabbitMQTestBroker:
    return RabbitMQTestBroker(failover_broker)


@pytest.fixture
def celery_broker_cluster(
    celery_rabbitmq_broker: RabbitMQTestBroker,
    failover_rabbitmq_broker: RabbitMQTestBroker,
) -> CeleryBrokerCluster:
    return CeleryBrokerCluster(celery_rabbitmq_broker, failover_rabbitmq_broker)


class test_failover:
    def test_broker_failover(self, celery_setup: CeleryTestSetup):
        celery_setup.broker_cluster.nodes[0].container.kill()
        res = identity.s("test_signals").delay()
        res = res.get()
        assert res == "test_signals"