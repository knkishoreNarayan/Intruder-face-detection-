#!/usr/bin/env python3
"""
CCTV Auto-Start Script
Automatically starts the CCTV monitoring system
"""

import requests
import time
import sys

def start_cctv_system():
    """Start the CCTV monitoring system automatically"""
    print("🚀 Starting CCTV Security System...")
    
    # Wait for Flask server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test camera first
        print("📷 Testing camera...")
        response = requests.get('http://localhost:5000/test_camera')
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print(f"✅ {data['message']}")
            else:
                print(f"❌ Camera test failed: {data['message']}")
                return False
        else:
            print("❌ Server not responding")
            return False
        
        # Start monitoring
        print("🎥 Starting continuous monitoring...")
        response = requests.get('http://localhost:5000/start_monitoring')
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print(f"✅ {data['message']}")
                print("🔒 CCTV system is now active and monitoring continuously")
                print("📊 Check http://localhost:5000 for live feed and statistics")
                return True
            else:
                print(f"❌ Failed to start monitoring: {data['message']}")
                return False
        else:
            print("❌ Server not responding")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure app.py is running.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("CCTV Security System Auto-Start")
    print("=" * 50)
    
    success = start_cctv_system()
    
    if success:
        print("\n🎯 CCTV system is now running!")
        print("💡 Press Ctrl+C to stop the system")
        print("🌐 Open http://localhost:5000 in your browser")
        
        try:
            # Keep the script running
            while True:
                time.sleep(10)
                # Check if system is still running
                try:
                    response = requests.get('http://localhost:5000/get_status')
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('camera_active'):
                            print("🟢 CCTV system running normally...")
                        else:
                            print("🔴 CCTV system stopped")
                            break
                except:
                    print("🔴 Server connection lost")
                    break
        except KeyboardInterrupt:
            print("\n🛑 Stopping CCTV system...")
            try:
                requests.get('http://localhost:5000/stop_monitoring')
                print("✅ CCTV system stopped")
            except:
                print("⚠️ Could not stop system gracefully")
    else:
        print("\n❌ Failed to start CCTV system")
        print("🔧 Please check the troubleshooting guide")
        sys.exit(1) 