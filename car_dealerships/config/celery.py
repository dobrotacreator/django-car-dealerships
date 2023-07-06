import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('car_dealerships')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
