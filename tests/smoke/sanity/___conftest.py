import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr
from retry.api import retry_call

from pytest_celery import defaults
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.containers.worker import CeleryWorkerContainer
from tests.common.celery4.fixtures import Celery4WorkerContainer
from tests.common.celery4.fixtures import celery4_worker_image  # noqa
from tests.smoke.conftest import SmokeWorkerContainer


class SessionWorkerContainer(SmokeWorkerContainer):
    @classmethod
    def worker_name(cls) -> str:
        return CeleryWorkerContainer.worker_name() + "-session-worker"

    @classmethod
    def worker_queue(cls) -> str:
        return CeleryWorkerContainer.worker_queue() + "-smoke-tests-session-queue"


session_worker_image = build(
    path="src/pytest_celery/components/worker",
    tag="pytest-celery/components/worker:session",
    buildargs=SessionWorkerContainer.buildargs(),
)

session_worker_container = container(
    image="{session_worker_image.id}",
    scope="session",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=SessionWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture
def session_worker(
    session_worker_container: CeleryWorkerContainer,
    celery_setup_app: Celery,
) -> CeleryTestWorker:
    worker = CeleryTestWorker(session_worker_container, app=celery_setup_app)
    worker.ready()
    yield worker
    worker.teardown()


celery4_session_worker_container = container(
    image="{celery4_worker_image.id}",
    scope="session",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=Celery4WorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery4_session_worker(
    celery4_session_worker_container: CeleryWorkerContainer,
    celery_setup_app: Celery,
) -> CeleryTestWorker:
    worker = CeleryTestWorker(celery4_session_worker_container, app=celery_setup_app)
    worker.ready()
    yield worker


@pytest.fixture(
    # Each param item is a list of workers to be used in the cluster
    params=[
        ["session_worker"],
        ["celery4_session_worker"],
        ["session_worker", "celery4_worker"],
    ]
)
def celery_worker_cluster(request: pytest.FixtureRequest) -> CeleryWorkerCluster:
    nodes = tuple(
        retry_call(
            lambda: [request.getfixturevalue(worker) for worker in request.param],
            exceptions=defaults.RETRY_ERRORS,
            tries=defaults.MAX_TRIES,
            delay=defaults.DELAY_SECONDS,
            max_delay=defaults.MAX_DELAY_SECONDS,
        )
    )
    cluster = CeleryWorkerCluster(*nodes)
    cluster.ready()
    yield cluster
    cluster.teardown()
