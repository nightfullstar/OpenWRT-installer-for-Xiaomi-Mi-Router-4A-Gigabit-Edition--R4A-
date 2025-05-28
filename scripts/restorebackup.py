import sys
import telnetlib
import ftplib

import gateway
router_ip_address=gateway.get_ip_address()

try:	
	ftp=ftplib.FTP(router_ip_address)
except:
	print ("FTP server is not running.")
	sys.exit(1)
try:	
	file1=open('data/backup.bin', 'rb')
except:
	print ("backup.bin not found.")
	sys.exit(1)
try:	
	file2=open('scripts/flashall.sh', 'rb')
except:
	print ("Script flashall.sh not found.")
	sys.exit(1)
print ("Uploading backup to router...")
ftp.storbinary(f'STOR /tmp/backup.bin', file1)
ftp.storbinary(f'STOR /tmp/flashall.sh', file2)
file1.close()
file2.close()
ftp.quit()

tn = telnetlib.Telnet(router_ip_address)
tn.read_until(b"XiaoQiang login:")
tn.write(b"root\n")
tn.read_until(b"root@XiaoQiang:~#")
tn.write(b"sh /tmp/flashall.sh >/dev/null 2>&1 &\n")
tn.read_until(b"root@XiaoQiang:~#",10)
print ("Router started restoring from backup.")
print ("Do not turn off the router!")
print ("After backup restoration, the router will reboot automatically.")
print ("You can press any key to close the window.")

