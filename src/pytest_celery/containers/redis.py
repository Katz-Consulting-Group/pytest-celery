from time import sleep
from typing import Union

from pytest_docker_tools.wrappers.container import wait_for_callable
from redis import Redis

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.utils import cached_property


class RedisContainer(CeleryTestContainer):
    __ready_prompt__ = "Ready to accept connections"

    def ready(self) -> bool:
        return self._full_ready(self.__ready_prompt__, check_client=False)

    def _full_ready(self, match_log: str = "", check_client: bool = True) -> bool:
        ready = super()._full_ready(match_log, check_client)
        if ready and check_client:
            c: Redis = self.client  # type: ignore
            if c.ping():
                c.set("ready", "1")
                ready = c.get("ready") == "1"
                c.delete("ready")
        return ready

    @cached_property
    def client(self) -> Union[Redis, None]:
        tries = 1
        max_tries = defaults.DEFAULT_MAX_RETRIES
        while tries <= max_tries:
            try:
                celeryconfig = self.celeryconfig()
                client = Redis.from_url(
                    celeryconfig["local_url"],
                    decode_responses=True,
                )
                return client
            except Exception as e:
                if tries == max_tries:
                    raise e
                sleep(5 * tries)
                tries += 1
        return None

    def celeryconfig(self, vhost: str = "0") -> dict:
        try:
            wait_for_callable(
                "Waiting for port to be ready",
                lambda: self.get_addr("6379/tcp"),
            )
        except IndexError:
            sleep(1)

        _, port = self.get_addr("6379/tcp")

        hostname = self.attrs["Config"]["Hostname"]
        url = f"redis://{hostname}/{vhost}"
        local_url = f"redis://localhost:{port}/{vhost}"
        return {
            "url": url,
            "local_url": local_url,
            "hostname": hostname,
            "port": port,
            "vhost": vhost,
        }

    @classmethod
    def version(cls) -> str:
        return cls.image().split(":")[-1]

    @classmethod
    def env(cls) -> dict:
        return defaults.DEFAULT_REDIS_BACKEND_ENV

    @classmethod
    def image(cls) -> str:
        return defaults.DEFAULT_REDIS_BACKEND_IMAGE

    @classmethod
    def ports(cls) -> dict:
        return defaults.DEFAULT_REDIS_BACKEND_PORTS
