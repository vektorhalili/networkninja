from django import forms
from .models import Device

class PostDevice(forms.ModelForm):
	class Meta:
		model = Device
		fields = ('name','ipadd','type','user','password')
class ArpDevice(forms.Form):
	name = forms.CharField(max_length=20)
