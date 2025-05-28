import sys
import re
import time
import random
import hashlib
import requests
import socket

import gateway
router_ip_address=gateway.get_ip_address()

try: 
	r0 = requests.get("http://{router_ip_address}/cgi-bin/luci/web".format(router_ip_address=router_ip_address))
except:
	print ("Router not found.")
	sys.exit(1)
try:	
	mac = re.findall(r'deviceId = \'(.*?)\'', r0.text)[0]
except:
	print ("Incorrect router model.")
	sys.exit(1)
key = re.findall(r'key: \'(.*)\',', r0.text)[0]
nonce = "0_" + mac + "_" + str(int(time.time())) + "_" + str(random.randint(1000, 10000))
account_str = hashlib.sha1((input("Enter password: ") + key).encode('utf-8')).hexdigest()
password = hashlib.sha1((nonce + account_str).encode('utf-8')).hexdigest()
data = "username=admin&password={password}&logtype=2&nonce={nonce}".format(password=password,nonce=nonce)
r1 = requests.post("http://{router_ip_address}/cgi-bin/luci/api/xqsystem/login".format(router_ip_address=router_ip_address), 
	data = data, 
	headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})

try:	
	stok = re.findall(r'"token":"(.*?)"',r1.text)[0]
except:
	print ("Incorrect password.")
	sys.exit(1)

print("Loading configuration files...")
requests.post("http://{router_ip_address}/cgi-bin/luci/;stok={stok}/api/misystem/c_upload".format(router_ip_address=router_ip_address,stok=stok), files={"image":open("data/main.tar.gz",'rb')})

print("Starting telnet and ftpd servers...")
requests.get("http://{router_ip_address}/cgi-bin/luci/;stok={stok}/api/xqnetdetect/netspeed".format(router_ip_address=router_ip_address,stok=stok))
print("Done! You can press any key to close the window.")
print("There are 3 ways to connect to the router:")
print("FTP - using 'ftp 192.168.31.1'.")
print("Telnet - using 'telnet 192.168.31.1'.")
print("Through option 6.")