import pytest
from kombu import Connection
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_RABBITMQ_BROKER
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker
from tests.defaults import ALL_RABBITMQ_FIXTURES


@pytest.mark.parametrize("container", lazy_fixture(ALL_RABBITMQ_FIXTURES))
class test_rabbitmq_container:
    def test_client(self, container: RabbitMQContainer):
        c: Connection = container.client
        assert c
        try:
            assert c.connect()
        finally:
            c.release()


@pytest.mark.parametrize("node", [lazy_fixture(CELERY_RABBITMQ_BROKER)])
class test_rabbitmq_test_broker:
    def test_ready(self, node: RabbitMQTestBroker):
        assert node.ready()