from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .tasks import get_pressure

# Index is the default view that appears when starting the app
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

# AutoTest is the view that appears when beginning an auto test
def autoTest(request):
    template = loader.get_template('autotest.html')
    return HttpResponse(template.render())

# Settings view appears when user selects settings button
def settings(request):
    return HttpResponse('you are now in the settings page')

def menu(request):
    return HttpResponse('you are now in the menu page')
