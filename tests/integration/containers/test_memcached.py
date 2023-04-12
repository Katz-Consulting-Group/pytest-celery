import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import defaults
from pytest_celery.containers.memcached import MemcachedContainer


@pytest.mark.parametrize("container", lazy_fixture(defaults.ALL_MEMCACHED_FIXTURES))
class test_memcached_container:
    def test_client(self, container: MemcachedContainer):
        assert container.client()
