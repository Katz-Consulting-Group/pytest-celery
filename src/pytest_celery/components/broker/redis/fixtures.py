import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.broker.redis.api import RedisTestBroker
from pytest_celery.containers.redis import RedisContainer


@pytest.fixture
def celery_redis_broker(redis_session_broker: RedisContainer) -> RedisTestBroker:
    return RedisTestBroker(redis_session_broker)


redis_function_broker = container(
    image="{redis_function_broker_image}",
    ports=fxtr("redis_function_broker_ports"),
    environment=fxtr("redis_function_broker_env"),
    wrapper_class=RedisContainer,
)


@pytest.fixture
def redis_function_broker_env() -> dict:
    return defaults.REDIS_FUNCTION_BROKER_ENV


@pytest.fixture
def redis_function_broker_image() -> str:
    return defaults.REDIS_FUNCTION_BROKER_IMAGE


@pytest.fixture
def redis_function_broker_ports() -> dict:
    return defaults.REDIS_FUNCTION_BROKER_PORTS


redis_session_broker = container(
    image="{redis_session_broker_image}",
    scope="session",
    ports=fxtr("redis_session_broker_ports"),
    environment=fxtr("redis_session_broker_env"),
    wrapper_class=RedisContainer,
)


@pytest.fixture(scope="session")
def redis_session_broker_env() -> dict:
    return defaults.REDIS_SESSION_BROKER_ENV


@pytest.fixture(scope="session")
def redis_session_broker_image() -> str:
    return defaults.REDIS_SESSION_BROKER_IMAGE


@pytest.fixture(scope="session")
def redis_session_broker_ports() -> dict:
    return defaults.REDIS_SESSION_BROKER_PORTS
