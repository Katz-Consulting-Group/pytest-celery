from time import sleep

import pytest
from celery.canvas import chain
from celery.canvas import chord
from celery.canvas import group
from celery.canvas import signature

from pytest_celery import CeleryTestSetup
from pytest_celery import defaults
from tests.common.tasks import identity
from tests.smoke.tasks import add


class test_acceptance:
    def test_sanity(self, celery_setup: CeleryTestSetup):
        assert 3 <= len(celery_setup) <= 6
        worker_queue = celery_setup.worker_cluster[0].worker_queue
        expected = "test_sanity"
        res = identity.s(expected).apply_async(queue=worker_queue)
        assert res.get(timeout=defaults.RESULT_TIMEOUT) == expected

        sleep(2)  # wait for logs to be flushed
        assert expected in celery_setup.worker_cluster[0].logs()

        if len(celery_setup.worker_cluster) > 1:
            worker_queue = celery_setup.worker_cluster[1].worker_queue

        res = add.s(1, 2).apply_async(queue=worker_queue)
        assert res.get(timeout=defaults.RESULT_TIMEOUT) == 3

        sleep(2)  # wait for logs to be flushed
        if len(celery_setup.worker_cluster) > 1:
            assert expected not in celery_setup.worker_cluster[1].logs()
            assert "succeeded" in celery_setup.worker_cluster[1].logs()
        else:
            assert expected in celery_setup.worker_cluster[0].logs()

    def test_signature(self, celery_setup: CeleryTestSetup):
        worker_queue = celery_setup.worker_cluster[0].worker_queue
        sig = signature(identity, args=("test_signature",), queue=worker_queue)
        assert sig.delay().get(timeout=defaults.RESULT_TIMEOUT) == "test_signature"

    def test_group(self, celery_setup: CeleryTestSetup):
        worker_queue = celery_setup.worker_cluster[0].worker_queue
        sig = group(
            group(add.si(1, 1), add.si(2, 2)),
            group([add.si(1, 1), add.si(2, 2)]),
            group(s for s in [add.si(1, 1), add.si(2, 2)]),
        )
        res = sig.apply_async(queue=worker_queue)
        assert res.get(timeout=defaults.RESULT_TIMEOUT)  # == [2, 4, 2, 4, 2, 4]

    def test_chain(self, celery_setup: CeleryTestSetup):
        worker_queue = celery_setup.worker_cluster[0].worker_queue
        sig = chain(
            identity.si("chain_task1").set(queue=worker_queue),
            identity.si("chain_task2").set(queue=worker_queue),
        ) | identity.si("test_chain").set(queue=worker_queue)
        res = sig.apply_async()
        assert res.get(timeout=defaults.RESULT_TIMEOUT) == "test_chain"

    def test_chord(self, celery_setup: CeleryTestSetup):
        if not celery_setup.chords_allowed():
            pytest.skip("Chords are not supported")

        worker_queue = celery_setup.worker_cluster[0].worker_queue

        upgraded_chord = signature(
            group(identity.si("header_task1"), identity.si("header_task2")) | identity.si("body_task"),
            queue=worker_queue
            if len(celery_setup.worker_cluster) == 1
            else celery_setup.worker_cluster[1].worker_queue,
        )

        sig = group(
            [
                upgraded_chord,
                chord(group(identity.si("header_task3"), identity.si("header_task4")), identity.si("body_task")),
                chord(
                    (sig for sig in [identity.si("header_task5"), identity.si("header_task6")]),
                    identity.si("body_task"),
                ),
            ]
        )
        res = sig.apply_async(queue=worker_queue)
        assert res.get(timeout=defaults.RESULT_TIMEOUT) == ["body_task"] * 3
