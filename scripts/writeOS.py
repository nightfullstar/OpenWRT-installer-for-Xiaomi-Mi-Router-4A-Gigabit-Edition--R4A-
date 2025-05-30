import os
import os
import sys
import telnetlib
import ftplib

import gateway
import logger

# Initialize logging
log = logger.RouterLogger("writeOS.py")
log.info("Starting firmware installation process")

router_ip_address=gateway.get_ip_address()
log.info(f"Router IP address: {router_ip_address}")
	
log.info("Scanning for firmware files in firmwares directory")
firmware_files = []
firmware_path = ""
firmware_count = 0

# Check if firmwares directory exists
if not os.path.exists('firmwares'):
	log.error("Firmwares directory not found")
	print("❌ Error: 'firmwares' directory not found.")
	print("Please create a 'firmwares' directory and place your firmware files there.")
	sys.exit(1)

for path, dirs, files in os.walk('firmwares'):
	# Filter for common firmware file extensions
	firmware_extensions = ['.bin', '.img', '.trx', '.tar.gz', '.tar.bz2', '.tar.xz']
	valid_files = [f for f in files if any(f.lower().endswith(ext) for ext in firmware_extensions)]
	
	firmware_count = len(valid_files)
	if firmware_count <= 0:
		log.error("No firmware files found in firmwares directory")
		print("❌ No firmware files found in 'firmwares' directory.")
		print("Supported formats: .bin, .img, .trx, .tar.gz, .tar.bz2, .tar.xz")
		print("Please place your firmware files in the 'firmwares' directory.")
		sys.exit(1)
		
	log.info(f"Found {firmware_count} firmware files")
	firmware_files = valid_files
	firmware_path = path
	
	print("📦 Available firmware files:")
	print("-" * 50)
	i = 1
	while i <= len(valid_files):
		file_size = os.path.getsize(os.path.join(path, valid_files[i-1]))
		size_mb = file_size / (1024 * 1024)
		print(f"({i}) {valid_files[i-1]} [{size_mb:.1f} MB]")
		i += 1
	print("-" * 50)
	break  # Only process the first directory

print()
try:
	selection = input("🎯 Select firmware and press the corresponding number: ").strip()
	i = int(selection)
	log.info(f"User selected firmware option: {i}")
except (ValueError, KeyboardInterrupt) as e:
	log.error(f"Invalid input or cancelled: {e}")
	print("❌ Invalid input or operation cancelled.")
	sys.exit(1)

if i <= 0 or i > firmware_count:
	log.error(f"Invalid firmware selection: {i} (valid range: 1-{firmware_count})")
	print(f"❌ Invalid selection. Please choose a number between 1 and {firmware_count}.")
	sys.exit(1)

selected_firmware = firmware_files[i-1]
selected_path = os.path.join(firmware_path, selected_firmware)
log.info(f"Selected firmware: {selected_firmware}")

# Verify file exists and is readable
if not os.path.exists(selected_path):
	log.error(f"Selected firmware file not found: {selected_path}")
	print(f"❌ Firmware file not found: {selected_firmware}")
	sys.exit(1)

file_size = os.path.getsize(selected_path)
if file_size == 0:
	log.error(f"Selected firmware file is empty: {selected_firmware}")
	print(f"❌ Firmware file is empty: {selected_firmware}")
	sys.exit(1)

print(f"✅ Selected: {selected_firmware} ({file_size / (1024*1024):.1f} MB)")
	
try:
	file1 = open(selected_path, 'rb')
	log.info(f"Opened firmware file: {selected_firmware}")
except Exception as e:
	log.error(f"Cannot open firmware file: {e}")
	print(f"❌ Cannot open firmware file: {e}")
	sys.exit(1)

try:	
	file2 = open('scripts/flashos.sh', 'rb')
	log.info("Opened flash script: flashos.sh")
except FileNotFoundError:
	log.error("Flash script not found: scripts/flashos.sh")
	print("❌ Flash script not found: scripts/flashos.sh")
	print("Please ensure the scripts directory contains flashos.sh")
	file1.close()
	sys.exit(1)
except Exception as e:
	log.error(f"Cannot open flash script: {e}")
	print(f"❌ Cannot open flash script: {e}")
	file1.close()
	sys.exit(1)

