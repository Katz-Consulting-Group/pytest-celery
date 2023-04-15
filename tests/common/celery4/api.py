from typing import Any

from pytest_celery import defaults
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.containers.worker import CeleryWorkerContainer


class Celery4TestWorker(CeleryTestWorker):
    pass


class Worker4Container(CeleryWorkerContainer):
    def client(self, max_tries: int = defaults.DEFAULT_READY_MAX_RETRIES) -> Any:
        return self
