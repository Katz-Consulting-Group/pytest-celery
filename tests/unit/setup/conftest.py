import pytest

from pytest_celery import CeleryTestSetup


@pytest.fixture
def celery_setup(celery_session_setup: CeleryTestSetup) -> CeleryTestSetup:
    return celery_session_setup
