FROM python:3.10-slim-bullseye as base
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv \
 && pipenv --python 3.10 \
 && pipenv install --system --deploy
COPY car_dealerships /app/

FROM base as celery
RUN chmod +x entrypoints/entrypoint_celery.sh
CMD ["celery", "-A", "car_dealerships.config", "worker", "-l", "info"]

FROM base as django
RUN chmod +x entrypoints/entrypoint_django.sh
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
