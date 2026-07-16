#!/usr/bin/env python3
"""
Reliable Server Startup Script for DFM Inspector
Handles common connection issues and provides diagnostics
"""
import socket
import sys
import os
import subprocess
import time

def check_port_available(port=5000):
    """Check if port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', port))
        sock.close()
        return True
    except OSError:
        return False

def find_process_on_port(port=5000):
    """Find process using the port"""
    try:
        if sys.platform == 'win32':
            result = subprocess.run(
                ['netstat', '-ano'], 
                capture_output=True, 
                text=True
            )
            for line in result.stdout.split('\n'):
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    pid = parts[-1]
                    return pid
        else:
            result = subprocess.run(
                ['lsof', '-i', f':{port}'], 
                capture_output=True, 
                text=True
            )
            lines = result.stdout.split('\n')
            if len(lines) > 1:
                return lines[1].split()[1]
    except Exception as e:
        print(f"Error finding process: {e}")
    return None

def kill_process_on_port(port=5000):
    """Kill process using the port"""
    pid = find_process_on_port(port)
    if pid:
        try:
            if sys.platform == 'win32':
                subprocess.run(['taskkill', '/F', '/PID', pid], check=True)
            else:
                subprocess.run(['kill', '-9', pid], check=True)
            print(f"✓ Killed process {pid} on port {port}")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"✗ Error killing process: {e}")
            return False
    return False

def check_dependencies():
    """Check if required packages are installed"""
    required = {
        'flask': 'flask',
        'numpy': 'numpy',
        'trimesh': 'trimesh',
        'cascadio': 'cascadio',
        'matplotlib': 'matplotlib',
        'docx': 'python-docx'
    }
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    return missing

def main():
    print("=" * 70)
    print("🔍 DFM INSPECTOR - Server Startup")
    print("=" * 70)
    print()
    
    # Check dependencies
    print("1. Checking dependencies...")
    missing = check_dependencies()
    if missing:
        print(f"   ✗ Missing packages: {', '.join(missing)}")
        print(f"   Run: pip install -r requirements.txt")
        return 1
    print("   ✓ All dependencies installed")
    print()
    
    # Check if port is available
    print("2. Checking port 5000...")
    if not check_port_available(5000):
        print("   ⚠ Port 5000 is already in use")
        response = input("   Kill existing process? (y/n): ")
        if response.lower() == 'y':
            if kill_process_on_port(5000):
                print("   ✓ Port 5000 is now available")
            else:
                print("   ✗ Could not free port 5000")
                print("   Try manually: netstat -ano | findstr :5000")
                return 1
        else:
            print("   ✗ Cannot start server - port in use")
            return 1
    else:
        print("   ✓ Port 5000 is available")
    print()
    
    # Check if app.py exists
    print("3. Checking app.py...")
    if not os.path.exists('app.py'):
        print("   ✗ app.py not found!")
        print("   Make sure you're in the DFM PRO directory")
        return 1
    print("   ✓ app.py found")
    print()
    
    # Start server
    print("4. Starting Flask server...")
    print("=" * 70)
    print()
    print("✓ Server starting...")
    print("✓ Open your browser: http://127.0.0.1:5000")
    print("✓ Alternative: http://localhost:5000")
    print()
    print("⌨️  Press Ctrl+C to stop")
    print("=" * 70)
    print()
    
    # Import and run app
    try:
        import app
        app.app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped by user")
        return 0
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Check if all dependencies are installed: pip install -r requirements.txt")
        print("2. Check if port 5000 is available: netstat -ano | findstr :5000")
        print("3. Try running directly: python app.py")
        return 1

if __name__ == '__main__':
    sys.exit(main())
