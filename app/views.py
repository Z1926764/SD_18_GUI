from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .tasks import get_pressure
from app.models import PressurePoint
import csv

# Index is the default view that appears when starting the app
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

# AutoTest is the view that appears when beginning an auto test
def autoTest(request):
    template = loader.get_template('autotest.html')
    return HttpResponse(template.render())

def graph(request):
    template = loader.get_template('graph.html')
    return HttpResponse(template.render())

# Settings view appears when user selects settings button
def settings(request):
    return HttpResponse('you are now in the settings page')

def data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'time','pressure'])

    data = PressurePoint.objects.all().values()
    dataList = []

    for row in data:
        dataList = row.values()
        writer.writerow(dataList)

    return response
'''

def data(request):
    template = loader.get_template('data.html')
    return HttpResponse(template.render())
'''