import gc

from pytest_celery.fixtures.backend import CeleryTestBackend


class RedisTestBackend(CeleryTestBackend):
    def teardown(self) -> None:
        gc.collect()  # TODO: Explain why this is needed
        super().teardown()
