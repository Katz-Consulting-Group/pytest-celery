import pytest
from multi_broker_setup import MultiBrokerSetup

from pytest_celery import CeleryTestBackend
from pytest_celery import CeleryTestBroker
from pytest_celery import CeleryTestSetup
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker
from pytest_celery import RedisContainer
from pytest_celery import RedisTestBackend
from pytest_celery import RedisTestBroker


class RabbitMQSetup(CeleryTestSetup):
    def __init__(
        self,
        rabbitmq_broker: RabbitMQContainer,
    ):
        super().__init__(rabbitmq_broker, None)

    def ready(self) -> bool:
        return self.broker.ready()


@pytest.fixture
def celery_rabbitmq_setup(celery_rabbitmq_broker):
    return RabbitMQSetup(celery_rabbitmq_broker)


@pytest.mark.parametrize("i", list(range(1)))
def test_double_setups(celery_setup, celery_multi_broker_setup, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_celery_setup(celery_setup, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_rabbitmq_setup(celery_rabbitmq_setup, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_multi_broker_setup(celery_multi_broker_setup, i):
    s: MultiBrokerSetup = celery_multi_broker_setup
    assert s.ready()


@pytest.mark.parametrize("i", list(range(1)))
def test_default_celery_setup(
    celery_setup: CeleryTestSetup,
    celery_rabbitmq_broker: RabbitMQTestBroker,
    celery_redis_broker: RedisTestBroker,
    celery_redis_backend: RedisTestBackend,
    i,
):
    assert celery_setup.broker in (celery_rabbitmq_broker.broker, celery_redis_broker.broker)
    assert celery_setup.backend == celery_redis_backend.backend
    assert celery_setup.ready()


@pytest.mark.parametrize("i", list(range(1)))
def test_all_celery_components(celery_session_broker, celery_session_backend, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_all_brokers_vs_rabbit(celery_session_broker, celery_rabbitmq_broker, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_all_brokers_vs_redis(celery_session_broker, celery_redis_broker, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_all_backends_vs_rabbit(celery_session_backend, celery_rabbitmq_broker, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_rabbitmq_broker_redis_backend(celery_rabbitmq_broker, celery_redis_backend, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_xdist(
    celery_session_broker: CeleryTestBroker,
    celery_session_backend: CeleryTestBackend,
    celery_rabbitmq_broker: RabbitMQTestBroker,
    celery_redis_broker: RedisTestBroker,
    celery_redis_backend: RedisTestBackend,
    i,
):
    if isinstance(celery_session_backend.backend, RedisContainer) and isinstance(
        celery_session_broker.broker, RedisContainer
    ):
        assert celery_redis_backend.backend != celery_redis_broker.broker
        assert celery_session_backend.backend == celery_redis_backend.backend
        assert celery_session_broker.broker == celery_redis_broker.broker

    if isinstance(celery_session_backend.backend, RedisContainer):
        assert celery_session_backend.backend == celery_redis_backend.backend

    if isinstance(celery_session_broker.broker, RedisContainer):
        assert celery_session_broker.broker == celery_redis_broker.broker
        assert celery_session_broker.broker.status == "running"
        c = celery_session_broker.broker.client()
        c.set("foo", "bar")
        assert c.get("foo") == "bar"
    elif isinstance(celery_session_broker.broker, RabbitMQContainer):
        assert celery_session_broker.broker == celery_rabbitmq_broker.broker
        assert celery_session_broker.broker.status == "running"
        c = celery_session_broker.broker.client()
        assert c.info()
    else:
        raise RuntimeError("Unknown broker container type")
