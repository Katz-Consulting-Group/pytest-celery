from typing import Any

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
    def ready_prompt(self) -> str:
        return ""

    @retry(ContainerNotReady, delay=3, max_delay=defaults.CONTAINER_TIMEOUT)
    def ready(self) -> bool:
        if super().ready():
            if self.ready_prompt:
                wait_for_callable(
                    f"Waiting for logs in: {self.__class__.__name__}::{self.name}",
                    self.logs,
                    timeout=5,
                )
                if self.ready_prompt in self.logs():
                    return True
            else:
                return True
        raise ContainerNotReady(self)

    def teardown(self) -> None:
        pass
