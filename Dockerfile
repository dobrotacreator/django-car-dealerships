FROM python:3.10-slim-bullseye as base
WORKDIR /app
COPY car_dealerships .
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv \
    && pipenv install --system

FROM base as celery
RUN chmod +x entrypoints/entrypoint_celery.sh
CMD ["celery", "-A", "car_dealerships.car_dealerships", "worker", "-l", "info"]

FROM base as django
RUN chmod +x entrypoints/entrypoint_django.sh
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]