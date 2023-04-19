# mypy: disable-error-code="misc"

from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.broker.redis.api import RedisTestBroker
from pytest_celery.containers.redis import RedisContainer


@pytest.fixture(scope="session")
def celery_session_redis_broker(default_session_redis_broker: RedisContainer) -> RedisTestBroker:
    broker = RedisTestBroker(default_session_redis_broker)
    broker.ready()
    yield broker
    broker.teardown()


@pytest.fixture(scope="session")
def default_session_redis_broker_cls() -> Type[RedisContainer]:
    return RedisContainer


default_session_redis_broker = container(
    image="{default_session_redis_broker_image}",
    scope="session",
    ports=fxtr("default_session_redis_broker_ports"),
    environment=fxtr("default_session_redis_broker_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)


@pytest.fixture(scope="session")
def default_session_redis_broker_env(default_session_redis_broker_cls: Type[RedisContainer]) -> dict:
    yield default_session_redis_broker_cls.env()


@pytest.fixture(scope="session")
def default_session_redis_broker_image(default_session_redis_broker_cls: Type[RedisContainer]) -> str:
    yield default_session_redis_broker_cls.image()


@pytest.fixture(scope="session")
def default_session_redis_broker_ports(default_session_redis_broker_cls: Type[RedisContainer]) -> dict:
    yield default_session_redis_broker_cls.ports()


@pytest.fixture(scope="session")
def default_session_redis_broker_celeryconfig(default_session_redis_broker: RedisContainer) -> dict:
    yield {"broker_url": default_session_redis_broker.celeryconfig["url"]}
