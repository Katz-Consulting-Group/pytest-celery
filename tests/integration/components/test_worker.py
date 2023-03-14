import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import BaseTestWorker
from pytest_celery import defaults


@pytest.mark.parametrize(
    "node",
    [
        lazy_fixture(defaults.CELERY_TEST_WORKER),
    ],
)
class test_redis_test_backend:
    def test_ready(self, node: BaseTestWorker):
        assert node.ready()
