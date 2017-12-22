
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
#from napalm import get_network_driver
from devices.models import Device
from devices.models import Client
from devices.models import DeviceFacts
from . import models
from .forms import PostDevice
from .forms import ArpDevice
from .forms import ConfigDevice
from .forms import DeviceFactsForm
from .forms import DeviceNameForm
from django.shortcuts import redirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import View
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from .cisco_commands import *

def index(request):
   return render(request, 'index.html', {})

def devices(request):
	##if post it means we are passing the name of device here to get arp
	if request.method == "POST" and "arp:" in (request.POST['name']):
		#print(request.POST)
		form = ArpDevice(request.POST)
		if form.is_valid():
			devicename = form.cleaned_data['name'].split(':')[1]
			try:
				device = Device.objects.get(name__iexact=devicename)
				device = get_device_arp(device.ipadd, device.type, device.user, device.password)
				return render(request, 'devicearp.html',{'device': device,'devicename': devicename})
			except Exception:
				raise Http404
	elif request.method == "POST" and "config:" in (request.POST['name']):
		 #if post and contains config it means we clicked config button
		form = ConfigDevice(request.POST)
		if form.is_valid():
			devicename = form.cleaned_data['name'].split(':')[1]
			try:
				device = Device.objects.get(name__iexact=devicename)
				config = get_device_config(device.ipadd, device.type, device.user, device.password)
				return render(request, 'deviceconfig.html',{'config': config,'devicename': devicename})
			except Exception:
				raise Http404
	elif request.method == "POST" and "facts:" in (request.POST['name']):
		#if post and contains config it means we clicked FACTS button
		form = DeviceFactsForm(request.POST)
		if form.is_valid():
			devicename = form.cleaned_data['name'].split(':')[1]
			try:
				device = Device.objects.get(name__iexact=devicename)
				devicefacts = get_device_facts(device.ipadd, device.type, device.user, device.password)
				return render(request, 'devicefacts.html',{'devicefacts': devicefacts,'devicename': devicename})
			except Exception:
				raise Http404
	else:
		devices = Device.objects.all()
		return render(request, 'devices.html',{'devices': devices})

def post_device(request):
	if request.method == "POST":
		form = PostDevice(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/devices')
	else:
		form = PostDevice(initial={'type': 'ios'})
		return render(request, 'post_device.html', {'form': form})

class ClientsListView(ListView):
    context_object_name = 'clients'
    model = models.Client
    template_name = 'clients.html'

class ArpDeviceView(View):
    template_name = 'devicearp.html'
    form_class = DeviceNameForm
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            devicename = form.cleaned_data['name']
            try:
                device = Device.objects.get(name__iexact=devicename)
                device = get_device_arp(device.ipadd, device.type, device.user, device.password)
            except Exception as arperror:
                #raise Http404
                print(f'the error was: {arperror}')
            return render(request, self.template_name, {'devicename': devicename, 'device' : device})


class DeviceFactsView(View):
    template_name = 'devicefacts.html'
    form_class = DeviceNameForm
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            devicename = form.cleaned_data['name']
            try:
                device = Device.objects.get(name__iexact=devicename)
                device = get_device_facts(device.ipadd, device.type, device.user, device.password)
            except Exception:
                raise Http404
            return render(request, self.template_name, {'devicename': devicename, 'device' : device})

