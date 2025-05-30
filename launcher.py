#!/usr/bin/env python3
"""
Cross-platform launcher for Router Installer
Works on both Windows and Linux
"""

import sys
import os
import platform
import subprocess

# Add scripts directory to path for imports
sys.path.append('scripts')

# Import logger after adding scripts to path
try:
    import logger
    log = logger.RouterLogger("launcher.py")
    log.info("Router Installer launcher started")
except ImportError:
    # Fallback if logger is not available
    log = None
    print("Warning: Logger not available, continuing without logging")

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
    if log:
        log.info("Checking Python dependencies")
    try:
        import requests
        import telnetlib
        import ftplib
        if log:
            log.info("All required Python modules are available")
        return True
    except ImportError as e:
        if log:
            log.error(f"Missing required Python module: {e}")
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
    print(f"{Colors.CYAN}💡 Advanced Options for Option 1 (Manual execution):{Colors.NC}")
    print(f"{Colors.WHITE}   python scripts/main.py --token <TOKEN>    {Colors.PURPLE}# Use saved token{Colors.NC}")
    print(f"{Colors.WHITE}   python scripts/main.py --skip-auth        {Colors.PURPLE}# Skip auth, enter token manually{Colors.NC}")
    print(f"{Colors.YELLOW}─────────────────────────────────────────────────────────────{Colors.NC}")
    print()

def run_script(script_name, python_cmd):
    """Run a Python script with the appropriate Python command"""
    if log:
        log.info(f"Running script: {script_name}")
    script_path = os.path.join("scripts", script_name)
    if not os.path.exists(script_path):
        if log:
            log.error(f"Script {script_name} not found at {script_path}")
        print(f"{Colors.RED}Script {script_name} not found!{Colors.NC}")
        return
    
    try:
        if log:
            log.info(f"{python_cmd} {script_path}")
        subprocess.run([python_cmd, script_path], check=True)
        if log:
            log.info(f"Script {script_name} completed successfully")
    except subprocess.CalledProcessError as e:
        if log:
            log.error(f"Script {script_name} execution failed: {e}")
        print(f"{Colors.RED}Script execution failed: {e}{Colors.NC}")
    except FileNotFoundError:
        if log:
            log.error(f"Python interpreter not found: {python_cmd}")
        print(f"{Colors.RED}Python interpreter not found: {python_cmd}{Colors.NC}")
        print(f"{Colors.YELLOW}Please install Python 3 or check your installation.{Colors.NC}")

def ftp_connect():
    """Handle FTP connection with cross-platform support"""
    if log:
        log.info("Starting FTP connection for shell mode")
    print(f"{Colors.GREEN}Starting FTP connection to shell mode...{Colors.NC}")
    print(f"{Colors.YELLOW}Username and password: root{Colors.NC}")
    print(f"{Colors.YELLOW}After all operations, the device will reboot.{Colors.NC}")
    
    # Get router IP address dynamically
    try:
        import gateway
        router_ip = gateway.get_ip_address() or '192.168.31.1'
        if log:
            log.info(f"Router IP detected: {router_ip}")
        print(f"{Colors.GREEN}Connecting to router at: {router_ip}{Colors.NC}")
    except Exception as e:
        router_ip = '192.168.31.1'
        if log:
            log.warning(f"Could not detect router IP, using default: {router_ip} - {e}")
        print(f"{Colors.YELLOW}Could not detect router IP, using default: {router_ip}{Colors.NC}")
    
    system = platform.system().lower()
    
    if system == "windows":
        # On Windows, try to use built-in ftp
        try:
            if log:
                log.info(f"ftp {router_ip}")
            subprocess.run(["ftp", router_ip])
        except FileNotFoundError:
            if log:
                log.error("FTP client not found on Windows")
            print(f"{Colors.RED}FTP client not found. Please install an FTP client.{Colors.NC}")
    else:
        # On Linux/Unix
        if subprocess.run(["which", "ftp"], capture_output=True).returncode == 0:
            if log:
                log.info(f"ftp {router_ip}")
            subprocess.run(["ftp", router_ip])
        elif subprocess.run(["which", "lftp"], capture_output=True).returncode == 0:
            print(f"{Colors.YELLOW}Using lftp instead of ftp...{Colors.NC}")
            if log:
                log.info(f"lftp ftp://root@{router_ip}")
            subprocess.run(["lftp", f"ftp://root@{router_ip}"])
        else:
            if log:
                log.error("No FTP client found on system")
            print(f"{Colors.RED}No FTP client found. Please install ftp or lftp:{Colors.NC}")
            print(f"{Colors.WHITE}Ubuntu/Debian: sudo apt install ftp{Colors.NC}")
            print(f"{Colors.WHITE}CentOS/RHEL: sudo yum install ftp{Colors.NC}")
            print(f"{Colors.WHITE}Arch: sudo pacman -S inetutils{Colors.NC}")
            print(f"{Colors.WHITE}Windows: FTP client should be built-in{Colors.NC}")

def main():
    """Main program loop"""
    if log:
        log.info("Starting main program loop")
    
    if not check_dependencies():
        input(f"{Colors.YELLOW}Press Enter to exit...{Colors.NC}")
        return
    
    python_cmd = get_python_command()
    if log:
        log.info(f"Using Python command: {python_cmd}")
    
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        try:
            choice = input(f"{Colors.CYAN}Enter the number corresponding to your action: {Colors.NC}")
            choice = int(choice.strip())
            if log:
                log.info(f"User selected menu option: {choice}")
        except (ValueError, KeyboardInterrupt):
            if log:
                log.info("User cancelled or entered invalid input")
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
            if log:
                log.warning(f"Invalid menu option selected: {choice}")
            print(f"{Colors.RED}Invalid option selected!{Colors.NC}")
        
        input(f"{Colors.YELLOW}Press Enter to continue...{Colors.NC}")
    
    if log:
        log.info("Router Installer launcher finished")

if __name__ == "__main__":
    main()
