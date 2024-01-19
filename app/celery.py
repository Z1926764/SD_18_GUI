# django_celery/celery.py


import os

from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
from app.tasks import get_pressure

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'measure-pressure': {
        'task': 'app.tasks.get_pressure',
        'schedule': timedelta(seconds=.25),
        'args': (16, 16),
    },
    'pressure-switch-state': {
        'task': 'app.tasks.read_pressure_switch',
        'schedule': timedelta(seconds=0),
        'args': (1,1),
    },
    'update-control-pressure': {
        'task': 'app.tasks.control_pressure',
        'schedule': timedelta(seconds=.25),
        'args': (1,1),
    }
}