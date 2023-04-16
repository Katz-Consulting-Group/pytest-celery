import pytest

from pytest_celery import defaults
from pytest_celery.api.setup import CeleryTestSetup
from tests.common.tasks import identity
from tests.common.test_setup import shared_celery_test_setup_suite


@pytest.fixture
def default_worker_tasks() -> set:
    from tests.common import tasks

    return {tasks}


class test_celery_test_setup(shared_celery_test_setup_suite):
    def test_ready(self, celery_setup: CeleryTestSetup):
        queue = celery_setup.worker_cluster[0].worker_queue
        r = identity.s("test_ready").apply_async(queue=queue)
        assert r.get(timeout=defaults.RESULT_TIMEOUT) == "test_ready"

    def test_celery_test_setup_ready_ping(self, celery_setup: CeleryTestSetup):
        assert celery_setup.ready(ping=True)

    def test_celery_test_setup_ready_ping_false(self, celery_setup: CeleryTestSetup):
        assert celery_setup.ready(ping=False)
