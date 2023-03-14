from celery import Celery

app = Celery(
    "myapp",
    broker="pyamqp://guest@rabbitmq//",
    # broker="redis://redis:6379/0",
    # backend="redis://redis:6379/0",
    task_acks_late=True,
)


@app.task
def add(x, y):
    return x + y


# print("TOMER")
# add.s(16, 16).delay()

if __name__ == "__main__":
    app.start()
