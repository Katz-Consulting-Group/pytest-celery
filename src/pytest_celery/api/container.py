from typing import Any

from pytest_docker_tools import wrappers
from pytest_docker_tools.wrappers.container import wait_for_callable
from retry import retry

from pytest_celery import defaults


class CeleryTestContainer(wrappers.Container):
    def __init__(self, *args, **kwargs):  # type: ignore
        super().__init__(*args, **kwargs)
        self._client: Any = None  # type: ignore

    @property
    def client(self) -> Any:
        raise NotImplementedError("CeleryTestContainer.client")

    @property
    def celeryconfig(self) -> dict:
        raise NotImplementedError("CeleryTestContainer.celeryconfig")

    @classmethod
    def command(cls) -> list:
        raise NotImplementedError("CeleryTestContainer.command")

    @retry(IndexError)
    def _wait_port(self, port: str) -> int:
        _, p = self.get_addr(port)
        return p

    @retry(defaults.RETRYABLE_ERRORS)
    def _full_ready(self, match_log: str = "", check_client: bool = True) -> bool:
        wait_for_callable(
            f">>> Warming up: '{self.__class__.__name__}::{self.name}'",
            super().ready,
        )
        ready = super().ready()

        if ready:
            if match_log:
                ready = match_log in self.logs()
            if check_client:
                ready = ready and self.client is not None
        return ready

    def teardown(self) -> None:
        pass
