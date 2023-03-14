import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import RabbitMQContainer
from pytest_celery import RedisContainer
from pytest_celery import defaults


class test_redis_container_settings:
    @pytest.mark.parametrize(
        "container, expected_image, expected_ports",
        [
            (
                lazy_fixture(defaults.REDIS_FUNCTION_BACKEND),
                defaults.REDIS_FUNCTION_BACKEND_IMAGE,
                defaults.REDIS_FUNCTION_BACKEND_PORTS,
            ),
            (
                lazy_fixture(defaults.REDIS_FUNCTION_BROKER),
                defaults.REDIS_FUNCTION_BROKER_IMAGE,
                defaults.REDIS_FUNCTION_BROKER_PORTS,
            ),
        ],
    )
    def test_defaults(self, container: RedisContainer, expected_image: str, expected_ports: dict):
        attrs = container.attrs
        assert attrs["Config"]["Image"] == expected_image
        assert attrs["Config"]["ExposedPorts"].keys() == expected_ports.keys()


class test_rabbitmq_container_settings:
    @pytest.mark.parametrize(
        "container, expected_image",
        [
            (
                lazy_fixture(defaults.RABBITMQ_FUNCTION_BROKER),
                defaults.RABBITMQ_FUNCTION_BROKER_IMAGE,
            ),
        ],
    )
    def test_defaults(self, container: RabbitMQContainer, expected_image: str):
        attrs = container.attrs
        assert attrs["Config"]["Image"] == expected_image
