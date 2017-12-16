from django.db import models
from django.utils import timezone

# Create your models here.



class Device(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=3)
    ipadd = models.GenericIPAddressField()
    user = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def publish(self):
        self.save()
    def __str__(self):
        return self.name

#class Client(models.Model):
