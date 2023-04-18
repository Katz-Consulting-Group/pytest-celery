from functools import partial
from typing import Any

from pytest_docker_tools import wrappers
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery import defaults


class CeleryTestContainer(wrappers.Container):
    @property
    def client(self) -> Any:
        raise NotImplementedError("CeleryTestContainer.client")

    @property
    def celeryconfig(self) -> dict:
        raise NotImplementedError("CeleryTestContainer.celeryconfig")

    def _port(self, port: str) -> int:
        wait_for_callable(
            f">>> Waiting for port '{port}' to be ready: '{self.__class__.__name__}::{self.name}'",
            partial(self.get_addr, port),
            timeout=defaults.READY_TIMEOUT,
        )
        _, p = self.get_addr(port)
        return p

    def _full_ready(self, match_log: str = "", check_client: bool = True) -> bool:
        wait_for_callable(
            f">>> Waiting for container to warm up: '{self.__class__.__name__}::{self.name}'",
            super().ready,
            timeout=defaults.READY_TIMEOUT,
        )
        ready = super().ready()

        if ready:
            if match_log:
                ready = match_log in self.logs()
            if check_client:
                wait_for_callable(
                    f">>> Waiting for client to be ready: '{self.__class__.__name__}::{self.name}'",
                    lambda: self.client is not None,
                    timeout=defaults.READY_TIMEOUT,
                )
                ready = ready and self.client is not None
        return ready