print("\n🔌 Connecting to router FTP server...")
try:	
	log.info("Connecting to FTP server")
	ftp = ftplib.FTP(router_ip_address)
	ftp.login('root', '')  # Login with root and no password
	log.info("FTP connection established")
	print("✅ Connected to FTP server")
except ftplib.error_perm as e:
	log.error(f"FTP authentication failed: {e}")
	print("❌ FTP authentication failed. Make sure Telnet/FTP services are enabled (option 1).")
	file1.close()
	file2.close()
	sys.exit(1)
except Exception as e:
	log.error(f"FTP server connection failed: {e}")
	print("❌ Cannot connect to FTP server.")
	print("Please ensure Telnet/FTP services are enabled first (option 1).")
	file1.close()
	file2.close()
	sys.exit(1)
	
print("📤 Uploading firmware to router...")
print("⚠️  This may take several minutes depending on file size...")
log.info(f"Uploading firmware file: {selected_firmware}")

try:
	# Upload firmware file
	print(f"   Uploading {selected_firmware}...")
	ftp.storbinary(f'STOR /tmp/sysupgrade.bin', file1)
	log.info("Firmware file uploaded successfully")
	print("   ✅ Firmware uploaded")
	
	# Upload flash script
	print("   Uploading flash script...")
	ftp.storbinary(f'STOR /tmp/flashos.sh', file2)
	log.info("Flash script uploaded successfully")
	print("   ✅ Flash script uploaded")
	
	file1.close()
	file2.close()
	ftp.quit()
	print("✅ All files uploaded successfully")
	
except ftplib.error_perm as e:
	log.error(f"FTP permission error: {e}")
	print(f"❌ FTP permission error: {e}")
	file1.close()
	file2.close()
	ftp.quit()
	sys.exit(1)
except Exception as e:
	log.error(f"Failed to upload files: {e}")
	print(f"❌ Upload failed: {e}")
	file1.close()
	file2.close()
	try:
		ftp.quit()
	except:
		pass
	sys.exit(1)

print("\n🔗 Connecting to router via Telnet...")
log.info("Connecting to telnet server for firmware installation")
try:
	tn = telnetlib.Telnet(router_ip_address, timeout=10)
	log.info("Telnet connection established")
	print("✅ Connected to Telnet server")
except Exception as e:
	log.error(f"Failed to connect to telnet server: {e}")
	print("❌ Cannot connect to Telnet server.")
	print("Please ensure Telnet/FTP services are enabled first (option 1).")
	sys.exit(1)

try:
	# Wait for login prompt
	tn.read_until(b"XiaoQiang login:", timeout=5)
	log.debug("Logging in as root")
	tn.write(b"root\n")
	
	# Wait for shell prompt
	tn.read_until(b"root@XiaoQiang:~#", timeout=5)
	log.info("Successfully logged in via telnet")
	print("✅ Logged in to router shell")
	
except Exception as e:
	log.error(f"Telnet login failed: {e}")
	print("❌ Failed to login via Telnet")
	tn.close()
	sys.exit(1)

# Execute firmware flash
print("\n⚠️  CRITICAL: Starting firmware installation!")
print("🚨 DO NOT POWER OFF THE ROUTER DURING THIS PROCESS!")
print("🚨 POWER INTERRUPTION MAY BRICK YOUR DEVICE!")
print("\n⏳ Starting firmware flash process...")

log.warning("Starting firmware flash process - DO NOT POWER OFF ROUTER!")
flash_command = "nohup sh /tmp/flashos.sh >/dev/null 2>&1 &"
log.info(f"Executing: {flash_command}")

try:
	tn.write(flash_command.encode() + b"\n")
	tn.read_until(b"root@XiaoQiang:~#", timeout=10)
	log.info("Firmware installation command executed successfully")
	
	print("✅ Firmware installation started successfully!")
	print("\n" + "="*60)
	print("🎉 FIRMWARE INSTALLATION IN PROGRESS")
	print("="*60)
	print("⏰ The router is now flashing the firmware")
	print("⚠️  DO NOT POWER OFF the router during this process!")
	print("🔄 The router will reboot automatically when complete")
	print("⏱️  This process typically takes 3-5 minutes")
	print("💡 You can safely close this window")
	print("="*60)
	
except Exception as e:
	log.error(f"Failed to execute flash command: {e}")
	print(f"❌ Failed to start firmware installation: {e}")
finally:
	try:
		tn.close()
	except:
		pass

log.info("Firmware installation process initiated successfully")

