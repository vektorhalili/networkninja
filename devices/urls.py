from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('^post/post_device.html$', views.post_device, name='post_device'),
    #re_path('^devices/getdevicearp', views.getdevicearp, name='getdevicearp'),
    path('devices/', views.devices, name='devices'),
    path('clients/', views.clients, name='clients'),
    path('', views.index, name='index'),
]
