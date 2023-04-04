from time import sleep

from kombu import Connection

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class RabbitMQContainer(CeleryTestContainer):
    def ready(self) -> bool:
        if super().ready():
            return True if self.client() else False
        return False

    def client(self) -> Connection:
        celeryconfig = self.celeryconfig()
        client = Connection(
            f"amqp://localhost/{celeryconfig['vhost']}",
            port=celeryconfig["port"],
        )
        return client

    def celeryconfig(self, vhost="/") -> dict:
        while not self.ports["5672/tcp"]:
            sleep(0.1)
        _, port = self.get_addr("5672/tcp")

        hostname = self.attrs["Config"]["Hostname"]
        url = f"amqp://{hostname}/{vhost}"
        local_url = f"amqp://localhost:{port}/{vhost}"
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
        return defaults.RABBITMQ_FUNCTION_BROKER_ENV

    @classmethod
    def image(cls) -> str:
        return defaults.RABBITMQ_FUNCTION_BROKER_IMAGE

    @classmethod
    def ports(cls) -> dict:
        return defaults.RABBITMQ_FUNCTION_BROKER_PORTS
