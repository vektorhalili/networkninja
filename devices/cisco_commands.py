from napalm import get_network_driver


def get_device_arp(ipadd, type, user, password):
    try:
        driver = get_network_driver(type)
        enable = {'secret': password}
        device = driver(ipadd, user, password, optional_args=enable)
        device.open()
        arp = device.get_arp_table()
        device.close()
    except:
        arp={'error': 'error'}
    return arp
def get_device_config(ipadd, type, user, password):
    try:
        driver = get_network_driver(type)
        optional_args = {'secret': password}
        device = driver(ipadd, user, password, optional_args=optional_args)
        device.open()
        config = device.get_config()
        #config = config['startup']
        device.close()
    except Exception:
        config='was not able to pull device config'
    return config
def get_device_facts(ipadd, type, user, password):
    try:
        driver = get_network_driver(type)
        optional_args = {'secret': password}
        device = driver(ipadd, user, password, optional_args=optional_args)
        device.open()
        devicefacts = device.get_facts()
        device.close()
    except Exception:
        devicefacts='was not able to pull device facts'
    return devicefacts

def device_action(action, ipadd, type, user, password):
    if action == 'get_device_config':
        config = get_device_config(ipadd, type, user, password)
        return config
    elif action == 'get_device_arp':
        arp = get_device_arp(ipadd, type, user, password)
        return arp
    elif action == 'get_device_facts':
        facts = get_device_facts(ipadd, type, user, password)
        return facts
