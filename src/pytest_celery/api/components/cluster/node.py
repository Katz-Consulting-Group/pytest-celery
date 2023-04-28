import gc

from pytest_docker_tools.exceptions import ContainerNotReady
from pytest_docker_tools.wrappers.container import wait_for_callable
from retry import retry

from pytest_celery.api.container import CeleryTestContainer


class CeleryTestNode:
    def __init__(self, container: CeleryTestContainer):
        self._container = container

    @property
    def container(self) -> CeleryTestContainer:
        return self._container

    @retry((ContainerNotReady, TimeoutError), delay=5, max_delay=60)
    def ready(self) -> bool:
        if self.container.ready():
            if self.container.ready_prompt:
                wait_for_callable(
                    f"Waiting on ready prompt log from: {self.__class__.__name__}::{self.name()}",
                    lambda: self.container.ready_prompt in self.logs(),
                )
            return True
        raise ContainerNotReady(self.container)

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

    def name(self) -> str:
        return self.container.name

    def kill(self) -> None:
        self.container.kill()

    def teardown(self) -> None:
        gc.collect()  # TODO: Explain why this is needed
        self.container.teardown()
