from pytest_celery import CeleryTestSetup


class test_celery_test_setup:
    def test_ready(self, celery_setup: CeleryTestSetup):
        assert celery_setup.ready()
