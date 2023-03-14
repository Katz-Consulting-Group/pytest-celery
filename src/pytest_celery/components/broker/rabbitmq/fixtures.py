import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker
from pytest_celery.containers.rabbitmq import RabbitMQContainer


@pytest.fixture
def celery_rabbitmq_broker(rabbitmq_session_broker: RabbitMQContainer) -> RabbitMQTestBroker:
    return RabbitMQTestBroker(rabbitmq_session_broker)


rabbitmq_function_broker = container(
    image="{rabbitmq_function_broker_image}",
    ports=fxtr("rabbitmq_function_broker_ports"),
    environment=fxtr("rabbitmq_function_broker_env"),
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture
def rabbitmq_function_broker_env() -> dict:
    return defaults.RABBITMQ_FUNCTION_BROKER_ENV


@pytest.fixture
def rabbitmq_function_broker_image() -> str:
    return defaults.RABBITMQ_FUNCTION_BROKER_IMAGE


@pytest.fixture
def rabbitmq_function_broker_ports() -> dict:
    return defaults.RABBITMQ_FUNCTION_BROKER_PORTS


rabbitmq_session_broker = container(
    image="{rabbitmq_session_broker_image}",
    scope="session",
    ports=fxtr("rabbitmq_session_broker_ports"),
    environment=fxtr("rabbitmq_session_broker_env"),
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture(scope="session")
def rabbitmq_session_broker_env() -> dict:
    return defaults.RABBITMQ_SESSION_BROKER_ENV


@pytest.fixture(scope="session")
def rabbitmq_session_broker_image() -> str:
    return defaults.RABBITMQ_SESSION_BROKER_IMAGE


@pytest.fixture(scope="session")
def rabbitmq_session_broker_ports() -> dict:
    return defaults.RABBITMQ_SESSION_BROKER_PORTS
