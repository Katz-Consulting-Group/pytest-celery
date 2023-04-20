import contextlib
import multiprocessing
import time
from typing import Any

import docker
from pytest_docker_tools import network

RETRY_ERRORS = (
    docker.errors.NotFound,
    docker.errors.APIError,
)

READY_TIMEOUT = 30
RESULT_TIMEOUT = 30
MAX_TRIES = 5
DELAY_SECONDS = 0.5
MAX_DELAY_SECONDS = 120

CONCURRENT_FIXTURES_LIMIT = 10
FIXTURES_SEMAPHORE = multiprocessing.Semaphore(CONCURRENT_FIXTURES_LIMIT)


class NetworkPool:
    def __init__(self):
        self.networks = []
        self.lock = multiprocessing.Lock()

    def get_network(self):
        with self.lock:
            if self.networks:
                return self.networks.pop()
            return None

    def return_network(self, net):
        with self.lock:
            self.networks.append(net)


network_pool = NetworkPool()


@contextlib.contextmanager
def network_context():
    net = network_pool.get_network()
    acquired_semaphore = False

    if net is None:
        FIXTURES_SEMAPHORE.acquire()
        acquired_semaphore = True
        for _ in range(MAX_TRIES):
            try:
                net = network()
                break
            except RETRY_ERRORS:
                time.sleep(DELAY_SECONDS)

    if net is None:
        raise RuntimeError("Failed to create a network after multiple retries")

    try:
        yield net
    finally:
        network_pool.return_network(net)
        if acquired_semaphore:
            FIXTURES_SEMAPHORE.release()


def network_with_retry() -> Any:
    with network_context() as net:
        return net
