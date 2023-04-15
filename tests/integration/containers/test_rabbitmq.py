import pytest

from pytest_celery import RabbitMQContainer
from pytest_celery import defaults
from pytest_celery.utils import resilient_lazy_fixture as lazy_fixture


@pytest.mark.parametrize("container", lazy_fixture(defaults.ALL_RABBITMQ_FIXTURES))
class test_rabbitmq_container:
    def test_client(self, container: RabbitMQContainer):
        assert container.client()
