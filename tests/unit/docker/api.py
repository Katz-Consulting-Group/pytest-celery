from pytest_celery import CeleryTestContainer
from pytest_celery.containers.worker import CeleryWorkerContainer


class UnitTestContainer(CeleryTestContainer):
    def client(self):
        return self


class UnitWorkerContainer(CeleryWorkerContainer):
    def _full_ready(self, match_log: str = "", check_client: bool = True) -> bool:
        return super()._full_ready(match_log=match_log, check_client=False)
