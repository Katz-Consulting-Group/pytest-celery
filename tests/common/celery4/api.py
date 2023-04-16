from typing import Any

from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.containers.worker import CeleryWorkerContainer
from pytest_celery.utils import cached_property


class Celery4TestWorker(CeleryTestWorker):
    pass


class Worker4Container(CeleryWorkerContainer):
    @cached_property
    def client(self) -> Any:
        return self

    @classmethod
    def version(cls) -> str:
        return "4.4.7"
