# django_celery/celery.py

import os

from celery import Celery
from celery import chain
from celery.schedules import crontab
from datetime import timedelta
from app.tasks import get_pressure
from app.tasks import read_pressure_switch
from app.tasks import control_pressure

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

'''
@app.task
def chained_pressure_tasks(arg1, arg2):
    chained_task = chain(
        app.tasks.get_pressure.s(arg1, arg2),
        app.tasks.read_pressure_switch.s(arg1, arg2),
    )
'''

app.conf.beat_schedule = {
    'measure-pressure': {
        'task': 'app.tasks.get_pressure',
        'schedule': timedelta(milliseconds=100),
        'args': (16, 16),
    },

    '''
    'pressure-switch-state': {
        'task': 'app.tasks.read_pressure_switch',
        'schedule': timedelta(milliseconds=10000),
        'args': (1,1),
    },
    '''

    '''
    'chained-pressure-tasks': {
        'task': 'app.tasks.chained_pressure_tasks',
        'schedule': timedelta(milliseconds=2500),
        'args': (16,16),
    },
    '''
    'update-control-pressure': {
        'task': 'app.tasks.control_pressure',
        'schedule': timedelta(milliseconds=2500),
        'args': (1,1),
    }
}