#!/usr/bin/env python3
"""
Gomoku Bot Battle Launcher
A simple script to start the game server with helpful information.
"""

import socket
import subprocess
import sys
import time

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "localhost"

def main():
    """Main launcher function"""
    print("🎮 GOMOKU BOT BATTLE")
    print("=" * 50)
    print("Starting the game server...")
    print()
    
    # Get local IP
    local_ip = get_local_ip()
    
    print("📱 Network Information:")
    print(f"   Local URL: http://localhost:8080")
    print(f"   Network URL: http://{local_ip}:8080")
    print()
    
    print("🤖 For Teams:")
    print(f"   1. Open a web browser")
    print(f"   2. Visit: http://{local_ip}:8080")
    print(f"   3. Write your bot code in the text areas")
    print(f"   4. Click 'Save Bots' and 'Start Game'")
    print()
    
    print("📋 Instructions:")
    print("   - Teams can create bots using JavaScript")
    print("   - No installation required - just a web browser!")
    print("   - See README.md for detailed instructions")
    print()
    
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    print()
    
    try:
        # Import and run the server
        from server import run_server
        run_server()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("Make sure you have Python 3.x installed")
        sys.exit(1)

if __name__ == "__main__":
    main() 