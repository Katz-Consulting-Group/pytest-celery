import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import MemcachedTestBackend
from pytest_celery import defaults


@pytest.mark.parametrize("node", [lazy_fixture(defaults.CELERY_MEMCACHED_BACKEND)])
class test_memcached_test_backend:
    def test_ready(self, node: MemcachedTestBackend):
        assert node.ready()
