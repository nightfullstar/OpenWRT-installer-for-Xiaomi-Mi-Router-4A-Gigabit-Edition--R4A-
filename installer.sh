#!/bin/bash

# Set colors for fancy UI
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

clear

# Fancy header with colors
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${WHITE}                        Router Installer                        ${CYAN}║${NC}"
echo -e "${CYAN}║${YELLOW}                           R3GV2                               ${CYAN}║${NC}"
echo -e "${CYAN}║${GREEN}                      R4A Gigabyte                             ${CYAN}║${NC}"
echo -e "${CYAN}║${BLUE}                        Routers                                ${CYAN}║${NC}"
echo -e "${CYAN}║${PURPLE}                    By IgorechekXD                            ${CYAN}║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}────────────────────── Select an option ──────────────────────${NC}"
echo -e "${WHITE}        1 -- ${GREEN}Enable Telnet and FTP servers${NC}"
echo -e "${WHITE}        2 -- ${GREEN}Create backup of stock firmware${NC}"
echo -e "${WHITE}        3 -- ${GREEN}Install bootloader to 3rd firmware partition${NC}"
echo -e "${WHITE}        4 -- ${GREEN}Install firmware (OpenWRT, stock, etc.)${NC}"
echo -e "${WHITE}        5 -- ${GREEN}Restore backup${NC}"
echo -e "${WHITE}        6 -- ${GREEN}Enter Shell mode (via FTP)${NC}"
echo -e "${YELLOW}─────────────────────────────────────────────────────────────${NC}"
echo ""
echo -ne "${CYAN}Enter the number corresponding to your action: ${NC}"
read f
n=$f

case $n in
    1)
        echo -e "${GREEN}Script for enabling Telnet and FTP servers started...${NC}"
        python3 scripts/main.py
        echo -e "${YELLOW}Press any key to continue...${NC}"
        read -n 1
        ;;
    2)
        echo -e "${GREEN}Starting script for creating firmware backup...${NC}"
        python3 scripts/createbackup.py
        echo -e "${YELLOW}Press any key to continue...${NC}"
        read -n 1
        ;;
    3)
        echo -e "${GREEN}Starting script for bootloader installation...${NC}"
        python3 scripts/writeuboot3.py
        echo -e "${YELLOW}Press any key to continue...${NC}"
        read -n 1
        ;;
    4)
        echo -e "${GREEN}Starting script for firmware installation...${NC}"
        python3 scripts/writeOS.py
        echo -e "${YELLOW}Press any key to continue...${NC}"
        read -n 1
        ;;
    5)
        echo -e "${GREEN}Starting script for backup restoration...${NC}"
        python3 scripts/restorebackup.py
        echo -e "${YELLOW}Press any key to continue...${NC}"
        read -n 1
        ;;
    6)
        echo -e "${GREEN}Starting FTP connection to shell mode...${NC}"
        echo -e "${YELLOW}Username and password: root${NC}"
        echo -e "${YELLOW}After all operations, the device will reboot.${NC}"
        echo -e "${CYAN}Note: You may need to install an FTP client if not available.${NC}"
        
        # Get router IP address dynamically
        router_ip=$(python3 -c "import sys; sys.path.append('scripts'); import gateway; print(gateway.get_gateway() or '192.168.31.1')" 2>/dev/null)
        if [ -z "$router_ip" ]; then
            router_ip="192.168.31.1"
            echo -e "${YELLOW}Could not detect router IP, using default: $router_ip${NC}"
        else
            echo -e "${GREEN}Connecting to router at: $router_ip${NC}"
        fi
        
        # Check if ftp client is available
        if command -v ftp &> /dev/null; then
            ftp $router_ip
        elif command -v lftp &> /dev/null; then
            echo -e "${YELLOW}Using lftp instead of ftp...${NC}"
            lftp ftp://root@$router_ip
        else
            echo -e "${RED}No FTP client found. Please install ftp or lftp:${NC}"
            echo -e "${WHITE}Ubuntu/Debian: sudo apt install ftp${NC}"
            echo -e "${WHITE}CentOS/RHEL: sudo yum install ftp${NC}"
            echo -e "${WHITE}Arch: sudo pacman -S inetutils${NC}"
        fi
        echo -e "${YELLOW}Press any key to continue...${NC}"
        read -n 1
        ;;
    *)
        echo -e "${RED}Invalid option selected!${NC}"
        echo -e "${YELLOW}Press any key to continue...${NC}"
        read -n 1
        ;;
esac

clear
exec "$0"