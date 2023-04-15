from kombu import Connection
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class RabbitMQContainer(CeleryTestContainer):
    __ready_prompt__ = "Server startup complete"

    def ready(self) -> bool:
        ready = False
        if self._full_ready(self.__ready_prompt__, check_client=True):
            c: Connection = self.client()
            try:
                c.connect()
            finally:
                c.release()
        return ready

    def client(self, max_tries: int = defaults.DEFAULT_READY_MAX_RETRIES) -> Connection:
        tries = 1
        while tries <= max_tries:
            try:
                celeryconfig = self.celeryconfig()
                client = Connection(
                    f"amqp://localhost/{celeryconfig['vhost']}",
                    port=celeryconfig["port"],
                )
                return client
            except Exception as e:
                if tries == max_tries:
                    raise e
                tries += 1

    def celeryconfig(self, vhost: str = "/") -> dict:
        wait_for_callable(
            "Waiting for port to be ready",
            lambda: self.get_addr("5672/tcp"),
        )
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
        return defaults.DEFAULT_RABBITMQ_BROKER_ENV

    @classmethod
    def image(cls) -> str:
        return defaults.DEFAULT_RABBITMQ_BROKER_IMAGE

    @classmethod
    def ports(cls) -> dict:
        return defaults.DEFAULT_RABBITMQ_BROKER_PORTS
