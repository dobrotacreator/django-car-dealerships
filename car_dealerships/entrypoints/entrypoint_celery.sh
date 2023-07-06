#!/bin/bash

sleep 10
celery -A config worker -l INFO
