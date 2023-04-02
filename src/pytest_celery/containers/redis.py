from time import sleep

from redis import Redis

from pytest_celery.api.container import CeleryTestContainer


class RedisContainer(CeleryTestContainer):
    def ready(self) -> bool:
        return super().ready() and self.client()

    def client(self) -> Redis:
        celeryconfig = self.celeryconfig()
        client = Redis.from_url(
            celeryconfig["local_url"],
            decode_responses=True,
        )
        return client

    def celeryconfig(self, vhost="0") -> dict:
        while not self.ports["6379/tcp"]:
            sleep(0.1)
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
