import pytest

from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults
from pytest_celery.utils import resilient_lazy_fixture as lazy_fixture


@pytest.mark.parametrize("container", lazy_fixture(defaults.ALL_WORKERS_FIXTURES))
class test_celery_worker_container:
    def test_client(self, container: CeleryWorkerContainer):
        c = container.client()
        assert c
        assert c == container, "Check tests/conftest.py/WorkerContainer.client"
