from pytest_celery.api.components.worker.node import CeleryTestWorker


class test_base_test_worker:
    def test_ready(self, celery_setup_worker: CeleryTestWorker):
        assert celery_setup_worker.ready()
