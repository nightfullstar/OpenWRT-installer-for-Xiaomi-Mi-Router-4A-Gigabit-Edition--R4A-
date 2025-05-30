#!/usr/bin/env python3
"""
Comprehensive logging system for OpenWRT router installer
Provides structured logging with file and console output
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any
import json
import subprocess
import platform


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output for console"""
    
    # Color codes for different log levels
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add color to the levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        
        return super().format(record)


class RouterLogger:
    """Main logging class for the router installer"""
    
    def __init__(self, name: str = "router_installer", log_dir: str = "logs"):
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create logs directory
        os.makedirs(log_dir, exist_ok=True)
        
        # Setup handlers
        self._setup_file_handler()
        self._setup_console_handler()
        
        # Log session start
        self.info("="*60)
        self.info(f"Router Installer Logging Session Started")
        self.info(f"Platform: {platform.system()} {platform.release()}")
        self.info(f"Python: {sys.version}")
        self.info("="*60)
    
    def _setup_file_handler(self):
        """Setup file handler with detailed logging"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.log_dir, f"router_installer_{timestamp}.log")
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        self.logger.addHandler(file_handler)
        self.log_file_path = log_file
    
    def _setup_console_handler(self):
        """Setup console handler with colored output"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        console_formatter = ColoredFormatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(self._format_message(message, **kwargs))
    
    def _format_message(self, message: str, **kwargs) -> str:
        """Format message with additional context"""
        if kwargs:
            context = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
            return f"{message} | {context}"
        return message
    
    def log_step(self, step_number: int, total_steps: int, description: str):
        """Log installation step with progress"""
        progress = f"[{step_number}/{total_steps}]"
        self.info(f"{progress} {description}")
    
    def log_http_request(self, method: str, url: str, status_code: Optional[int] = None, 
                        response_time: Optional[float] = None, error: Optional[str] = None):
        """Log HTTP request details"""
        request_info = {
            'method': method,
            'url': url,
            'status_code': status_code,
            'response_time_ms': round(response_time * 1000, 2) if response_time else None,
            'error': error
        }
        
        if error:
            self.error(f"HTTP Request Failed: {method} {url}", **request_info)
        elif status_code and status_code >= 400:
            self.warning(f"HTTP Request Warning: {method} {url}", **request_info)
        else:
            self.debug(f"HTTP Request: {method} {url}", **request_info)
    
    def log_command_execution(self, command: str, return_code: Optional[int] = None,
                            stdout: Optional[str] = None, stderr: Optional[str] = None,
                            execution_time: Optional[float] = None):
        """Log system command execution"""
        cmd_info = {
            'command': command,
            'return_code': return_code,
            'execution_time_s': round(execution_time, 2) if execution_time else None
        }
        
        if return_code is not None and return_code != 0:
            self.error(f"Command Failed: {command}", **cmd_info)
            if stderr:
                self.error(f"Command Error Output: {stderr.strip()}")
        else:
            self.debug(f"Command Executed: {command}", **cmd_info)
        
        if stdout and stdout.strip():
            self.debug(f"Command Output: {stdout.strip()}")
    
    def log_telnet_session(self, host: str, port: int, command: str, 
                          response: Optional[str] = None, error: Optional[str] = None):
        """Log telnet session details"""
        session_info = {
            'host': host,
            'port': port,
            'command': command
        }
        
        if error:
            self.error(f"Telnet Session Failed: {host}:{port}", error=error, **session_info)
        else:
            self.debug(f"Telnet Command: {command}", **session_info)
            if response:
                self.debug(f"Telnet Response: {response.strip()}")
    
    def log_ftp_operation(self, operation: str, local_path: Optional[str] = None,
                         remote_path: Optional[str] = None, file_size: Optional[int] = None,
                         transfer_time: Optional[float] = None, error: Optional[str] = None):
        """Log FTP operation details"""
        ftp_info = {
            'operation': operation,
            'local_path': local_path,
            'remote_path': remote_path,
            'file_size_bytes': file_size,
            'transfer_time_s': round(transfer_time, 2) if transfer_time else None
        }
        
        if error:
            self.error(f"FTP Operation Failed: {operation}", error=error, **ftp_info)
        else:
            self.info(f"FTP Operation: {operation}", **ftp_info)
    
    def log_firmware_info(self, firmware_type: str, file_path: str, file_size: int,
                         checksum: Optional[str] = None):
        """Log firmware file information"""
        fw_info = {
            'firmware_type': firmware_type,
            'file_path': file_path,
            'file_size_bytes': file_size,
            'checksum': checksum
        }
        
        self.info(f"Firmware Info: {firmware_type}", **fw_info)
    
    def log_router_status(self, ip_address: str, status: str, firmware_version: Optional[str] = None,
                         model: Optional[str] = None):
        """Log router status information"""
        router_info = {
            'ip_address': ip_address,
            'status': status,
            'firmware_version': firmware_version,
            'model': model
        }
        
        self.info(f"Router Status: {status}", **router_info)
    
    def log_backup_operation(self, operation: str, backup_path: str, 
                           partitions: Optional[list] = None, success: bool = True):
        """Log backup operation details"""
        backup_info = {
            'operation': operation,
            'backup_path': backup_path,
            'partitions': partitions,
            'success': success
        }
        
        level = self.info if success else self.error
        level(f"Backup Operation: {operation}", **backup_info)
    
    def log_network_scan(self, target_range: str, discovered_devices: list):
        """Log network scan results"""
        scan_info = {
            'target_range': target_range,
            'devices_found': len(discovered_devices),
            'devices': discovered_devices
        }
        
        self.info(f"Network Scan Completed", **scan_info)
    
    def log_exception(self, exception: Exception, context: str = ""):
        """Log exception with full traceback"""
        import traceback
        
        exc_info = {
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'context': context
        }
        
        self.error(f"Exception Occurred: {context}", **exc_info)
        
        # Log full traceback to file only
        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.emit(logging.LogRecord(
                    name=self.logger.name,
                    level=logging.ERROR,
                    pathname="",
                    lineno=0,
                    msg=f"Full Traceback:\n{traceback.format_exc()}",
                    args=(),
                    exc_info=None
                ))
    
    def get_log_file_path(self) -> str:
        """Get the current log file path"""
        return self.log_file_path
    
    def create_context_logger(self, context: str) -> 'ContextLogger':
        """Create a context-specific logger"""
        return ContextLogger(self, context)


class ContextLogger:
    """Context-specific logger that adds context to all messages"""
    
    def __init__(self, parent_logger: RouterLogger, context: str):
        self.parent = parent_logger
        self.context = context
    
    def _add_context(self, message: str) -> str:
        return f"[{self.context}] {message}"
    
    def debug(self, message: str, **kwargs):
        self.parent.debug(self._add_context(message), **kwargs)
    
    def info(self, message: str, **kwargs):
        self.parent.info(self._add_context(message), **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.parent.warning(self._add_context(message), **kwargs)
    
    def error(self, message: str, **kwargs):
        self.parent.error(self._add_context(message), **kwargs)
    
    def critical(self, message: str, **kwargs):
        self.parent.critical(self._add_context(message), **kwargs)


# Global logger instance
_global_logger = None

def get_logger(name: str = "router_installer") -> RouterLogger:
    """Get or create global logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = RouterLogger(name)
    return _global_logger

def setup_logging(log_dir: str = "logs", name: str = "router_installer") -> RouterLogger:
    """Setup and return logger instance"""
    global _global_logger
    _global_logger = RouterLogger(name, log_dir)
    return _global_logger
