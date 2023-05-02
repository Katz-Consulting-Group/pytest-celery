from typing import Any
from typing import Optional

from kombu.utils import cached_property
from pytest_docker_tools import wrappers
from pytest_docker_tools.exceptions import ContainerNotReady
from retry import retry


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

    def teardown(self) -> None:
        pass

    @property
    def ready_prompt(self) -> Optional[str]:
        return None

    @retry(IndexError, delay=10, tries=5)
    def _wait_port(self, port: str) -> int:
        _, p = self.get_addr(port)
        return p

    @retry(ContainerNotReady, delay=10, tries=5)
    def _wait_ready(self) -> bool:
        if self.ready_prompt in self.logs():
            return True
        raise ContainerNotReady(self)

    def ready(self) -> bool:
        if not super().ready():
            return False

        if self.ready_prompt is None:
            return True

        try:
            self._wait_ready()
            return True
        except ContainerNotReady:
            return False
