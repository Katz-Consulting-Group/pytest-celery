import pytest

from pytest_celery.api.setup import CeleryTestSetup
from tests.shared.tasks import identity


@pytest.fixture
def function_worker_tasks() -> set:
    from tests.shared import tasks

    return {tasks}


class test_celery_test_setup:
    def test_ready(self, celery_setup: CeleryTestSetup):
        assert identity.s("test_ready").delay().get() == "test_ready"
        assert celery_setup.app
        # if celery_setup.app:
        #     r = celery_setup.app.control.ping()
        #     for response in r:
        #         for _, res in response.items():
        #             assert res["ok"] == "pong"
