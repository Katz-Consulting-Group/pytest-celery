import logging
import sys

from celery import Celery
from celery.signals import after_setup_logger

# Will be replaced with the import string for the tasks at runtime
{}

app = Celery("celery_test_app")


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    # https://distributedpython.com/posts/celery-docker-and-the-missing-startup-banner/
    logger.addHandler(logging.StreamHandler(sys.stdout))


if __name__ == "__main__":
    app.start()
