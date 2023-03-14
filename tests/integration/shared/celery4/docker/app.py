import logging
import sys

from celery import Celery
from celery.signals import after_setup_logger

app = Celery("celery4_test_app")


@app.task
def ping():
    return "pong"


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    # https://distributedpython.com/posts/celery-docker-and-the-missing-startup-banner/
    logger.addHandler(logging.StreamHandler(sys.stdout))


# ping.delay()

if __name__ == "__main__":
    app.start()
