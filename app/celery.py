# django_celery/celery.py

import os

from celery import Celery
from celery import chain
from celery.schedules import crontab
from datetime import timedelta
from app.tasks import IO
from app.tasks import control_pressure

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'measure-pressure': {
        'task': 'app.tasks.IO',
        'schedule': timedelta(milliseconds=100),
        'args': (16, 16),
    },

    'update-control-pressure': {
        'task': 'app.tasks.control_pressure',
        'schedule': timedelta(milliseconds=250),
        'args': (1,1),
    }
}