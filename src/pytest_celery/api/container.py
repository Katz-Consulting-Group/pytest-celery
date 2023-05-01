from typing import Any
from typing import Optional

from kombu.utils import cached_property
from pytest_docker_tools import wrappers
from pytest_docker_tools.exceptions import ContainerNotReady
from pytest_docker_tools.wrappers.container import wait_for_callable
from retry import retry

from pytest_celery import defaults


class CeleryTestContainer(wrappers.Container):
    @cached_property
    def client(self) -> Any:
        raise NotImplementedError("CeleryTestContainer.client")

    @cached_property
    def celeryconfig(self) -> dict:
        raise NotImplementedError("CeleryTestContainer.celeryconfig")

    @classmethod
    def command(cls) -> list:
        raise NotImplementedError("CeleryTestContainer.command")

    @retry(IndexError, max_delay=defaults.CONTAINER_TIMEOUT)
    def _wait_port(self, port: str) -> int:
        _, p = self.get_addr(port)
        return p

    @property
    def ready_prompt(self) -> Optional[str]:
        return None

    @retry(ContainerNotReady, delay=5, max_delay=defaults.CONTAINER_TIMEOUT)
    def ready(self) -> bool:
        if super().ready():
            if self.ready_prompt is None:
                return True

            try:
                wait_for_callable(
                    f"Waiting for {self.__class__.__name__}::{self.name} to get ready",
                    lambda: self.ready_prompt in self.logs(),
                    timeout=defaults.CONTAINER_TIMEOUT // 2,
                )
                return True
            except TimeoutError:
                if self.ready_prompt not in self.logs():
                    self.restart()
                else:
                    return True

        raise ContainerNotReady(self)

    def teardown(self) -> None:
        pass
