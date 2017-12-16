from django.urls import path

from . import views

urlpatterns = [
    path('devices/', views.devices, name='devices'),
    path('clients/', views.clients, name='clients'),
    path('', views.index, name='index'),
]
