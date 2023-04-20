"""
This module contains all the default values and settings.
These values are used by the pytest-celery plugin to configure the
components fixtures. You can override these values by hooking to the
matchin fixture and returning your own value.
"""


from typing import Any

import amqp
import docker
import pytest_docker_tools
import redis
import requests
from celery.exceptions import TimeoutError as CeleryTimeoutError
from pytest_docker_tools import network
from retry import retry

##########
# Docker
##########

READY_TIMEOUT = 30
RESULT_TIMEOUT = 30

DOCKER_RETRYABLE_ERRORS = (
    docker.errors.NotFound,
    docker.errors.APIError,
    requests.exceptions.HTTPError,
)

REDIS_RETRYABLE_ERRORS = DOCKER_RETRYABLE_ERRORS + (
    TimeoutError,
    ConnectionError,
    ConnectionRefusedError,
    BrokenPipeError,
    redis.exceptions.ConnectionError,
    redis.exceptions.TimeoutError,
)

NETWORK_RETRYABLE_ERRORS = DOCKER_RETRYABLE_ERRORS + (
    TimeoutError,
    requests.exceptions.Timeout,
    requests.exceptions.RetryError,
    pytest_docker_tools.exceptions.ContainerNotReady,
    pytest_docker_tools.exceptions.TimeoutError,
)


READY_RETRYABLE_ERRORS = (
    NETWORK_RETRYABLE_ERRORS
    + REDIS_RETRYABLE_ERRORS
    + (
        ConnectionError,
        requests.exceptions.ConnectionError,
        amqp.exceptions.NotFound,
        CeleryTimeoutError,
    )
)
PORT_RETRYABLE_ERRORS = READY_RETRYABLE_ERRORS + (IndexError,)
RETRYABLE_ERRORS = READY_RETRYABLE_ERRORS
COMPONENT_RETRYABLE_ERRORS = RETRYABLE_ERRORS + (Exception,)

DELAY = 0.5
READY_RETRYABLE_DELAY = DELAY or 5
NETWORK_RETRYABLE_DELAY = DELAY or 5
PORT_RETRYABLE_DELAY = DELAY or 5
RETRYABLE_DELAY = DELAY or 5
COMPONENT_RETRYABLE_DELAY = DELAY or 5


@retry(
    NETWORK_RETRYABLE_ERRORS,
    delay=NETWORK_RETRYABLE_DELAY,
)
def network_with_retry() -> Any:
    return network()


DEFAULT_NETWORK = network()

##########
# Fixtures
##########

# These are the names of the fixtures that are used by the plugin.
# They define preconfigured components fixtures for docker containers

# Fixtures names
################

# Generic components fixtures
CELERY_SETUP = "celery_setup"
CELERY_WORKER = "celery_worker"
CELERY_WORKER_CLUSTER = "celery_worker_cluster"
CELERY_BACKEND = "celery_backend"
CELERY_BACKEND_CLUSTER = "celery_backend_cluster"
CELERY_BROKER = "celery_broker"
CELERY_BROKER_CLUSTER = "celery_broker_cluster"

# Components fixtures
CELERY_SETUP_WORKER = "celery_setup_worker"
CELERY_REDIS_BACKEND = "celery_redis_backend"
CELERY_REDIS_BROKER = "celery_redis_broker"
CELERY_RABBITMQ_BROKER = "celery_rabbitmq_broker"
DEFAULT_WORKER = "default_worker_container"
DEFAULT_REDIS_BACKEND = "default_redis_backend"
DEFAULT_RABBITMQ_BROKER = "default_rabbitmq_broker"
DEFAULT_REDIS_BROKER = "default_redis_broker"

# Fixtures collections
######################

DEFAULT_WORKERS = (DEFAULT_WORKER,)
DEFAULT_BACKENDS = (DEFAULT_REDIS_BACKEND,)
DEFAULT_BROKERS = (
    DEFAULT_RABBITMQ_BROKER,
    DEFAULT_REDIS_BROKER,
)

