# from pytest_docker_tools.wrappers.container import wait_for_callable

# from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class CeleryTestNode:
    def __init__(self, container: CeleryTestContainer):
        self._container = container

    @property
    def container(self) -> CeleryTestContainer:
        return self._container

    def ready(self) -> bool:
        # wait_for_callable(
        #     f">>> Waiting for the node's container to be ready: '{self.__class__.__name__}::{self.container.name}'",
        #     self.container.ready,
        #     timeout=defaults.READY_TIMEOUT,
        # )
        return self.container.ready()

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

    def kill(self) -> None:
        self.container.kill()

    def teardown(self) -> None:
        pass
