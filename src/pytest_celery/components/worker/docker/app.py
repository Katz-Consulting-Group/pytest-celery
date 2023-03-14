import os

from celery import Celery

# from logging import Logger


# from celery.signals import after_setup_logger
# from celery.signals import after_setup_task_logger

app = Celery("celery_test_app")
# app.config_from_object("celeryconfig")
# app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")

# @after_setup_logger.connect
# def after_setup_logger_handler(logger: Logger, *args, **kwargs):
#     logger.setLevel(os.environ.get("LOG_LEVEL", "DEBUG"))
#     for handler in logger.handlers:
#         handler.setLevel(os.environ.get("LOG_LEVEL", "DEBUG"))


# @after_setup_task_logger.connect
# def after_setup_task_logger_handler(logger: Logger, *args, **kwargs):
#     logger.setLevel(os.environ.get("LOG_LEVEL", "DEBUG"))
#     for handler in logger.handlers:
#         handler.setLevel(os.environ.get("LOG_LEVEL", "DEBUG"))


@app.task
def ping():
    return "pong"


print(f'CELERY_BROKER_URL={os.environ.get("CELERY_BROKER_URL", "N/A")}')
# ping.delay()
# print(app.conf.humanize(with_defaults=True, censored=False))
if __name__ == "__main__":
    app.start()
