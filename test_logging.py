#!/usr/bin/env python3
"""
Test script to verify logging system integration
"""

import sys
import os

print("Starting logging test...")

# Add scripts directory to path
sys.path.append('scripts')
print("Scripts path added")

try:
    import logger
    print("Logger module imported successfully")
    
    # Test logger
    log = logger.RouterLogger("test_logging")
    print("Logger instance created")
    
    print("Testing logging system...")
    log.info("This is an info message")
    log.info("This is a success message (using info)")
    log.warning("This is a warning message")
    log.error("This is an error message")
    log.debug("This is a debug message")
    log.info("Command: echo 'This is a command log'")
    log.log_http_request("GET", "http://example.com", 200)
    
    print("Logging system test completed successfully!")
    log.info("All logging tests passed")
    
except Exception as e:
    print(f"Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
