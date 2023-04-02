from pytest_celery import CeleryTestSetup
from tests.shared.tasks import identity
from tests.smoke.tasks import add


class test_acceptance:
    def test_sanity(self, celery_setup: CeleryTestSetup):
        assert identity.s("test_ready").delay().get() == "test_ready"
        assert add.s(1, 2).delay().get() == 3
