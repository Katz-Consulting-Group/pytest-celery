from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.backend.memcached.api import MemcachedTestBackend
from pytest_celery.containers.memcached import MemcachedContainer


@pytest.fixture
def celery_memcached_backend(default_memcached_backend: MemcachedContainer) -> MemcachedTestBackend:
    return MemcachedTestBackend(default_memcached_backend)


@pytest.fixture
def default_memcached_backend_cls() -> Type[MemcachedContainer]:
    return MemcachedContainer


default_memcached_backend = container(
    image="{default_memcached_backend_image}",
    ports=fxtr("default_memcached_backend_ports"),
    environment=fxtr("default_memcached_backend_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=MemcachedContainer,
    timeout=defaults.MEMCACHED_CONTAINER_TIMEOUT,
)


@pytest.fixture
def default_memcached_backend_env(default_memcached_backend_cls: Type[MemcachedContainer]) -> dict:
    return default_memcached_backend_cls.env()


@pytest.fixture
def default_memcached_backend_image(default_memcached_backend_cls: Type[MemcachedContainer]) -> str:
    return default_memcached_backend_cls.image()


@pytest.fixture
def default_memcached_backend_ports(default_memcached_backend_cls: Type[MemcachedContainer]) -> dict:
    return default_memcached_backend_cls.ports()


@pytest.fixture
def default_memcached_backend_celeryconfig(default_memcached_backend: MemcachedContainer) -> dict:
    return {"result_backend": default_memcached_backend.celeryconfig()["url"]}
