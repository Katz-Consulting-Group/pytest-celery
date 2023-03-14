# FROM python3:3.9
# RUN pip3 install celery
# COPY ./app.py /app.py
# ENV PYTHONUNBUFFERED 1
# CMD ["celery", "-A", "app", "worker", "-l", "INFO"]


# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster
# FROM gcr.io/google-appengine/python

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
WORKDIR /home/user/app
COPY . .

# Install any necessary dependencies
# RUN pip install celery
# RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install -r requirements.txt

# Expose the port that the Celery worker will run on (if applicable)
# EXPOSE 6379

# Define the command to run the Celery worker
CMD celery -A app worker --loglevel=info

# FROM python:3.9-slim-buster

# RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
# WORKDIR /home/user

# ENV CELERY_VERSION "5.3.0b2"

# RUN pip install celery==$CELERY_VERSION

# # RUN { \
# #     echo 'import os'; \
# #     echo "BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'pyamqp://')"; \
# #     } > celeryconfig.py

# # --link some-rabbit:rabbit "just works"
# # ENV CELERY_BROKER_URL redis://localhost:6379/0

# USER user
# # CMD ["celery", "worker"]
# CMD ["celery", "worker", "-A", "app", "--loglevel=info"]
