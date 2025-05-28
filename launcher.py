#!/usr/bin/env python3
"""
Cross-platform launcher for Router Installer
Works on both Windows and Linux
"""

import sys
import os
import platform
import subprocess

# ANSI color codes (work on most modern terminals, including Windows 10+)
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    YELLOW = '\033[1;33m'
    PURPLE = '\033[0;35m'
    WHITE = '\033[1;37m'
    NC = '\033[0m'  # No Color

def clear_screen():
    """Clear screen on both Windows and Unix"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def get_python_command():
    """Get the appropriate Python command for the current system"""
    system = platform.system().lower()
    
    if system == "windows":
        # On Windows, try the bundled Python first, then system Python
        if os.path.exists("python/python.exe"):
            return "python/python.exe"
        elif os.path.exists("python3.exe"):
            return "python3.exe"
        else:
            return "python"
    else:
        # On Linux/Unix, use system Python3
        return "python3"

def check_dependencies():
    """Check if required Python modules are available"""
    try:
        import requests
        import telnetlib
        import ftplib
        return True
    except ImportError as e:
        print(f"{Colors.RED}Missing required Python module: {e}{Colors.NC}")
        print(f"{Colors.YELLOW}Please install required modules:{Colors.NC}")
        print(f"{Colors.WHITE}pip install requests{Colors.NC}")
        return False

def print_header():
    """Print fancy header"""
    print(f"{Colors.CYAN}╔════════════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║{Colors.WHITE}                        Router Installer                        {Colors.CYAN}║{Colors.NC}")
    print(f"{Colors.CYAN}║{Colors.YELLOW}                           R3GV2                               {Colors.CYAN}║{Colors.NC}")
    print(f"{Colors.CYAN}║{Colors.GREEN}                      R4A Gigabyte                             {Colors.CYAN}║{Colors.NC}")
    print(f"{Colors.CYAN}║{Colors.BLUE}                        Routers                                {Colors.CYAN}║{Colors.NC}")
    print(f"{Colors.CYAN}║{Colors.PURPLE}                    By IgorechekXD                            {Colors.CYAN}║{Colors.NC}")
    print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════════╝{Colors.NC}")
    print()

def print_menu():
    """Print menu options"""
    print(f"{Colors.YELLOW}────────────────────── Select an option ──────────────────────{Colors.NC}")
    print(f"{Colors.WHITE}        1 -- {Colors.GREEN}Enable Telnet and FTP servers{Colors.NC}")
    print(f"{Colors.WHITE}        2 -- {Colors.GREEN}Create backup of stock firmware{Colors.NC}")
    print(f"{Colors.WHITE}        3 -- {Colors.GREEN}Install bootloader to 3rd firmware partition{Colors.NC}")
    print(f"{Colors.WHITE}        4 -- {Colors.GREEN}Install firmware (OpenWRT, stock, etc.){Colors.NC}")
    print(f"{Colors.WHITE}        5 -- {Colors.GREEN}Restore backup{Colors.NC}")
    print(f"{Colors.WHITE}        6 -- {Colors.GREEN}Enter Shell mode (via FTP){Colors.NC}")
    print(f"{Colors.YELLOW}─────────────────────────────────────────────────────────────{Colors.NC}")
    print()

def run_script(script_name, python_cmd):
    """Run a Python script with the appropriate Python command"""
    script_path = os.path.join("scripts", script_name)
    if not os.path.exists(script_path):
        print(f"{Colors.RED}Script {script_name} not found!{Colors.NC}")
        return
    
    try:
        subprocess.run([python_cmd, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Script execution failed: {e}{Colors.NC}")
    except FileNotFoundError:
        print(f"{Colors.RED}Python interpreter not found: {python_cmd}{Colors.NC}")
        print(f"{Colors.YELLOW}Please install Python 3 or check your installation.{Colors.NC}")

def ftp_connect():
    """Handle FTP connection with cross-platform support"""
    print(f"{Colors.GREEN}Starting FTP connection to shell mode...{Colors.NC}")
    print(f"{Colors.YELLOW}Username and password: root{Colors.NC}")
    print(f"{Colors.YELLOW}After all operations, the device will reboot.{Colors.NC}")
    
    # Get router IP address dynamically
    try:
        sys.path.append('scripts')
        import gateway
        router_ip = gateway.get_gateway() or '192.168.31.1'
    except:
        router_ip = '192.168.31.1'
        print(f"{Colors.YELLOW}Could not detect router IP, using default: {router_ip}{Colors.NC}")
    else:
        print(f"{Colors.GREEN}Connecting to router at: {router_ip}{Colors.NC}")
    
    system = platform.system().lower()
    
    if system == "windows":
        # On Windows, try to use built-in ftp
        try:
            subprocess.run(["ftp", router_ip])
        except FileNotFoundError:
            print(f"{Colors.RED}FTP client not found. Please install an FTP client.{Colors.NC}")
    else:
        # On Linux/Unix
        if subprocess.run(["which", "ftp"], capture_output=True).returncode == 0:
            subprocess.run(["ftp", router_ip])
        elif subprocess.run(["which", "lftp"], capture_output=True).returncode == 0:
            print(f"{Colors.YELLOW}Using lftp instead of ftp...{Colors.NC}")
            subprocess.run(["lftp", f"ftp://root@{router_ip}"])
        else:
            print(f"{Colors.RED}No FTP client found. Please install ftp or lftp:{Colors.NC}")
            print(f"{Colors.WHITE}Ubuntu/Debian: sudo apt install ftp{Colors.NC}")
            print(f"{Colors.WHITE}CentOS/RHEL: sudo yum install ftp{Colors.NC}")
            print(f"{Colors.WHITE}Arch: sudo pacman -S inetutils{Colors.NC}")
            print(f"{Colors.WHITE}Windows: FTP client should be built-in{Colors.NC}")

def main():
    """Main program loop"""
    if not check_dependencies():
        input(f"{Colors.YELLOW}Press Enter to exit...{Colors.NC}")
        return
    
    python_cmd = get_python_command()
    
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        try:
            choice = input(f"{Colors.CYAN}Enter the number corresponding to your action: {Colors.NC}")
            choice = int(choice.strip())
        except (ValueError, KeyboardInterrupt):
            print(f"{Colors.RED}Invalid input or cancelled by user.{Colors.NC}")
            break
        
        if choice == 1:
            print(f"{Colors.GREEN}Script for enabling Telnet and FTP servers started...{Colors.NC}")
            run_script("main.py", python_cmd)
        elif choice == 2:
            print(f"{Colors.GREEN}Starting script for creating firmware backup...{Colors.NC}")
            run_script("createbackup.py", python_cmd)
        elif choice == 3:
            print(f"{Colors.GREEN}Starting script for bootloader installation...{Colors.NC}")
            run_script("writeuboot3.py", python_cmd)
        elif choice == 4:
            print(f"{Colors.GREEN}Starting script for firmware installation...{Colors.NC}")
            run_script("writeOS.py", python_cmd)
        elif choice == 5:
            print(f"{Colors.GREEN}Starting script for backup restoration...{Colors.NC}")
            run_script("restorebackup.py", python_cmd)
        elif choice == 6:
            ftp_connect()
        else:
            print(f"{Colors.RED}Invalid option selected!{Colors.NC}")
        
        input(f"{Colors.YELLOW}Press Enter to continue...{Colors.NC}")

if __name__ == "__main__":
    main()
