from typing import Union

import memcache
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class MemcachedContainer(CeleryTestContainer):
    def ready(self) -> bool:
        ready = self._full_ready(check_client=True)
        if ready:
            c: memcache.Client = self.client()
            if c.get_stats():
                c.set("ready", True)
                return bool(c.get("ready"))
        return False

    def client(self, max_tries: int = defaults.DEFAULT_READY_MAX_RETRIES) -> Union[memcache.Client, None]:
        tries = 1
        while tries <= max_tries:
            try:
                celeryconfig = self.celeryconfig()
                connection_strings = [f"{celeryconfig['local_url'].split('://')[-1]}"]
                client = memcache.Client(connection_strings)
                return client
            except Exception as e:
                if tries == max_tries:
                    raise e
                tries += 1
        return None

    def celeryconfig(self, vhost: str = "0") -> dict:
        wait_for_callable(
            "Waiting for port to be ready",
            lambda: self.get_addr("11211/tcp"),
        )
        _, port = self.get_addr("11211/tcp")

        hostname = self.attrs["Config"]["Hostname"]
        url = f"cache+memcached://{hostname}"
        local_url = f"memcached://localhost:{port}"
        return {
            "url": url,
            "local_url": local_url,
            "hostname": hostname,
            "port": port,
            "vhost": None,
        }

    @classmethod
    def version(cls) -> str:
        return cls.image().split(":")[-1]

    @classmethod
    def env(cls) -> dict:
        return defaults.DEFAULT_MEMCACHED_BACKEND_ENV

    @classmethod
    def image(cls) -> str:
        return defaults.DEFAULT_MEMCACHED_BACKEND_IMAGE

    @classmethod
    def ports(cls) -> dict:
        return defaults.DEFAULT_MEMCACHED_BACKEND_PORTS
