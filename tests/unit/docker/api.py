from typing import Any

from pytest_celery import CeleryTestContainer
from pytest_celery import defaults
from pytest_celery.containers.worker import CeleryWorkerContainer


class UnitTestContainer(CeleryTestContainer):
    def client(self, max_tries: int = defaults.DEFAULT_MAX_RETRIES) -> Any:
        return self


class UnitWorkerContainer(CeleryWorkerContainer):
    def client(self, max_tries: int = defaults.DEFAULT_MAX_RETRIES) -> Any:
        return self
