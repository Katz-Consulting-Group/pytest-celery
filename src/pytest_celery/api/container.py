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

    @retry(ContainerNotReady)
    def ready(self) -> bool:
        if not super().ready():
            raise ContainerNotReady(self)
        return True

    #     if super().ready():
    #         return self.client is not None
    #     return False

    def teardown(self) -> None:
        pass
