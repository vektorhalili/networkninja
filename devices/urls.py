from django.urls import path, re_path
from . import views
#from devices.views import DeviceFactsView
from devices.views import *

app_name = 'devices'

urlpatterns = [
    path('post_device.html', views.post_device, name='post_device'),
    #re_path('^devices/getdevicearp', views.getdevicearp, name='getdevicearp'),
    path('devices/', views.devices, name='devices'),
#    path('clients/', views.clients, name='clients'),
#    the above was the function equivalent
    path('clients/', ClientsListView.as_view(), name='clients'),
    re_path('^devices/arp/', ArpDeviceView.as_view(), name='arp'),
    path('devicearp.html', ArpDeviceView.as_view(), name = 'arp'),
    #path('devicefaces/', views.devicefacts, name='devicefacts'),
    #path('devices/devicefacts/', DeviceFactsView.as_view()),
    path('mytest/', mytestview.as_view()),
    path('', views.index, name='index'),
]
