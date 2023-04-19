# mypy: disable-error-code="misc"

from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker
from pytest_celery.containers.rabbitmq import RabbitMQContainer


@pytest.fixture(scope="session")
def celery_session_rabbitmq_broker(default_session_rabbitmq_broker: RabbitMQContainer) -> RabbitMQTestBroker:
    broker = RabbitMQTestBroker(default_session_rabbitmq_broker)
    broker.ready()
    yield broker
    broker.teardown()


@pytest.fixture(scope="session")
def default_session_rabbitmq_broker_cls() -> Type[RabbitMQContainer]:
    return RabbitMQContainer


default_session_rabbitmq_broker = container(
    image="{default_session_rabbitmq_broker_image}",
    scope="session",
    ports=fxtr("default_session_rabbitmq_broker_ports"),
    environment=fxtr("default_session_rabbitmq_broker_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture(scope="session")
def default_session_rabbitmq_broker_env(default_session_rabbitmq_broker_cls: Type[RabbitMQContainer]) -> dict:
    yield default_session_rabbitmq_broker_cls.env()


@pytest.fixture(scope="session")
def default_session_rabbitmq_broker_image(default_session_rabbitmq_broker_cls: Type[RabbitMQContainer]) -> str:
    yield default_session_rabbitmq_broker_cls.image()


@pytest.fixture(scope="session")
def default_session_rabbitmq_broker_ports(default_session_rabbitmq_broker_cls: Type[RabbitMQContainer]) -> dict:
    yield default_session_rabbitmq_broker_cls.ports()


@pytest.fixture(scope="session")
def default_session_rabbitmq_broker_celeryconfig(default_session_rabbitmq_broker: RabbitMQContainer) -> dict:
    yield {"broker_url": default_session_rabbitmq_broker.celeryconfig["url"]}
