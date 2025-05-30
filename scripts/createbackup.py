import sys
import telnetlib
import ftplib

import gateway
import logger

# Initialize logging
log = logger.RouterLogger("createbackup.py")
log.info("Starting firmware backup process")

router_ip_address=gateway.get_ip_address()
log.info(f"Router IP address: {router_ip_address}")
	
try:	
	log.info("Connecting to telnet server")
	tn = telnetlib.Telnet(router_ip_address)
	log.info("Telnet connection established")
except Exception as e:
	log.error(f"Telnet server is not running: {e}")
	print("Telnet server is not running.")
	sys.exit(1)
tn.read_until(b"XiaoQiang login:")
log.debug("Logging in as root")
tn.write(b"root\n")
tn.read_until(b"root@XiaoQiang:~#")
log.info("Successfully logged in via telnet")
print("Creating full firmware backup...")
log.info("Starting firmware backup creation (dd command)")
log.info("dd if=/dev/mtd0 of=/tmp/backup.bin")
tn.write(b"dd if=/dev/mtd0 of=/tmp/backup.bin\n")
tn.read_until(b"root@XiaoQiang:~#")
log.info("Firmware backup created successfully")
tn.write(b"exit\n")

log.info("Connecting to FTP server for file download")
try:
	ftp=ftplib.FTP(router_ip_address)
	log.info("FTP connection established")
except Exception as e:
	log.error(f"Failed to connect to FTP server: {e}")
	print("Failed to connect to FTP server.")
	sys.exit(1)

try:
	file=open('data/backup.bin', 'wb')
	print("Downloading backup to computer...")
	log.info("Downloading backup.bin from router")
	ftp.retrbinary(f'RETR /tmp/backup.bin', file.write)
	file.close()
	ftp.quit()
	log.info("Backup file downloaded successfully")
except Exception as e:
	log.error(f"Failed to download backup file: {e}")
	print("Failed to download backup file.")
	sys.exit(1)

log.info("Cleaning up temporary files on router")
tn = telnetlib.Telnet(router_ip_address)
tn.read_until(b"XiaoQiang login:")
tn.write(b"root\n")
tn.read_until(b"root@XiaoQiang:~#")
print("Removing temporary files...")
log.info("rm /tmp/backup.bin")
tn.write(b"rm /tmp/backup.bin\n")
tn.read_until(b"root@XiaoQiang:~#")
tn.write(b"exit\n")
log.info("Firmware backup process completed successfully!")
print("Done! You can press any key to close the window.")
