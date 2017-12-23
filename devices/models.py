from django.db import models
from django.utils import timezone

# Create your models here.



class Device(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=3)
    ipadd = models.GenericIPAddressField()
    user = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    enable = models.CharField(max_length=30)

    def publish(self):
        self.save()
    def __str__(self):
        return self.name


class Client(models.Model):
	mac = models.CharField(max_length=19, primary_key=True)
	ipadd = models.GenericIPAddressField()
	def publish(self):
		self.save()
	def __str__(self):
		return self.mac

class DeviceFacts(models.Model):
    uptime = models.IntegerField
    vendor = models.CharField(max_length=30)
    os_version = models.CharField(max_length=30)
    fqdn = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    def publish(self):
        self.save()
    def __str__(self):
        return self.fqdn
