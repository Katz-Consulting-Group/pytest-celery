from typing import Optional

from kombu.utils import cached_property
from redis import BlockingConnectionPool
from redis import StrictRedis as Redis
from retry.api import retry_call

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class RedisContainer(CeleryTestContainer):
    __ready_prompt__ = "Ready to accept connections"

    @cached_property
    def client(self) -> Optional[Redis]:
        if self._client:
            return self._client

        pool = retry_call(
            BlockingConnectionPool.from_url,
            fargs=(self.celeryconfig["local_url"],),
            fkwargs={
                "max_connections": self.app_transport_options()["max_connections"],
                "timeout": self.app_transport_options()["timeout"],
                "decode_responses": True,
            },
            exceptions=defaults.RETRYABLE_ERRORS,
        )
        self._client = Redis(connection_pool=pool)
        return self._client

    @property
    def celeryconfig(self) -> dict:
        return {
            "url": self.url,
            "local_url": self.local_url,
            "hostname": self.hostname,
            "port": self.port,
            "vhost": self.vhost,
        }

    @property
    def url(self) -> str:
        return f"redis://{self.hostname}/{self.vhost}"

    @property
    def local_url(self) -> str:
        return f"redis://localhost:{self.port}/{self.vhost}"

    @property
    def hostname(self) -> str:
        return self.attrs["Config"]["Hostname"]

    @property
    def port(self) -> int:
        return self._wait_port("6379/tcp")

    @property
    def vhost(self) -> str:
        return "0"

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

    @classmethod
    def app_transport_options(cls) -> dict:
        return {
            "max_connections": int(cls.command()[-1]),
            # "max_connections": None,
            "timeout": None,
            "pool_class": "redis.BlockingConnectionPool",
        }

    @classmethod
    def command(cls) -> list:
        return ["redis-server", "--maxclients", "10000"]
