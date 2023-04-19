# mypy: disable-error-code="misc"

import pytest

from pytest_celery import defaults
from pytest_celery.api.components.backend import CeleryBackendCluster
from pytest_celery.api.components.backend import CeleryTestBackend

ALL_CELERY_SESSION_BACKENDS = (
    f"{defaults.CELERY_FIXTURES_PREFIX}_session_{backend}" for backend in defaults.ALL_CELERY_BACKENDS
)
CELERY_SESSION_BACKEND_CLUSTER = f"{defaults.CELERY_FIXTURES_PREFIX}_session_{defaults.CELERY_BACKEND_CLUSTER}"


@pytest.fixture(scope="session", params=ALL_CELERY_SESSION_BACKENDS)
def celery_session_backend(request: pytest.FixtureRequest) -> CeleryTestBackend:
    backend: CeleryTestBackend = request.getfixturevalue(request.param)
    backend.ready()
    yield backend
    backend.teardown()


@pytest.fixture(scope="session")
def celery_session_backend_cluster(celery_session_backend: CeleryTestBackend) -> CeleryBackendCluster:
    cluster = CeleryBackendCluster(celery_session_backend)
    cluster.ready()
    yield cluster
    cluster.teardown()


@pytest.fixture(scope="session")
def celery_session_backend_cluster_config(request: pytest.FixtureRequest) -> dict:
    try:
        cluster: CeleryBackendCluster = request.getfixturevalue(CELERY_SESSION_BACKEND_CLUSTER)
        cluster.ready()
        return cluster.config()
    except pytest.fail.Exception:
        return CeleryBackendCluster.default_config()
