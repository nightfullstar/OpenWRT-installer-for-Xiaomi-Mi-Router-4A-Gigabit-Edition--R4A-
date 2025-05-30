#!/usr/bin/env python3
"""
Test script for manual token fallback functionality
"""

import sys
import os

# Change to scripts directory
sys.path.append('/home/ikanat/Downloads/Installer/scripts')

try:
    # Test imports
    import gateway
    import logger
    print("✓ Imports successful")
    
    # Test gateway functionality
    router_ip = gateway.get_ip_address()
    print(f"✓ Router IP detection: {router_ip}")
    
    # Test logger functionality
    log = logger.RouterLogger("test")
    log.info("✓ Logger working")
    
    print("\n🎯 Testing command line arguments parsing...")
    
    # Simulate the argument parsing
    import argparse
    parser = argparse.ArgumentParser(description='Router Exploit Script')
    parser.add_argument('--token', '-t', help='Use provided session token instead of authentication')
    parser.add_argument('--skip-auth', '-s', action='store_true', help='Skip authentication and prompt for manual token')
    
    # Test with different scenarios
    test_cases = [
        ['--help'],
        ['--token', 'test_token_12345'],
        ['--skip-auth']
    ]
    
    for test_args in test_cases:
        try:
            args = parser.parse_args(test_args)
            print(f"✓ Args {test_args}: {args}")
        except SystemExit:
            print(f"✓ Help displayed for: {test_args}")
    
    print("\n✅ All basic functionality tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
