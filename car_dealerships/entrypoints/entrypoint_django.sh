#!/bin/bash

echo "Applying database migrations..."
# python manage.py makemigrations cars customers dealerships suppliers transaction_history
python manage.py makemigrations ```cd src && ls -d */ | sed 's#/##' | grep -v '^__'```
python manage.py migrate --noinput

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000