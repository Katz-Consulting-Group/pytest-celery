from typing import Any

from kombu.utils import cached_property
from pytest_docker_tools import wrappers
from pytest_docker_tools.exceptions import ContainerNotReady
from retry import retry

from pytest_celery import defaults


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

    @retry(IndexError, delay=2, max_delay=defaults.READY_TIMEOUT)
    def _wait_port(self, port: str) -> int:
        _, p = self.get_addr(port)
        return p

    @property
    def ready_prompt(self) -> str:
        return ""

    # @retry(ContainerNotReady, delay=2, max_delay=defaults.READY_TIMEOUT)
    # def ready(self) -> bool:
    #     return super().ready()
    #     if not super().ready():
    #         raise ContainerNotReady(self)
    #     return True
    #     if super().ready():
    #         return self.client is not None
    #     return False

    def teardown(self) -> None:
        pass
