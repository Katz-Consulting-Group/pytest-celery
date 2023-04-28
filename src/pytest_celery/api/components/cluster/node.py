import gc

from pytest_docker_tools.exceptions import ContainerNotReady
from pytest_docker_tools.wrappers.container import wait_for_callable
from retry import retry
from retry.api import retry_call

from pytest_celery.api.container import CeleryTestContainer


class CeleryTestNode:
    def __init__(self, container: CeleryTestContainer):
        self._container = container

    @property
    def container(self) -> CeleryTestContainer:
        return self._container

    @retry(ContainerNotReady, delay=5, max_delay=60)
    def ready(self) -> bool:
        if self.container.ready():
            if self.container.ready_prompt:
                retry_call(
                    wait_for_callable,
                    fargs=(
                        f"Waiting for ready prompt log in: {self.__class__.__name__}::{self.name()}",
                        lambda: self.container.ready_prompt in self.logs(),
                    ),
                    exceptions=TimeoutError,
                    tries=3,
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
