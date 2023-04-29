from typing import Any

from kombu.utils import cached_property
from pytest_docker_tools import wrappers
from pytest_docker_tools.exceptions import ContainerNotReady
from retry import retry


class CeleryTestContainer(wrappers.Container):
    def __init__(self, *args, **kwargs):  # type: ignore
        super().__init__(*args, **kwargs)

    @cached_property
    def client(self) -> Any:
        raise NotImplementedError("CeleryTestContainer.client")

    @cached_property
    def celeryconfig(self) -> dict:
        raise NotImplementedError("CeleryTestContainer.celeryconfig")

    @classmethod
    def command(cls) -> list:
        raise NotImplementedError("CeleryTestContainer.command")

    @retry(IndexError)
    def _wait_port(self, port: str) -> int:
        _, p = self.get_addr(port)
        return p

    @property
    def ready_prompt(self) -> str:
        return ""

    @retry(ContainerNotReady, max_delay=300)
    def ready(self) -> bool:
        if super().ready():
            if self.ready_prompt:
                if self.ready_prompt in self.logs():
                    return True
            else:
                return True
        raise ContainerNotReady(self)

    def teardown(self) -> None:
        pass
