from pytest_celery import BaseTestWorker


class test_base_test_worker:
    def test_ready(self, celery_test_worker: BaseTestWorker):
        assert celery_test_worker.ready()
