from pytest_celery.api.container import CeleryTestContainer


class CeleryWorkerContainer(CeleryTestContainer):
    def client(self):
        return self
