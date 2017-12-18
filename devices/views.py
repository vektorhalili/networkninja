
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from napalm import get_network_driver
from devices.models import Device
from devices.models import Client
from .forms import PostDevice
from .forms import ArpDevice
from .forms import ConfigDevice
from django.shortcuts import redirect
from django.http import Http404

def get_device_arp(ipadd, type, user, password):
    try:
        driver = get_network_driver(type)
        device = driver(ipadd, user, password)
        device.open()
        arp = device.get_arp_table()
        return(arp)
    except:
        arp='was not able to get device arp'

def index(request):
   return render(request, 'index.html', {})

def devices(request):
	##if post it means we are passing the name of device here to get arp
	if request.method == "POST" and "arp:" in (request.POST['name']):
		print(request.POST)
		form = ArpDevice(request.POST)
		if form.is_valid():
			devicename = form.cleaned_data['name']
			devicename = devicename.split(':')
			devicename = devicename[1]
			try:
				device = Device.objects.get(name__iexact=devicename)
				devicename = device.name
				ipadd = device.ipadd
				type = device.type
				user = device.user
				password = device.password
				device = get_device_arp(ipadd, type, user, password)
				return render(request, 'devicearp.html',{'device': device,'devicename': devicename})
			except Exception:
				raise Http404
	elif request.method == "POST" and "config:" in (request.POST['name']):
		 #if post and contains config it means we clicked config button
		form = ConfigDevice(request.POST)
		if form.is_valid():
			devicename = form.cleaned_data['name']
			devicename = devicename.split(':')
			devicename = devicename[1]
			try:
				device = Device.objects.get(name__iexact=devicename)
				devicename = device.name
				ipadd = device.ipadd
				type = device.type
				user = device.user
				password = device.password
				driver = get_network_driver(type)
				device = driver(ipadd, user, password)
				device.open()
				config = device.get_config()
				config = config['startup']
				device.close()
				return render(request, 'deviceconfig.html',{'config': config,'devicename': devicename})
			except Exception:
				raise Http404
	else:
		form = ArpDevice()
		devices = Device.objects.all()
		return render(request, 'devices.html',{'devices': devices, 'form': form})

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
