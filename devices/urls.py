from django.urls import path, re_path
from . import views
from devices.views import *

app_name = 'devices'

urlpatterns = [
    path('post_device', views.post_device, name='post_device'),
    path('devices/', views.devices, name='devices'),
    path('clients/', ClientsListView.as_view(), name='clients'),
    re_path('^devices/arp/', ArpDeviceView.as_view(), name='arp'),
    re_path('^devices/facts/', DeviceFactsView.as_view(), name='facts'),
    path('', views.index, name='index'),
]
