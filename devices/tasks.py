from __future__ import absolute_import, unicode_literals
from devices.models import *
from napalm import get_network_driver
from devices.cisco_commands import *
from celery.decorators import task




@task(name="update_all_arp")
def update_all_arp():
    try:
        try:
            devices = Device.objects.all()
        except Exception:
            print('failed to read the DB')
        for device in devices:
            try:
                arp = get_device_arp(device.ipadd, device.type, device.user, device.password)
            except Exception:
                print('failed to execute get device arp command')
            for dev in arp:
                try:
                    newmac = dev['mac']
                    newipadd = dev['ip']
                    newclient = Client(mac=newmac, ipadd=newipadd)
                    newclient.save()
                    print('added the client')
                except Exception:
                    print('failed to put the device into the DB')
            #once done with the device, close the connection
            device.close()
    except Exception:
            print(f'Failed to get the arp table from a device: {device.name}')
