
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from devices.models import Device


def index(request):
   return render(request, 'index.html', {})

def devices(request):
    devices = Device.objects.all()
    return render(request, 'devices.html',{'devices': devices})
