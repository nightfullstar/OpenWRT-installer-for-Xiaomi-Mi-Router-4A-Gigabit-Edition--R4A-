import sys
import telnetlib
import ftplib

import gateway
import logger

# Initialize logging
log = logger.RouterLogger("restorebackup.py")
log.info("Starting backup restoration process")

router_ip_address=gateway.get_ip_address()
log.info(f"Router IP address: {router_ip_address}")

try:	
	log.info("Connecting to FTP server")
	ftp=ftplib.FTP(router_ip_address)
	log.info("FTP connection established")
except Exception as e:
	log.error(f"FTP server is not running: {e}")
	print("FTP server is not running.")
	sys.exit(1)
	
try:	
	log.info("Opening backup file: backup.bin")
	file1=open('data/backup.bin', 'rb')
	log.info("Backup file opened successfully")
except Exception as e:
	log.error(f"backup.bin not found: {e}")
	print("backup.bin not found.")
	sys.exit(1)
	
try:	
	log.info("Opening flash script: flashall.sh")
	file2=open('scripts/flashall.sh', 'rb')
	log.info("Flash script opened successfully")
except Exception as e:
	log.error(f"Script flashall.sh not found: {e}")
	print("Script flashall.sh not found.")
	sys.exit(1)
print("Uploading backup to router...")
log.info("Uploading backup file to router")
try:
	ftp.storbinary(f'STOR /tmp/backup.bin', file1)
	log.info("Backup file uploaded successfully")
	ftp.storbinary(f'STOR /tmp/flashall.sh', file2)
	log.info("Flash script uploaded successfully")
	file1.close()
	file2.close()
	ftp.quit()
except Exception as e:
	log.error(f"Failed to upload files: {e}")
	file1.close()
	file2.close()
	ftp.quit()
	sys.exit(1)

log.info("Connecting to telnet server for backup restoration")
try:
	tn = telnetlib.Telnet(router_ip_address)
	log.info("Telnet connection established")
except Exception as e:
	log.error(f"Failed to connect to telnet server: {e}")
	print("Telnet server is not running.")
	sys.exit(1)

tn.read_until(b"XiaoQiang login:")
log.debug("Logging in as root")
tn.write(b"root\n")
tn.read_until(b"root@XiaoQiang:~#")
log.info("Successfully logged in via telnet")
log.warning("Starting backup restoration - DO NOT POWER OFF ROUTER!")
log.info("sh /tmp/flashall.sh >/dev/null 2>&1 &")
tn.write(b"sh /tmp/flashall.sh >/dev/null 2>&1 &\n")
tn.read_until(b"root@XiaoQiang:~#",10)
log.info("Backup restoration started successfully")
print("Router started restoring from backup.")
print("Do not turn off the router!")
print("After backup restoration, the router will reboot automatically.")
print("You can press any key to close the window.")

