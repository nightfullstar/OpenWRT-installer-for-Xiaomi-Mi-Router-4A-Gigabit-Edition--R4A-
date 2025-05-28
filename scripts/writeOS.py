import os
import sys
import telnetlib
import ftplib

import gateway
router_ip_address=gateway.get_ip_address()
	
for path,dirs,files in os.walk('firmwares'):
	c=len(files)
	if c <= 0:
		print ("No firmware files found.")
		sys.exit(1)
	i=1
	while i <= len(files):
		print("(%d) %s" % (i, files[i-1]))
		i += 1
print()
try:
	i = int(input("Select firmware and press the corresponding number: "))
except:
	print ("Input error.")
	sys.exit(1)

if i <= 0 or i > c:
	print ("Incorrect selection.")
	sys.exit(1)
	
file1=open(os.path.join(path,files[i-1]), 'rb')

try:	
	file2=open('scripts/flashos.sh', 'rb')
except:
	print ("Script not found.")
	sys.exit(1)

try:	
	ftp=ftplib.FTP(router_ip_address)
except:
	print ("FTP server is not running.")
	sys.exit(1)
	
print ("Uploading firmware to router...")
ftp.storbinary(f'STOR /tmp/sysupgrade.bin', file1)
ftp.storbinary(f'STOR /tmp/flashos.sh', file2)
file1.close()
file2.close()
ftp.quit()

tn = telnetlib.Telnet(router_ip_address)
tn.read_until(b"XiaoQiang login:")
tn.write(b"root\n")
tn.read_until(b"root@XiaoQiang:~#")
tn.write(b"nohup sh /tmp/flashos.sh >/dev/null 2>&1 &\n")
tn.read_until(b"root@XiaoQiang:~#",10)
print ("Router started flashing the OS.")
print ("Do not turn off the router!")
print ("After firmware installation, the router will reboot automatically.")
print ("You can press any key to close the window.")

