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
	file=open('data/uboot3.bin', 'rb')
except:
	print ("Bootloader file uboot3.bin not found.")
	sys.exit(1)
print ("Uploading uboot3.bin to router...")
ftp.storbinary(f'STOR /tmp/uboot3.bin', file)
file.close()
ftp.quit()

tn = telnetlib.Telnet(router_ip_address)
tn.read_until(b"XiaoQiang login:")
tn.write(b"root\n")
tn.read_until(b"root@XiaoQiang:~#")
print ("Installing bootloader...")
tn.write(b"mtd -e Bootloader write /tmp/uboot3.bin Bootloader\n")
tn.read_until(b"root@XiaoQiang:~#")
tn.write(b"exit\n")
print ("Done! You can press any key to close the window.")
