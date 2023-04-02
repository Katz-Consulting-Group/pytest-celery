from pytest_docker_tools.exceptions import ContainerNotReady
from pytest_docker_tools.exceptions import TimeoutError
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class CeleryTestNode:
    def __init__(self, container: CeleryTestContainer):
        self._container = container

    @property
    def container(self) -> CeleryTestContainer:
        return self._container

    def ready(self, max_tries: int = defaults.DEFAULT_READY_MAX_RETRIES) -> bool:
        tries = 0
        while tries < max_tries:
            try:
                wait_for_callable(
                    f"Waiting for node to be ready: {self.container.name}",
                    self.container.ready,
                    timeout=defaults.DEFAULT_READY_TIMEOUT,
                )
                return True
            except TimeoutError:
                tries += 1

        raise ContainerNotReady(
            self.container,
            f"Can't get node to be ready (attempted {max_tries} times): {self.container.name}",
        )
