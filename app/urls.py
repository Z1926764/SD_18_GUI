from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('autotest/', views.autoTest, name='autoTest'), # Path that lead to the auto test menu
    path('settings/', views.settings, name="settings"),
    path('data/', views.data, name="menu"),
]