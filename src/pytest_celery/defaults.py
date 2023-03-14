"""
This module contains all the default values and settings.
These values are used by the pytest-celery plugin to configure the
components fixtures. You can override these values by hooking to the
matchin fixture and returning your own value.
"""

##########
# Fixtures
##########

# These are the names of the fixtures that are used by the plugin.
# They define preconfigured components fixtures for docker containers

# Fixtures names
################

# Generic components fixtures
CELERY_SETUP = "celery_setup"
CELERY_SESSION_SETUP = "celery_session_setup"
CELERY_WORKER = "celery_worker"
CELERY_SESSION_WORKER = "celery_session_worker"
CELERY_WORKER_CLUSTER = "celery_worker_cluster"
CELERY_SESSION_WORKER_CLUSTER = "celery_session_worker_cluster"
CELERY_BACKEND = "celery_backend"
CELERY_SESSION_BACKEND = "celery_session_backend"
CELERY_BACKEND_CLUSTER = "celery_backend_cluster"
CELERY_SESSION_BACKEND_CLUSTER = "celery_session_backend_cluster"
CELERY_BROKER = "celery_broker"
CELERY_SESSION_BROKER = "celery_session_broker"
CELERY_BROKER_CLUSTER = "celery_broker_cluster"
CELERY_SESSION_BROKER_CLUSTER = "celery_session_broker_cluster"

# Components fixtures
CELERY_TEST_WORKER = "celery_test_worker"
CELERY_REDIS_BACKEND = "celery_redis_backend"
CELERY_REDIS_BROKER = "celery_redis_broker"
CELERY_RABBITMQ_BROKER = "celery_rabbitmq_broker"
FUNCTION_WORKER = "function_worker"
REDIS_FUNCTION_BACKEND = "redis_function_backend"
RABBITMQ_FUNCTION_BROKER = "rabbitmq_function_broker"
REDIS_FUNCTION_BROKER = "redis_function_broker"
SESSION_WORKER = "session_worker"
REDIS_SESSION_BACKEND = "redis_session_backend"
RABBITMQ_SESSION_BROKER = "rabbitmq_session_broker"
REDIS_SESSION_BROKER = "redis_session_broker"

# Fixtures collections
######################

FUNCTION_WORKERS = (FUNCTION_WORKER,)
SESSION_WORKERS = (SESSION_WORKER,)
FUNCTION_BACKENDS = (REDIS_FUNCTION_BACKEND,)
FUNCTION_BROKERS = (
    RABBITMQ_FUNCTION_BROKER,
    REDIS_FUNCTION_BROKER,
)
SESSION_BACKENDS = (REDIS_SESSION_BACKEND,)
SESSION_BROKERS = (
    RABBITMQ_SESSION_BROKER,
    REDIS_SESSION_BROKER,
)
ALL_REDIS_FIXTURES = (
    REDIS_FUNCTION_BACKEND,
    REDIS_SESSION_BACKEND,
    REDIS_FUNCTION_BROKER,
    REDIS_SESSION_BROKER,
)
ALL_RABBITMQ_FIXTURES = (
    RABBITMQ_FUNCTION_BROKER,
    RABBITMQ_SESSION_BROKER,
)
ALL_WORKERS_FIXTURES = (
    *FUNCTION_WORKERS,
    *SESSION_WORKERS,
)
ALL_BACKENDS_FIXTURES = (
    *FUNCTION_BACKENDS,
    *SESSION_BACKENDS,
)
ALL_BROKERS_FIXTURES = (
    *FUNCTION_BROKERS,
    *SESSION_BROKERS,
)
ALL_COMPONENTS_FIXTURES = (
    *ALL_WORKERS_FIXTURES,
    *ALL_BACKENDS_FIXTURES,
    *ALL_BROKERS_FIXTURES,
)
ALL_NODES_FIXTURES = (
    CELERY_WORKER,
    CELERY_SESSION_WORKER,
    CELERY_BACKEND,
    CELERY_SESSION_BACKEND,
    CELERY_BROKER,
    CELERY_SESSION_BROKER,
)
ALL_CLUSTERS_FIXTURES = (
    CELERY_WORKER_CLUSTER,
    CELERY_SESSION_WORKER_CLUSTER,
    CELERY_BACKEND_CLUSTER,
    CELERY_SESSION_BACKEND_CLUSTER,
    CELERY_BROKER_CLUSTER,
    CELERY_SESSION_BROKER_CLUSTER,
)

##########################
# Worker Container Settings
##########################

# Default container settings for all worker container fixtures
WORKER_ENV = {}

# Function and Session docker containers settings
#################################################

# Function Worker #
###################
FUNCTION_WORKER_ENV = WORKER_ENV

# Session Worker #
##################
SESSION_WORKER_ENV = WORKER_ENV

##########################
# Redis Container Settings
##########################

# Default container settings for all redis container fixtures

REDIS_IMAGE = "redis:latest"
REDIS_PORTS = {"6379/tcp": None}
REDIS_ENV = {}

# Function and Session docker containers settings
#################################################

# Function Backend #
####################
REDIS_FUNCTION_BACKEND_ENV = REDIS_ENV
REDIS_FUNCTION_BACKEND_IMAGE = REDIS_IMAGE
REDIS_FUNCTION_BACKEND_PORTS = REDIS_PORTS

# Session Backend #
###################
REDIS_SESSION_BACKEND_ENV = REDIS_ENV
REDIS_SESSION_BACKEND_IMAGE = REDIS_IMAGE
REDIS_SESSION_BACKEND_PORTS = REDIS_PORTS

# Function Broker #
###################
REDIS_FUNCTION_BROKER_ENV = REDIS_ENV
REDIS_FUNCTION_BROKER_IMAGE = REDIS_IMAGE
REDIS_FUNCTION_BROKER_PORTS = REDIS_PORTS

# Session Broker #
##################
REDIS_SESSION_BROKER_ENV = REDIS_ENV
REDIS_SESSION_BROKER_IMAGE = REDIS_IMAGE
REDIS_SESSION_BROKER_PORTS = REDIS_PORTS

#############################
# RabbitMQ Container Settings
#############################

# Default container settings for all rabbitmq container fixtures

RABBITMQ_IMAGE = "rabbitmq:latest"
RABBITMQ_PORTS = {"5672/tcp": None}
RABBITMQ_ENV = {}
RABBITMQ_CONTAINER_TIMEOUT = 60

# Function and Session docker containers settings
#################################################

# Function Broker #
###################
RABBITMQ_FUNCTION_BROKER_ENV = RABBITMQ_ENV
RABBITMQ_FUNCTION_BROKER_IMAGE = RABBITMQ_IMAGE
RABBITMQ_FUNCTION_BROKER_PORTS = RABBITMQ_PORTS

# Session Broker #
##################
RABBITMQ_SESSION_BROKER_ENV = RABBITMQ_ENV
RABBITMQ_SESSION_BROKER_IMAGE = RABBITMQ_IMAGE
RABBITMQ_SESSION_BROKER_PORTS = RABBITMQ_PORTS
