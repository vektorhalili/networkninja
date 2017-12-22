from django import forms
from .models import Device
from napalm import get_network_driver


def get_device_facts(ipadd, type, user, password):
    try:
        driver = get_network_driver(type)
        optional_args = {'secret': password}
        device = driver(ipadd, user, password, optional_args=optional_args)
        device.open()
        device = device.get_facts()
        return(device)
    except Exception:
        device='was not able to pull device facts'


class PostDevice(forms.ModelForm):
	class Meta:
		model = Device
		fields = ('name','ipadd','type','user','password')
class ArpDevice(forms.Form):
	name = forms.CharField(max_length=20)

class ConfigDevice(forms.Form):
	name = forms.CharField(max_length=20)

class DeviceFactsForm(forms.Form):
	name = forms.CharField(max_length=20)

class DeviceNameForm(forms.Form):
	name = forms.CharField(max_length=30)
