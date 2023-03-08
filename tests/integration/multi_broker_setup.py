import pytest

from pytest_celery import CeleryTestSetup

# from pytest_celery.containers import RabbitMQContainer
# from pytest_celery.containers import RedisContainer


class MultiBrokerSetup(CeleryTestSetup):
    pass


@pytest.fixture
def celery_multi_broker_setup(celery_backend_cluster, celery_broker_cluster):
    return MultiBrokerSetup(None, None)
