from napalm import get_network_driver
driver = get_network_driver('ios')
device = driver('10.0.1.3', 'admin', 'admin')
device.open()
arp = device.get_arp_table()

import psycopg2
connect_str = "dbname='cisco' user='cisco' host='localhost'  password='cisco'"
conn = psycopg2.connect(connect_str)
conn.autocommit = True
cursor = conn.cursor() 


for dev in arp:
    mac = dev['mac']
    ip = dev['ip']
    print(mac)
    print(ip)
    duplicate = cursor.execute(f"""select * from devices_client where ipadd='{ip}' and mac='{mac}';""")
    duplicate = cursor.fetchall()
    if not duplicate:
        cursor.execute(f"""insert into devices_client (mac, ipadd) values ('{mac}','{ip}');""")


cursor.execute("""SELECT * from devices_client""") 
rows = cursor.fetchall() 
print(rows)
