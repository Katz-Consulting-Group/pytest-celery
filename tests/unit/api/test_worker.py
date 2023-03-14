from pytest_celery import CeleryTestContainer
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster


class test_celey_test_worker:
    def test_ready(self, unit_tests_container: CeleryTestContainer):
        node = CeleryTestWorker(unit_tests_container)
        assert node.ready()


class test_celery_worker_cluster:
    def test_ready(self, unit_tests_container: CeleryTestContainer, local_test_container: CeleryTestContainer):
        node1 = CeleryTestWorker(unit_tests_container)
        node2 = CeleryTestWorker(local_test_container)
        cluster = CeleryWorkerCluster(node1, node2)
        assert cluster.ready()
