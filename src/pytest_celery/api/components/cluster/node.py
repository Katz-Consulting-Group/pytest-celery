from pytest_docker_tools.exceptions import ContainerNotReady
from pytest_docker_tools.exceptions import TimeoutError
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.utils import cached_property


class CeleryTestNode:
    def __init__(self, container: CeleryTestContainer):
        self._container = container

    @cached_property
    def container(self) -> CeleryTestContainer:
        return self._container

    def ready(self, max_tries: int = defaults.MAX_RETRIES) -> bool:
        tries = 1
        while tries <= max_tries:
            try:
                wait_for_callable(
                    f"Waiting for the node's container to be ready: '{self.container.name}'",
                    self.container.ready,
                    timeout=defaults.READY_TIMEOUT,
                )
                return True
            except TimeoutError:
                tries += 1

        raise ContainerNotReady(
            self.container,
            f"Can't get node to be ready (attempted {tries} times): '{self.container.name}'",
        )

    def config(self, *args: tuple, **kwargs: dict) -> dict:
        return self.container.celeryconfig

    @classmethod
    def default_config(cls) -> dict:
        return {}

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, CeleryTestNode):
            return self.container == __value.container
        return False

    def logs(self) -> str:
        return self.container.logs()

    def kill(self) -> None:
        self.container.kill()
