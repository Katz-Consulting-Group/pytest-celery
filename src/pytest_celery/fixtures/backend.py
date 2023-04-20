# mypy: disable-error-code="misc"

import pytest
from retry.api import retry_call

from pytest_celery import defaults
from pytest_celery.api.components.backend import CeleryBackendCluster
from pytest_celery.api.components.backend import CeleryTestBackend


@pytest.fixture(params=defaults.ALL_CELERY_BACKENDS)
def celery_backend(request: pytest.FixtureRequest) -> CeleryTestBackend:  # type: ignore
    backend: CeleryTestBackend = retry_call(
        lambda: request.getfixturevalue(request.param),
        exceptions=defaults.COMPONENT_RETRYABLE_ERRORS,
        delay=defaults.COMPONENT_RETRYABLE_DELAY,
    )
    backend.ready()
    yield backend
    backend.teardown()


@pytest.fixture
def celery_backend_cluster(celery_backend: CeleryTestBackend) -> CeleryBackendCluster:  # type: ignore
    cluster = CeleryBackendCluster(celery_backend)  # type: ignore
    cluster.ready()
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_backend_cluster_config(request: pytest.FixtureRequest) -> dict:
    try:
        use_default_config = pytest.fail.Exception
        assert use_default_config not in defaults.COMPONENT_RETRYABLE_ERRORS
        cluster: CeleryBackendCluster = retry_call(
            lambda: request.getfixturevalue(defaults.CELERY_BACKEND_CLUSTER),
            exceptions=defaults.RETRYABLE_ERRORS,
            delay=defaults.RETRYABLE_DELAY,
        )
        cluster.ready()
        return cluster.config()
    except use_default_config:
        return CeleryBackendCluster.default_config()
