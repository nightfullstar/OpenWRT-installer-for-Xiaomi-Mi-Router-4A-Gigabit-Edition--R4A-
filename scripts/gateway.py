import sys
import os
import subprocess
import re

def get_gateway():
	try:
		# Try to get default gateway using ip route (modern Linux)
		with open(os.devnull, 'w') as devnull:
			output = subprocess.check_output(["ip", "route", "show", "default"], stderr=devnull)
		decode = output.decode("utf-8")
		# Extract gateway IP from output like "default via 192.168.31.1 dev wlan0"
		match = re.search(r'default via (\d+\.\d+\.\d+\.\d+)', decode)
		if match:
			return match.group(1)
	except:
		pass
	
	try:
		# Fallback: try route command (older Linux systems)
		with open(os.devnull, 'w') as devnull:
			output = subprocess.check_output(["route", "-n"], stderr=devnull)
		decode = output.decode("utf-8")
		lines = decode.split("\n")
		for line in lines:
			if line.startswith("0.0.0.0"):
				parts = line.split()
				if len(parts) >= 2:
					return parts[1]
	except:
		pass
	
	try:
		# Another fallback: netstat
		with open(os.devnull, 'w') as devnull:
			output = subprocess.check_output(["netstat", "-rn"], stderr=devnull)
		decode = output.decode("utf-8")
		lines = decode.split("\n")
		for line in lines:
			if "0.0.0.0" in line and "UG" in line:
				parts = line.split()
				for part in parts:
					if re.match(r'^\d+\.\d+\.\d+\.\d+$', part) and part != "0.0.0.0":
						return part
	except:
		pass
	
	return None

def get_ip_address():
	print("Getting IP address for router access...")
	ip_address=get_gateway()
# Can't find router? Then comment the line above and uncomment the line below
#	ip_address='192.168.31.1'
	if not ip_address:
		print("IP address not found.")
		sys.exit(1)

	print("IP address for router access: {ip_address}".format(ip_address=ip_address))
	return ip_address
