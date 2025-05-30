import sys
import telnetlib
import ftplib

import gateway
import logger

# Initialize logging
log = logger.RouterLogger("writeuboot3.py")
log.info("Starting bootloader installation process")

router_ip_address=gateway.get_ip_address()
log.info(f"Router IP address: {router_ip_address}")

try:	
	log.info("Opening bootloader file uboot3.bin")
	file=open('data/uboot3.bin', 'rb')
	log.info("Bootloader file opened successfully")
except Exception as e:
	log.error(f"Bootloader file uboot3.bin not found: {e}")
	print("Bootloader file uboot3.bin not found.")
	sys.exit(1)

try:	
	log.info("Connecting to FTP server")
	ftp=ftplib.FTP(router_ip_address)
	log.info("FTP connection established")
except Exception as e:
	log.error(f"FTP server is not running: {e}")
	print("FTP server is not running.")
	file.close()
	sys.exit(1)

print("Uploading uboot3.bin to router...")
log.info("Uploading bootloader file to router via FTP")
try:
	ftp.storbinary(f'STOR /tmp/uboot3.bin', file)
	file.close()
	ftp.quit()
	log.info("Bootloader file uploaded successfully")
except Exception as e:
	log.error(f"Failed to upload bootloader file: {e}")
	file.close()
	ftp.quit()
	sys.exit(1)

log.info("Connecting to telnet server for bootloader installation")
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
print("Installing bootloader...")
log.warning("Writing bootloader to flash memory - this is a critical operation!")
log.info("mtd -e Bootloader write /tmp/uboot3.bin Bootloader")
tn.write(b"mtd -e Bootloader write /tmp/uboot3.bin Bootloader\n")
tn.read_until(b"root@XiaoQiang:~#")
tn.write(b"exit\n")
log.info("Bootloader installation completed successfully!")
print("Done! You can press any key to close the window.")
