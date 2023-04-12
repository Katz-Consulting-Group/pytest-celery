from pytest_celery.containers.memcached import MemcachedContainer


class test_memcached_container:
    def test_client(self, memcached_test_container: MemcachedContainer):
        assert memcached_test_container.client()
