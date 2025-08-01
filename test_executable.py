#!/usr/bin/env python3
"""
Test script to verify that executable files are allowed in the repository.
This script should be allowed since we removed 'executable' from the blob store check.
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    """Main function to test executable functionality."""
    print("=" * 50)
    print("EXECUTABLE FILE TEST")
    print("=" * 50)
    print(f"Script: {__file__}")
    print(f"Current time: {datetime.now()}")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Test some basic functionality
    print("\n--- System Information ---")
    try:
        result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
        print(f"System: {result.stdout.strip()}")
    except Exception as e:
        print(f"Could not get system info: {e}")
    
    # Test file operations
    print("\n--- File Operations Test ---")
    test_file = "/tmp/test_executable_script.txt"
    try:
        with open(test_file, 'w') as f:
            f.write("This is a test file created by the executable script.\n")
        print(f"Successfully created: {test_file}")
        
        # Clean up
        os.remove(test_file)
        print(f"Successfully removed: {test_file}")
    except Exception as e:
        print(f"Error with file operations: {e}")
    
    print("\n--- Environment Variables ---")
    important_vars = ['PATH', 'HOME', 'USER', 'PWD']
    for var in important_vars:
        value = os.environ.get(var, 'Not set')
        print(f"{var}: {value}")
    
    print("\n" + "=" * 50)
    print("Test completed successfully!")
    print("This executable Python script should be allowed in the repository.")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())