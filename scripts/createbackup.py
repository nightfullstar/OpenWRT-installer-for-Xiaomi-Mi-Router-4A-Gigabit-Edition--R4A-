import sys
import telnetlib
import ftplib

import gateway
router_ip_address=gateway.get_ip_address()
	
try:	
	tn = telnetlib.Telnet(router_ip_address)
except:
	print ("Telnet server is not running.")
	sys.exit(1)
tn.read_until(b"XiaoQiang login:")
tn.write(b"root\n")
tn.read_until(b"root@XiaoQiang:~#")
print ("Creating full firmware backup...")
tn.write(b"dd if=/dev/mtd0 of=/tmp/backup.bin\n")
tn.read_until(b"root@XiaoQiang:~#")
tn.write(b"exit\n")

ftp=ftplib.FTP(router_ip_address)
file=open('data/backup.bin', 'wb')
print ("Downloading backup to computer...")
ftp.retrbinary(f'RETR /tmp/backup.bin', file.write)
file.close()
ftp.quit()

tn = telnetlib.Telnet(router_ip_address)
tn.read_until(b"XiaoQiang login:")
tn.write(b"root\n")
tn.read_until(b"root@XiaoQiang:~#")
print ("Removing temporary files...")
tn.write(b"rm /tmp/backup.bin\n")
tn.read_until(b"root@XiaoQiang:~#")
tn.write(b"exit\n")
print ("Done! You can press any key to close the window.")
