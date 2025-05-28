# OpenWRT Router Installer (R3GV2/R4A Gigabyte Routers)

A cross-platform tool for installing OpenWRT and custom firmware on Xiaomi routers (R3GV2/R4A Gigabyte models). This tool enables you to bypass manufacturer restrictions and install open-source firmware like OpenWRT, giving you full control over your router's capabilities.

## Features

- **OpenWRT Installation** - Install OpenWRT firmware to unlock advanced router features
- **Cross-platform compatibility** - Works on both Windows and Linux
- **Firmware Liberation** - Break free from manufacturer firmware limitations
- **Complete Firmware Management** - Backup, restore, and switch between firmware versions
- **Bootloader Modification** - Install custom bootloaders for advanced firmware switching
- **Administrative Access** - Enable Telnet/FTP for full router control
- **Interactive shell access** - Direct command-line access to router filesystem

## Why OpenWRT?

OpenWRT transforms your Xiaomi router into a powerful, customizable networking device:

- **Advanced Networking Features**: VPN support, advanced QoS, traffic shaping
- **Package Management**: Install additional software packages and services
- **Enhanced Security**: Regular security updates and custom firewall rules
- **Performance Optimization**: Better CPU and memory utilization
- **Network Monitoring**: Detailed bandwidth and connection monitoring
- **Custom Applications**: Run web servers, file servers, IoT controllers
- **No Vendor Lock-in**: Full control over your hardware

## Supported Routers

This tool is specifically designed for Xiaomi routers with the following chipsets and models:

- **Xiaomi R3GV2** (Mi Router 3G v2)
- **Xiaomi R4A Gigabit** (Mi Router 4A Gigabit Edition)
- Other Xiaomi routers with compatible MediaTek MT7621 chipset
- Routers running Xiaomi's stock firmware with web-based administration

### Hardware Specifications
- **CPU**: MediaTek MT7621AT (dual-core MIPS 880MHz)
- **RAM**: 128MB DDR3
- **Flash**: 16MB SPI NOR flash
- **Wireless**: 2.4GHz + 5GHz 802.11ac
- **Ports**: 2×LAN + 1×WAN Gigabit Ethernet

### Firmware Compatibility
- **Stock**: Original Xiaomi/MiWiFi firmware
- **OpenWRT**: Official OpenWRT builds for MT7621
- **LEDE**: Legacy LEDE firmware (OpenWRT predecessor)
- **Padavan**: Alternative custom firmware
- **Custom builds**: Community-built firmware variations

## Requirements

### System Requirements

- **Windows**: Windows 7 or later
- **Linux**: Any modern Linux distribution
- **Python**: Python 3.6 or later

### Python Dependencies

The tool requires the following Python modules:
- `requests` - For HTTP communication with router
- `telnetlib` - For Telnet connections (built-in)
- `ftplib` - For FTP connections (built-in)

Install dependencies:
```bash
pip install requests
```

### Additional Tools (Optional)

- **FTP Client**: For manual router access and file management
  - Linux: `ftp` or `lftp` package
  - Windows: Built-in FTP client
