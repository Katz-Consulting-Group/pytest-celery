# mypy: disable-error-code="misc"

import pytest

from pytest_celery import defaults
from pytest_celery.api.components.broker import CeleryBrokerCluster
from pytest_celery.api.components.broker import CeleryTestBroker

ALL_CELERY_SESSION_BROKERS = (
    f"{defaults.CELERY_FIXTURES_PREFIX}_session_{broker}" for broker in defaults.ALL_CELERY_BROKERS
)
CELERY_SESSION_BROKER_CLUSTER = f"{defaults.CELERY_FIXTURES_PREFIX}_session_{defaults.CELERY_BROKER_CLUSTER}"


@pytest.fixture(scope="session", params=ALL_CELERY_SESSION_BROKERS)
def celery_session_broker(request: pytest.FixtureRequest) -> CeleryTestBroker:
    broker: CeleryTestBroker = request.getfixturevalue(request.param)
    broker.ready()
    yield broker
    broker.teardown()


@pytest.fixture(scope="session")
def celery_session_broker_cluster(celery_session_broker: CeleryTestBroker) -> CeleryBrokerCluster:
    cluster = CeleryBrokerCluster(celery_session_broker)
    cluster.ready()
    yield cluster
    cluster.teardown()


@pytest.fixture(scope="session")
def celery_session_broker_cluster_config(
    request: pytest.FixtureRequest,
) -> dict:
    try:
        cluster: CeleryBrokerCluster = request.getfixturevalue(CELERY_SESSION_BROKER_CLUSTER)
        cluster.ready()
        return cluster.config()
    except pytest.fail.Exception:
        return CeleryBrokerCluster.default_config()
