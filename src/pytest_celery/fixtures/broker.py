# mypy: disable-error-code="misc"

import pytest
from retry.api import retry_call

from pytest_celery import defaults
from pytest_celery.api.components.broker import CeleryBrokerCluster
from pytest_celery.api.components.broker import CeleryTestBroker


@pytest.fixture(params=defaults.ALL_CELERY_BROKERS)
def celery_broker(request: pytest.FixtureRequest) -> CeleryTestBroker:  # type: ignore
    broker: CeleryTestBroker = retry_call(
        lambda: request.getfixturevalue(request.param),
        exceptions=defaults.COMPONENT_RETRYABLE_ERRORS,
        delay=defaults.COMPONENT_RETRYABLE_DELAY,
    )
    broker.ready()
    yield broker
    broker.teardown()


@pytest.fixture
def celery_broker_cluster(celery_broker: CeleryTestBroker) -> CeleryBrokerCluster:  # type: ignore
    cluster = CeleryBrokerCluster(celery_broker)  # type: ignore
    cluster.ready()
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_broker_cluster_config(request: pytest.FixtureRequest) -> dict:
    try:
        use_default_config = pytest.fail.Exception
        assert use_default_config not in defaults.RETRYABLE_ERRORS
        cluster: CeleryBrokerCluster = retry_call(
            lambda: request.getfixturevalue(defaults.CELERY_BROKER_CLUSTER),
            exceptions=defaults.RETRYABLE_ERRORS + (Exception,),
            delay=defaults.RETRYABLE_DELAY,
        )
        cluster.ready()
        return cluster.config()
    except use_default_config:
        return CeleryBrokerCluster.default_config()