ALL_REDIS_FIXTURES = (
    DEFAULT_REDIS_BACKEND,
    DEFAULT_REDIS_BROKER,
)
ALL_RABBITMQ_FIXTURES = (DEFAULT_RABBITMQ_BROKER,)
ALL_WORKERS_FIXTURES = (*DEFAULT_WORKERS,)
ALL_BACKENDS_FIXTURES = (*DEFAULT_BACKENDS,)
ALL_BROKERS_FIXTURES = (*DEFAULT_BROKERS,)
ALL_COMPONENTS_FIXTURES = (
    *ALL_WORKERS_FIXTURES,
    *ALL_BACKENDS_FIXTURES,
    *ALL_BROKERS_FIXTURES,
)
ALL_NODES_FIXTURES = (
    CELERY_WORKER,
    CELERY_BACKEND,
    CELERY_BROKER,
)
ALL_CLUSTERS_FIXTURES = (
    CELERY_WORKER_CLUSTER,
    CELERY_BACKEND_CLUSTER,
    CELERY_BROKER_CLUSTER,
)
ALL_CELERY_WORKERS = (CELERY_SETUP_WORKER,)
ALL_CELERY_BACKENDS = (CELERY_REDIS_BACKEND,)
ALL_CELERY_BROKERS = (
    CELERY_REDIS_BROKER,
    CELERY_RABBITMQ_BROKER,
)

##########################
# Worker Container Settings
##########################

# Default container settings for all worker container fixtures
WORKER_CELERY_APP_NAME = "celery_test_app"
WORKER_CELERY_VERSION = "5.3.0b2"
WORKER_LOG_LEVEL = "INFO"
WORKER_NAME = CELERY_SETUP_WORKER
WORKER_QUEUE = "celery"
WORKER_ENV = {
    "CELERY_BROKER_URL": "memory://",
    "CELERY_RESULT_BACKEND": "cache+memory://",
    "PYTHONUNBUFFERED": "1",
}
WORKER_VOLUME = {
    "bind": "/app",
    "mode": "rw",
}

# Docker containers settings
#################################################

# Default Worker #
###################
DEFAULT_WORKER_APP_NAME = WORKER_CELERY_APP_NAME
DEFAULT_WORKER_VERSION = WORKER_CELERY_VERSION
DEFAULT_WORKER_LOG_LEVEL = WORKER_LOG_LEVEL
DEFAULT_WORKER_NAME = WORKER_NAME
DEFAULT_WORKER_ENV = WORKER_ENV
DEFAULT_WORKER_QUEUE = WORKER_QUEUE
DEFAULT_WORKER_CONTAINER_TIMEOUT = READY_TIMEOUT
DEFAULT_WORKER_VOLUME = WORKER_VOLUME

##########################
# Redis Container Settings
##########################

# Default container settings for all redis container fixtures

REDIS_IMAGE = "redis:latest"
REDIS_PORTS = {"6379/tcp": None}
REDIS_ENV: dict = {}
REDIS_CONTAINER_TIMEOUT = READY_TIMEOUT

# Docker containers settings
#################################################

# Default Backend #
####################
DEFAULT_REDIS_BACKEND_ENV = REDIS_ENV
DEFAULT_REDIS_BACKEND_IMAGE = REDIS_IMAGE
DEFAULT_REDIS_BACKEND_PORTS = REDIS_PORTS


# Default Broker #
###################
DEFAULT_REDIS_BROKER_ENV = REDIS_ENV
DEFAULT_REDIS_BROKER_IMAGE = REDIS_IMAGE
DEFAULT_REDIS_BROKER_PORTS = REDIS_PORTS


#############################
# RabbitMQ Container Settings
#############################

# Default container settings for all rabbitmq container fixtures

RABBITMQ_IMAGE = "rabbitmq:latest"
RABBITMQ_PORTS = {"5672/tcp": None}
RABBITMQ_ENV: dict = {}
RABBITMQ_CONTAINER_TIMEOUT = READY_TIMEOUT

# Docker containers settings
#################################################

# Default Broker #
###################
DEFAULT_RABBITMQ_BROKER_ENV = RABBITMQ_ENV
DEFAULT_RABBITMQ_BROKER_IMAGE = RABBITMQ_IMAGE
DEFAULT_RABBITMQ_BROKER_PORTS = RABBITMQ_PORTS
