# mypy: disable-error-code="misc"

import pytest
from retry import retry

from pytest_celery import defaults
from pytest_celery.api.components.broker import CeleryBrokerCluster
from pytest_celery.api.components.broker import CeleryTestBroker


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture(params=defaults.ALL_CELERY_BROKERS)
def celery_broker(request: pytest.FixtureRequest) -> CeleryTestBroker:  # type: ignore
    broker: CeleryTestBroker = request.getfixturevalue(request.param)
    broker.ready()
    yield broker
    broker.teardown()


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture
def celery_broker_cluster(celery_broker: CeleryTestBroker) -> CeleryBrokerCluster:  # type: ignore
    cluster = CeleryBrokerCluster(celery_broker)  # type: ignore
    cluster.ready()
    yield cluster
    cluster.teardown()


@retry(defaults.RETRYABLE_ERRORS)
@pytest.fixture
def celery_broker_cluster_config(request: pytest.FixtureRequest) -> dict:
    try:
        use_default_config = pytest.fail.Exception
        cluster: CeleryBrokerCluster = request.getfixturevalue(defaults.CELERY_BROKER_CLUSTER)
        cluster.ready()
        return cluster.config()
    except use_default_config:
        return CeleryBrokerCluster.default_config()
