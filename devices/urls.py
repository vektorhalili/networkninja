from django.urls import path, re_path
from . import views
from devices.views import *

app_name = 'devices'

urlpatterns = [
    path('devices/', views.devices, name='devices'),
    path('device_create/', DeviceAddView.as_view(), name='DeviceAddView'),
    path('devices/delete/', DeviceDeleteView.as_view(), name='DeviceDeleteView'),
    path('clients/', ClientsListView.as_view(), name='ClientsListView'),
    path('devices/arp/', DeviceArpView.as_view(), name='DeviceArpView'),
    path('devices/config/', DeviceConfigView.as_view(), name='DeviceConfigView'),
    path('devices/facts/', DeviceFactsView.as_view(), name='DeviceFactsView'),
    path('', views.index, name='index'),
]
