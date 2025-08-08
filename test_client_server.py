#!/usr/bin/env python3
"""
Test script to verify client-server communication
"""

import subprocess
import time
import requests
import signal
import sys

def test_client_server():
    """Test the client-server communication"""
    print("🧪 Testing client-server communication...")
    
    # Start server on different port
    print("Starting server...")
    server_process = subprocess.Popen(['python3', '-c', 'from server import run_server; run_server(8081)'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test server is responding
        print("Testing server response...")
        response = requests.get('http://localhost:8081/api/game-state', timeout=5)
        if response.status_code == 200:
            print("✅ Server is responding correctly")
        else:
            print("❌ Server not responding correctly")
            return False
        
        # Test client connection
        print("Testing client connection...")
        client_process = subprocess.Popen(['python3', 'client_python.py', 'localhost:8081'], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        
        # Let client run for a few seconds
        time.sleep(5)
        
        # Check if client is still running (not crashed)
        if client_process.poll() is None:
            print("✅ Client is running correctly")
            client_process.terminate()
            client_process.wait()
        else:
            print("❌ Client crashed")
            return False
        
        print("✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        # Clean up
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    success = test_client_server()
    sys.exit(0 if success else 1) 