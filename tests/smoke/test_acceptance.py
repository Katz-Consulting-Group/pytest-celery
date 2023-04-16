import pytest
from celery.canvas import chain
from celery.canvas import chord
from celery.canvas import group
from celery.canvas import signature

from pytest_celery import CeleryTestSetup
from tests.common.tasks import identity
from tests.smoke.tasks import add


class test_acceptance:
    def test_sanity(self, celery_setup: CeleryTestSetup):
        assert 3 <= len(celery_setup) <= 4
        assert identity.s("test_ready").delay().get(timeout=60) == "test_ready"
        assert add.s(1, 2).delay().get(timeout=60) == 3

    def test_signature(self, celery_setup: CeleryTestSetup):
        sig = signature(identity, args=("test_signature",))
        assert sig.delay().get(timeout=60) == "test_signature"

    def test_group(self, celery_setup: CeleryTestSetup):
        sig = group(
            group(add.s(1, 1), add.s(2, 2)),
            group([add.si(1, 1), add.si(2, 2)]),
            group(s for s in [add.si(1, 1), add.si(2, 2)]),
        )
        assert sig.delay().get(timeout=60) == [2, 4, 2, 4, 2, 4]

    def test_chain(self, celery_setup: CeleryTestSetup):
        sig = chain(identity.si("task1"), identity.si("task2"))
        assert sig.delay().get(timeout=60) == "task2"

    def test_chord(self, celery_setup: CeleryTestSetup):
        try:
            celery_setup.app.backend.ensure_chords_allowed()
        except NotImplementedError as e:
            raise pytest.skip(e.args[0])

        if any([v.startswith("4.") for v in celery_setup.worker_cluster.versions]):
            pytest.skip("Celery 4.x is not supported")

        for sig in [
            chord(group(identity.si("header_task1"), identity.si("header_task2")), identity.si("body_task")),
            group(identity.si("header_task1"), identity.si("header_task2")) | identity.si("body_task"),
            chord(
                (sig for sig in [identity.si("header_task1"), identity.si("header_task2")]),
                identity.si("body_task"),
            ),
        ]:
            assert sig.delay().get(timeout=60) == "body_task"
