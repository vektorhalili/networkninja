
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from napalm import get_network_driver
from devices.models import Device
from devices.models import Client
from .forms import PostDevice
from .forms import ArpDevice
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
	if request.method == "POST":
		form = ArpDevice(request.POST)
		if form.is_valid():
			devicename = form.cleaned_data['name']
			try:
				device = Device.objects.get(name__iexact=devicename)
				ipadd = device.ipadd
				type = device.type
				user = device.user
				password = device.password
				device = get_device_arp(ipadd, type, user, password)
				return render(request, 'devicearp.html',{'device': device})
			except Exception:
				raise Http404
	else:
		form = ArpDevice()
		devices = Device.objects.all()
		return render(request, 'devices.html',{'devices': devices, 'form': form})

def clients(request):
    clients = Client.objects.all()
    return render(request, 'clients.html',{'clients': clients})

def getdevicearp(request):
	requestdevice = request.POST["getdevicearp"]
	if (requestdevice):
		#requestdevice = request.GET.get('getdevicearp', '')
		#device = Device.objects.get(name__iexact=requestdevice)
		device = Device.objects.get(name__iexact=requestdevice)
		#device = Device(name=requestdevice)
		ipadd = device.ipadd
		type = device.type
		user = device.user
		password = device.password
		device = get_device_arp(ipadd, type, user, password)
		return render(request, 'devicearp.html',{'device': device})

def post_device(request):
	if request.method == "POST":
		form = PostDevice(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/devices')
	else:
		form = PostDevice()
		return render(request, 'post_device.html', {'form': form})
