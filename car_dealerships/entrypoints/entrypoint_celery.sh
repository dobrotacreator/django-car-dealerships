#!/bin/bash

sleep 10
celery -A car_dealerships worker --loglevel=INFO
