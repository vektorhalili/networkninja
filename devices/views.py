
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import *
from django.views.generic import *
from django.views.generic.base import *
from django.views.generic.edit import *
from devices.models import *
from devices.forms import *
from . import models
from . import forms

from .cisco_commands import *
####
# Create your views here.








def index(request):
   return render(request, 'index.html', {})

def devices(request):
	##if post it means we are passing the name of device here to get arp
	if request.method == "POST" and "config:" in (request.POST['name']):
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

class DeviceAddView(CreateView):
    model = Device
    template_name_suffix = '_create'
    fields = ['name','type','ipadd','user','password']
    success_url='/devices'

class DeviceDeleteView(View, FormMixin):
    model = Device
    form_class = DeviceNameForm
    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        if form.is_valid():
            devicename = form.cleaned_data['name']
            device = form.get_device(devicename)
            device.delete()
            return redirect('/devices')


class ClientsListView(ListView):
    context_object_name = 'clients'
    model = models.Client
    template_name = 'clients.html'

class DeviceView(TemplateView, FormMixin):
    form_class = DeviceNameForm
    action = None
    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        if form.is_valid():
            devicename = form.cleaned_data['name']
            device = form.get_device(devicename)
            device = device_action(self.action, device.ipadd, device.type, device.user, device.password)
        context = self.get_context_data(devicename=devicename, device=device)
        return self.render_to_response(context)



class DeviceConfigView(DeviceView):
    template_name = 'deviceconfig.html'
    action = 'get_device_config'

class DeviceArpView(DeviceView):
    template_name = 'devicearp.html'
    action = 'get_device_arp'

class DeviceFactsView(DeviceView):
    template_name = 'devicefacts.html'
    action = 'get_device_facts'
