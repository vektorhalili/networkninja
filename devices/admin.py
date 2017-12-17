from django.contrib import admin

# Register your models here.
from devices.models import Device
from devices.models import Client
admin.site.register(Device)
#admin.site.register(Client)