- **OpenWRT Firmware**: Download appropriate OpenWRT images
  - [OpenWRT Downloads](https://downloads.openwrt.org/releases/)
  - Device-specific builds for MT7621 architecture
- **SSH Client**: For secure shell access after OpenWRT installation
  - Linux: `openssh-client` (usually pre-installed)
  - Windows: Built-in SSH client (Windows 10+) or PuTTY

## Installation

1. **Download/Clone** the installer package
2. **Extract** to a directory of your choice
3. **Install Python dependencies**:
   ```bash
   pip install requests
   ```

## Directory Structure

```
Router-Installer/
├── launcher.py              # Cross-platform launcher
├── installer.sh             # Linux shell script (alternative)
├── Installer.bat            # Windows batch script (alternative)
├── README.md                # This file
├── data/                    # Required data files
│   ├── main.tar.gz         # Configuration files for enabling services
│   └── uboot3.bin          # Bootloader file
├── firmwares/               # Place firmware files here
├── scripts/                 # Python scripts
│   ├── main.py             # Enable Telnet/FTP servers
│   ├── createbackup.py     # Create firmware backup
│   ├── writeuboot3.py      # Install bootloader
│   ├── writeOS.py          # Install firmware
│   ├── restorebackup.py    # Restore from backup
│   ├── gateway.py          # Network detection utilities
│   ├── flashos.sh          # Firmware flashing script
│   └── flashall.sh         # Complete restore script
└── python/                  # Windows Python runtime (Windows only)
```

## Usage

### Quick Start

1. **Connect to your router's WiFi** or connect via Ethernet
2. **Run the launcher**:
   - **Cross-platform**: `python3 launcher.py`
   - **Linux**: `./installer.sh`
   - **Windows**: Double-click `Installer.bat`

### Menu Options

#### 1. Enable Telnet and FTP Servers
- **Purpose**: Enables administrative access to the router
- **Requirements**: Router admin password
- **What it does**:
  - Logs into router web interface
  - Uploads configuration files to enable Telnet and FTP
  - Provides access credentials (username: root, no password)

#### 2. Create Backup of Stock Firmware
- **Purpose**: Creates a complete backup of current firmware
- **Requirements**: Telnet access must be enabled first (option 1)
- **Output**: `data/backup.bin` file containing full firmware backup
- **What it does**:
  - Connects via Telnet to router
  - Creates complete MTD dump of firmware
  - Downloads backup to your computer
  - Removes temporary files from router

#### 3. Install Bootloader to 3rd Firmware Partition
- **Purpose**: Installs custom bootloader for advanced firmware management
- **Requirements**: 
  - FTP access enabled (option 1)
  - `data/uboot3.bin` file present
- **Warning**: This modifies bootloader - proceed with caution
- **What it does**:
  - Uploads bootloader file to router
  - Installs to bootloader partition
  - Enables advanced firmware switching capabilities

#### 4. Install OpenWRT/Custom Firmware
- **Purpose**: Install OpenWRT or other custom firmware to unlock advanced features
- **Requirements**:
  - FTP/Telnet access enabled (option 1)
  - OpenWRT firmware files in `firmwares/` directory
  - `scripts/flashos.sh` script present
- **Supported formats**: `.bin` firmware files (sysupgrade format recommended)
- **OpenWRT Benefits**:
  - Advanced package management with opkg
  - Custom firewall rules and VPN support
  - Real-time performance monitoring
  - SSH access and full Linux environment
  - Community support and regular updates
- **What it does**:
  - Lists available firmware files in `firmwares/` directory
  - Uploads selected OpenWRT firmware to router
  - Initiates safe firmware flashing process
  - Router reboots automatically with new firmware
  - **Note**: After OpenWRT installation, default IP is usually `192.168.1.1`

#### 5. Restore Backup
- **Purpose**: Restore router to previously backed up state
- **Requirements**:
  - FTP/Telnet access enabled (option 1)
  - `data/backup.bin` file from option 2
  - `scripts/flashall.sh` script present
- **What it does**:
  - Uploads backup file to router
  - Initiates complete firmware restoration
  - Router reboots to restored state

#### 6. Enter Shell Mode (via FTP)
- **Purpose**: Direct command-line access to router filesystem
- **Requirements**: FTP access enabled (option 1)
- **Credentials**: username `root`, password `root`
- **What it does**:
  - Automatically detects router IP
  - Opens FTP connection for manual file management
  - Provides direct access to router filesystem

## Post-Installation: Accessing OpenWRT

After successfully installing OpenWRT firmware:

### First Boot Setup
1. **Wait for reboot**: Router will restart automatically (2-3 minutes)
2. **Connect to OpenWRT**:
   - **IP Address**: `192.168.1.1` (OpenWRT default)
   - **Username**: `root`
   - **Password**: No password initially (set one immediately!)

### Initial Configuration
```bash
# Connect via SSH
ssh root@192.168.1.1

# Set root password (IMPORTANT!)
passwd

# Update package lists
opkg update

# Install web interface (if not included)
opkg install luci

# Start web interface
/etc/init.d/uhttpd start
/etc/init.d/uhttpd enable
```

### Web Interface Access
- **URL**: `http://192.168.1.1`
- **Login**: Username `root` with the password you set

### Essential OpenWRT Features
- **Package Management**: Install software with `opkg install package-name`
- **Network Configuration**: Advanced VLAN, bridge, and routing options
- **Firewall**: Sophisticated iptables-based firewall
- **VPN Support**: OpenVPN, WireGuard, and other VPN solutions
- **Monitoring**: Real-time bandwidth and system monitoring
- **File Sharing**: Samba, FTP, and other network services

## Network Detection

The tool automatically detects your router's IP address using:
- **Linux**: `ip route`, `route`, `netstat` commands
- **Windows**: `tracert`, `route print` commands
- **Fallback**: Defaults to `192.168.31.1` if detection fails

**Note**: After OpenWRT installation, the router IP typically changes to `192.168.1.1`

## Getting OpenWRT Firmware

### Official Sources
1. **OpenWRT Downloads**: https://downloads.openwrt.org/releases/
2. **Device Database**: https://openwrt.org/toh/start
3. **Search for your model**: Look for "Xiaomi Mi Router 3G v2" or "Xiaomi Mi Router 4A"

### Firmware Selection
- **Architecture**: `ramips/mt7621`
- **File type**: `*-squashfs-sysupgrade.bin` (recommended for upgrades)
- **Initial install**: `*-squashfs-factory.bin` (for first-time installation)
- **Version**: Latest stable release (avoid snapshots for production use)

### Example Download URLs
```
# For R3GV2
https://downloads.openwrt.org/releases/23.05.3/targets/ramips/mt7621/

# Look for files like:
openwrt-23.05.3-ramips-mt7621-xiaomi_mi-router-3g-v2-squashfs-sysupgrade.bin
```

## Safety and Warnings

⚠️ **Important Safety Information**:

1. **Backup First**: Always create a firmware backup (option 2) before installing OpenWRT
2. **Power Stability**: Never disconnect power during firmware flashing operations
3. **Network Stability**: Ensure stable network connection during firmware upload
4. **Compatible Firmware**: Only use OpenWRT builds specifically for your router model
5. **Bootloader Risk**: Installing custom bootloader (option 3) carries risk of bricking device
6. **Recovery Plan**: Keep stock firmware backup for emergency recovery
7. **OpenWRT Version**: Use stable releases, avoid development snapshots for production

### OpenWRT-Specific Warnings
- **IP Address Change**: Router IP will change from `192.168.31.1` to `192.168.1.1` after OpenWRT installation
- **WiFi Configuration**: WiFi will be disabled by default - configure via web interface or SSH
- **Package Space**: Router has limited storage - choose packages carefully
- **Performance**: Some features may impact performance on hardware-limited devices

## Troubleshooting

### Common Issues

#### "Router not found"
- Ensure you're connected to router's network (usually `192.168.31.1`)
- Check if router IP is different from default
- Try manually setting IP in `scripts/gateway.py`
- Verify router is running stock Xiaomi firmware (required for initial access)

#### "No firmware files found"
- Download OpenWRT firmware for your specific router model
- Place `.bin` files in the `firmwares/` directory
- Ensure filename matches expected format (`*-squashfs-sysupgrade.bin`)
- Check OpenWRT device database for compatible builds

#### "OpenWRT not accessible after installation"
- Router IP changed to `192.168.1.1` (OpenWRT default)
- Connect to new IP: `http://192.168.1.1` or `ssh root@192.168.1.1`
- WiFi may be disabled - configure via web interface
- Allow 3-5 minutes for full boot after firmware installation

#### "Incorrect password"
- Verify router admin password
- Reset router if password forgotten
- Ensure router is in normal operating mode

#### "Telnet/FTP server not running"
- Run option 1 first to enable services
- Wait a few seconds after enabling services
- Restart router if services don't start

#### "Python module not found"
- Install required modules: `pip install requests`
- Ensure Python 3 is installed and accessible
- On Linux, try `python3` instead of `python`

#### "FTP client not found" (Linux)
- Install FTP client: `sudo apt install ftp` (Debian/Ubuntu)
- Or install lftp: `sudo apt install lftp`
- Use package manager appropriate for your distribution

### Manual IP Configuration

If automatic IP detection fails, you can manually set the router IP:

1. Edit `scripts/gateway.py`
2. Comment out: `ip_address=get_gateway()`
3. Uncomment and modify: `ip_address='192.168.31.1'`
4. Replace `192.168.31.1` with your router's actual IP

## File Requirements

### Required Files (Included)
- `data/main.tar.gz` - Configuration files for enabling Telnet/FTP
- `data/uboot3.bin` - Bootloader file for option 3
- `scripts/flashos.sh` - Firmware installation script
- `scripts/flashall.sh` - Complete restoration script

### User-Provided Files
- **OpenWRT Firmware files**: Download and place `.bin` files in `firmwares/` directory
  - Get from [OpenWRT releases](https://downloads.openwrt.org/releases/)
  - Look for `openwrt-*-mt7621-*-squashfs-sysupgrade.bin`
  - Ensure compatibility with your specific router model
- **Custom Firmware**: Other compatible firmware files (Padavan, LEDE, etc.)
- **Backup files**: Created by option 2, used by option 5

## Technical Details

### Communication Protocol
1. **HTTP/HTTPS**: Initial authentication and service enabling
2. **Telnet**: Command execution on router (port 23)
3. **FTP**: File transfer operations (port 21)

### Security Considerations
- Tool requires router admin credentials
- Enables root access to router filesystem
- Creates temporary files on router during operations
- Automatically cleans up temporary files after completion

## Version History

- **v1.0**: Initial Windows-only release for Xiaomi router firmware modification
- **v2.0**: Added Linux support and cross-platform compatibility
- **v2.1**: English translation, improved UI, and OpenWRT focus
- **v2.2**: Enhanced OpenWRT documentation and post-installation guidance

## Related Projects

- **OpenWRT**: https://openwrt.org/ - The main OpenWRT project
- **OpenWRT Forums**: https://forum.openwrt.org/ - Community support and discussions
- **Device Database**: https://openwrt.org/toh/start - Hardware compatibility database
- **Package Repository**: https://openwrt.org/packages/start - Available software packages

## Credits

- **Original Author**: [IgorechekXD](https://4pda.to/forum/index.php?showtopic=988197&st=20380#entry135090727) - Initial Windows tool development
- **Cross-platform Port**: Enhanced for Linux compatibility and OpenWRT focus
- **OpenWRT Project**: The amazing open-source firmware that makes this all possible
- **Router Models**: Xiaomi R3GV2, R4A Gigabit Edition hardware support

## Community

- **OpenWRT Wiki**: Comprehensive documentation and guides
- **Reddit r/openwrt**: Community discussions and support
- **GitHub Issues**: Report bugs and request features
- **Telegram/Discord**: Real-time community chat and support

## License

This tool is provided as-is for educational and legitimate router modification purposes. Use at your own risk. The authors are not responsible for any damage to your router or network.

**OpenWRT License**: OpenWRT firmware is licensed under GPL and other open-source licenses. Respect the licensing terms of all software components.

## Disclaimer

- This tool modifies router firmware and enables installation of OpenWRT
- Improper use may result in router malfunction ("bricking")
- Installing OpenWRT will void manufacturer warranty
- Always maintain original firmware backup for recovery
- Ensure compliance with local laws and regulations regarding router modification
- OpenWRT installation changes default network configuration - plan accordingly
- Some router features may work differently or require additional configuration in OpenWRT
