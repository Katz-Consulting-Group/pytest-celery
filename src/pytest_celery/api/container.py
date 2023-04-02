from abc import abstractmethod
from typing import Any

from pytest_docker_tools import wrappers
from pytest_docker_tools.exceptions import ContainerNotReady
from pytest_docker_tools.exceptions import TimeoutError
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery import defaults


class CeleryTestContainer(wrappers.Container):
    @abstractmethod
    def client(self) -> Any:
        NotImplementedError("CeleryTestContainer.client")

    @abstractmethod
    def celeryconfig(self) -> dict:
        NotImplementedError("CeleryTestContainer.celeryconfig")

    def ready(self):
        max_tries = defaults.DEFAULT_READY_MAX_RETRIES
        tries = 0
        while tries < max_tries:
            try:
                wait_for_callable(
                    f"Waiting for test container to be ready: {self.name}",
                    super().ready,
                    timeout=defaults.DEFAULT_READY_TIMEOUT,
                )
                return True
            except TimeoutError:
                tries += 1

        raise ContainerNotReady(
            self,
            f"Can't get test container to be ready (attempted {max_tries} times): {self.name}",
        )
