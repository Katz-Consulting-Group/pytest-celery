from celery import Celery

from pytest_celery import defaults
from pytest_celery.api.components.backend.cluster import CeleryBackendCluster
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster


class CeleryTestSetup:
    def __init__(
        self,
        worker_cluster: CeleryWorkerCluster,
        broker_cluster: CeleryBrokerCluster,
        backend_cluster: CeleryBackendCluster,
        app: Celery = None,
    ):
        self._worker_cluster = worker_cluster
        self._broker_cluster = broker_cluster
        self._backend_cluster = backend_cluster
        self._app = app

        from pytest_celery.components.worker.common import ping

        self.ping = ping

    def __len__(self) -> int:
        return len(self._worker_cluster) + len(self._broker_cluster) + len(self._backend_cluster)

    @property
    def app(self) -> Celery:
        return self._app

    @property
    def worker_cluster(self) -> CeleryWorkerCluster:
        return self._worker_cluster

    @property
    def broker_cluster(self) -> CeleryBrokerCluster:
        return self._broker_cluster

    @property
    def backend_cluster(self) -> CeleryBackendCluster:
        return self._backend_cluster

    def ready(self, ping: bool = False) -> bool:
        ready = all(
            [
                self.worker_cluster.ready(),
                self.broker_cluster.ready(),
                self.backend_cluster.ready(),
            ]
        )

        r = self.app.control.ping()
        ready = all(
            [
                ready,
                all([all([res["ok"] == "pong" for _, res in response.items()]) for response in r]),
            ]
        )

        if not ping:
            return ready

        queue = self.worker_cluster[0].worker_queue  # type: ignore
        res = self.ping.s().apply_async(queue=queue)
        return ready and res.get(timeout=defaults.RESULT_TIMEOUT) == "pong"

    @classmethod
    def name(cls) -> str:
        return defaults.DEFAULT_WORKER_APP_NAME

    @classmethod
    def config(cls, celery_worker_cluster_config: dict) -> dict:
        if not celery_worker_cluster_config:
            raise ValueError("celery_worker_cluster_config is empty")

        celery_broker_cluster_config: dict = celery_worker_cluster_config["celery_broker_cluster_config"]
        celery_backend_cluster_config: dict = celery_worker_cluster_config["celery_backend_cluster_config"]
        return {
            "broker_url": ";".join(celery_broker_cluster_config["local_urls"]),
            "result_backend": ";".join(celery_backend_cluster_config["local_urls"]),
        }

    @classmethod
    def create_setup_app(cls, celery_setup_config: dict, celery_setup_app_name: str) -> Celery:
        if not celery_setup_config:
            raise ValueError("celery_setup_config is empty")

        if not celery_setup_app_name:
            raise ValueError("celery_setup_app_name is empty")

        app = Celery(celery_setup_app_name)
        app.config_from_object(celery_setup_config)
        return app

    def chords_allowed(self) -> bool:
        try:
            self.app.backend.ensure_chords_allowed()
        except NotImplementedError:
            return False

        if any([v.startswith("4.") for v in self.worker_cluster.versions]):
            return False

        return True

    def teardown(self) -> None:
        self.worker_cluster.teardown()
        self.broker_cluster.teardown()
        self.backend_cluster.teardown()
