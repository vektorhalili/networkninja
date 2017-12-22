from __future__ import absolute_import, unicode_literals
from devices.models import *
from napalm import get_network_driver
from devices.cisco_commands import *
from celery.decorators import task




@task(name="update_all_arp")
def update_all_arp():
    try:
        devices = Device.objects.all()
        for device in devices:
            arp = get_device_arp(device.ipadd, device.type, device.user, device.password)
            for dev in arp:
                cmac = dev['mac']
                cipadd = dev['ip']
                #check if mac or IP are already in DB before adding
                try:
                    cmaccheck = Client.objects.get(mac=cmac)
                    cipaddcheck = Client.objects.get(ipadd=cipadd)
                except Exception:
                    pass
                #note I put this in a try block and pass because it will fail often
                try:
                    if cmaccheck.mac or cipaddcheck.ipadd:
                        print('the mac and ip are already in the db')
                        continue
                except Exception:
                    pass
                #I put this outside of the block so it does not fail with the if
                client = Client(mac=cmac,ipadd=cipadd)
                client.save()
                print('added the client')
            #once done with the device, close the connection
            device.close()
    except Exception:
            print(f'Failed to get the arp table from a device: {device.name}')
