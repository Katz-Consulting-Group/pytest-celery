from pytest_celery.components.backend.memcached.api import MemcachedTestBackend


class test_memcached_test_backend:
    def test_ready(self, celery_memcached_backend: MemcachedTestBackend):
        assert celery_memcached_backend.ready()
