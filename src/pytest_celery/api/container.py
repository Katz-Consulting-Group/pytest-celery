from typing import Any

from pytest_docker_tools import wrappers
from pytest_docker_tools.wrappers.container import wait_for_callable
from retry import retry
from retry.api import retry_call

from pytest_celery import defaults


class CeleryTestContainer(wrappers.Container):
    __ready_prompt__ = ""

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

    def ready(self) -> bool:
        return self._full_ready(self.__ready_prompt__)

    @retry(defaults.RETRYABLE_ERRORS)
    def _full_ready(self, match_log: str = "", check_client: bool = True) -> bool:
        retry_call(
            wait_for_callable,
            fargs=(
                f">>> Warming up: '{self.__class__.__name__}::{self.name}'",
                super().ready,
            ),
            exceptions=defaults.READY_RETRYABLE_ERRORS,
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
