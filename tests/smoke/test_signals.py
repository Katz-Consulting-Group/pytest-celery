from time import sleep

import pytest
from celery.signals import after_task_publish
from celery.signals import before_task_publish

from pytest_celery import CeleryTestSetup
from pytest_celery import defaults
from pytest_celery.api.components.worker.node import CeleryTestWorker
from tests.common.tasks import identity
from tests.smoke.tasks import add


@pytest.fixture
def default_worker_signals(default_worker_signals: set) -> set:
    from tests.smoke import signal_handlers

    default_worker_signals.add(signal_handlers)
    yield default_worker_signals


class test_signals:
    def test_before_task_publish(self, celery_setup: CeleryTestSetup):
        signal_was_called = False

        @before_task_publish.connect
        def before_task_publish_handler(*args, **kwargs):
            nonlocal signal_was_called
            signal_was_called = True

        assert signal_was_called is False
        queue = celery_setup.worker_cluster[0].worker_queue
        res = identity.s("test_before_task_publish").apply_async(queue=queue)
        assert res.get(timeout=defaults.RESULT_TIMEOUT) == "test_before_task_publish"

        if len(celery_setup.worker_cluster) > 1:
            queue = celery_setup.worker_cluster[1].worker_queue

        res = add.s(1, 2).apply_async(queue=queue)
        assert res.get(timeout=defaults.RESULT_TIMEOUT) == 3
        assert signal_was_called is True

    def test_after_task_publish(self, celery_setup: CeleryTestSetup):
        signal_was_called = False

        @after_task_publish.connect
        def after_task_publish_handler(*args, **kwargs):
            nonlocal signal_was_called
            signal_was_called = True

        assert signal_was_called is False
        queue = celery_setup.worker_cluster[0].worker_queue
        res = identity.s("test_after_task_publish").apply_async(queue=queue)
        assert res.get(timeout=defaults.RESULT_TIMEOUT) == "test_after_task_publish"

        if len(celery_setup.worker_cluster) > 1:
            queue = celery_setup.worker_cluster[1].worker_queue

        res = add.s(1, 2).apply_async(queue=queue)
        assert res.get(timeout=defaults.RESULT_TIMEOUT) == 3
        assert signal_was_called is True

    def test_worker_init(self, celery_setup: CeleryTestSetup):
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            logs = worker.logs()
            assert "worker_init_handler" in logs

    def test_worker_process_init(self, celery_setup: CeleryTestSetup):
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            logs = worker.logs()
            assert "worker_process_init_handler" in logs

    def test_worker_process_shutdown(self, celery_setup: CeleryTestSetup):
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            worker.app.control.broadcast("shutdown")
            sleep(2)  # wait for logs to be flushed
            logs = worker.logs()
            assert "worker_process_shutdown_handler" in logs

    def test_worker_ready(self, celery_setup: CeleryTestSetup):
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            logs = worker.logs()
            assert "worker_ready_handler" in logs

    def test_worker_shutdown(self, celery_setup: CeleryTestSetup):
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            worker.app.control.broadcast("shutdown")
            sleep(2)  # wait for logs to be flushed
            logs = worker.logs()
            assert "worker_shutdown_handler" in logs
