import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.backend.redis.api import RedisTestBackend
from pytest_celery.containers.redis import RedisContainer


@pytest.fixture
def celery_redis_backend(redis_function_backend: RedisContainer) -> RedisTestBackend:
    return RedisTestBackend(redis_function_backend)


redis_function_backend = container(
    image="{redis_function_backend_image}",
    ports=fxtr("redis_function_backend_ports"),
    environment=fxtr("redis_function_backend_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)


@pytest.fixture
def redis_function_backend_env() -> dict:
    return defaults.REDIS_FUNCTION_BACKEND_ENV


@pytest.fixture
def redis_function_backend_image() -> str:
    return defaults.REDIS_FUNCTION_BACKEND_IMAGE


@pytest.fixture
def redis_function_backend_ports() -> dict:
    return defaults.REDIS_FUNCTION_BACKEND_PORTS


@pytest.fixture
def redis_function_backend_celeryconfig(redis_function_backend: RedisContainer) -> dict:
    return {"result_backend": redis_function_backend.celeryconfig()["url"]}
