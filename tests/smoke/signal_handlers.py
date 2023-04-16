from celery.signals import worker_init
from celery.signals import worker_process_init
from celery.signals import worker_process_shutdown
from celery.signals import worker_ready
from celery.signals import worker_shutdown


@worker_init.connect
def worker_init_handler(sender, **kwargs):  # type: ignore
    print(f"worker_init_handler: {sender=}")


@worker_process_init.connect
def worker_process_init_handler(sender, **kwargs):  # type: ignore
    print(f"worker_process_init_handler: {sender=}")


@worker_process_shutdown.connect
def worker_process_shutdown_handler(sender, pid, exitcode, **kwargs):  # type: ignore
    print(f"worker_process_shutdown_handler: {sender=}, {pid=}, {exitcode=}")


@worker_ready.connect
def worker_ready_handler(sender, **kwargs):  # type: ignore
    print(f"worker_ready_handler: {sender=}")


@worker_shutdown.connect
def worker_shutdown_handler(sender, **kwargs):  # type: ignore
    print(f"worker_shutdown_handler: {sender=}")
