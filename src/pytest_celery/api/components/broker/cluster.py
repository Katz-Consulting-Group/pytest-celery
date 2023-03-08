from typing import Tuple
from typing import Union

from pytest_celery.api.components.broker.node import CeleryTestBroker
from pytest_celery.api.components.cluster.base import CeleryTestCluster
from pytest_celery.api.components.cluster.node import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer


class CeleryBrokerCluster(CeleryTestCluster):
    def __init__(self, *brokers: Tuple[Union[CeleryTestBroker, CeleryTestContainer]]) -> None:
        super().__init__(*brokers)

    def _set_nodes(self, *nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]]) -> Tuple[CeleryTestNode]:
        return tuple(
            CeleryTestBroker(broker) if isinstance(broker, CeleryTestContainer) else broker for broker in nodes
        )
