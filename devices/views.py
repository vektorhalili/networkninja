
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from napalm import get_network_driver
from devices.models import Device
from devices.models import Client
from devices.models import DeviceFacts
from .import models
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

def get_device_arp(ipadd, type, user, password):
    try:
        driver = get_network_driver(type)
        optional_args = {'secret': password}
        device = driver(ipadd, user, password, optional_args=optional_args)
        device.open()
        arp = device.get_arp_table()
        device.close()
        return(arp)
    except:
        arp='was not able to get device arp'

def get_device_config(ipadd, type, user, password):
    try:
        driver = get_network_driver(type)
        optional_args = {'secret': password}
        device = driver(ipadd, user, password, optional_args=optional_args)
        device.open()
        config = device.get_config()
        config = config['startup']
        device.close()
        return(config)
    except Exception:
        config='was not able to pull device config'

def get_device_facts(ipadd, type, user, password):
    try:
        driver = get_network_driver(type)
        optional_args = {'secret': password}
        device = driver(ipadd, user, password, optional_args=optional_args)
        device.open()
        devicefacts = device.get_facts()
        device.close()
        return(devicefacts)
    except Exception:
        devicefacts='was not able to pull device facts'


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

def clients(request):
    clients = Client.objects.all()
    return render(request, 'clients.html',{'clients': clients})

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

class mytestview(View):
	def get(self,request):
		return HttpResponse('this page matched the mytestview GET method')

#class ArpDeviceView(View):
#    form_class = DeviceNameForm
#    template_name = 'devicearp.html'
#    def post(self, request, *args, **kwargs):
#        form = self.form_class(request.POST)
#        form.is_valid()
#        def form_valid():
#            devicename = form.cleaned_data['name']
#            try:
#                device = Device.objects.get(name__iexact=devicename)
#                device = get_device_arp(device.ipadd, device.type, device.user, device.password)
#                return render(request, 'devicearp.html',{'devicefacts': devicefacts,'devicename': devicename})
#            except Exception:
#                #raise Http404
#                print('error in getting the arp')
#        form.is_valid()


class ArpDeviceView(View):
    template_name = 'devicearp.html'
    form_class = DeviceNameForm
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            devicename = form.cleaned_data['name']
            try:
                device = Device.objects.get(name__iexact=devicename)
                print(device.ipadd)
                print(device.type)
                print(device.user)
                print(device.password)
                device = get_device_arp(device.ipadd, device.type, device.user, device.password)
            except Exception:
                #raise Http404
                print('error in try block getting device arp')
            return render(request, self.template_name, {'devicename': devicename, 'device' : device})
