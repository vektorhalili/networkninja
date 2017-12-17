from __future__ import absolute_import, unicode_literals
from devices.models import Device
from devices.models import Client
from napalm import get_network_driver
from celery.decorators import task

#logger = get_task_logger(__name__)

#@task(name="testtest")
#def testtest():
#	print('testtest')
#	logger.info("Start task")
#	now = datetime.now()
#	result = scrapers.scraper_example(now.day, now.minute)
#	logger.info("Task finished: result = %i" % result)



@task(name="update_all_arp")
def update_all_arp():
    try:
        devices = Device.objects.all()
        for singledevice in devices:
            type = singledevice.type
            ipadd = singledevice.ipadd
            user = singledevice.user
            password = singledevice.password
            driver = get_network_driver(type)
            device = driver(ipadd, user, password)
            device.open()
            arp = device.get_arp_table()
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
                    if cmaccheck.mac and cipaddcheck.ipadd:
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
            print('Failed to get the arp table from a device')
