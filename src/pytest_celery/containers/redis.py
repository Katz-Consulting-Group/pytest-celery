from time import sleep
from typing import Union

from pytest_docker_tools.wrappers.container import wait_for_callable
from redis import Redis

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class RedisContainer(CeleryTestContainer):
    def ready(self) -> bool:
        ready = False
        if self._full_ready("Ready to accept connections", check_client=True):
            c: Redis = self.client()  # type: ignore
            if c.ping():
                c.set("ready", "1")
                ready = c.get("ready") == "1"
                c.delete("ready")
        return ready

    def client(self, max_tries: int = defaults.DEFAULT_READY_MAX_RETRIES) -> Union[Redis, None]:
        tries = 1
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
                tries += 1
                sleep(5)
        return None

    def celeryconfig(self, vhost: str = "0") -> dict:
        wait_for_callable(
            "Waiting for port to be ready",
            lambda: self.get_addr("6379/tcp"),
        )
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
