from django.urls import path

from . import views

urlpatterns = [
    path('', views.devices, name='devices'),
#    path('', views.index, name='index'),
]
