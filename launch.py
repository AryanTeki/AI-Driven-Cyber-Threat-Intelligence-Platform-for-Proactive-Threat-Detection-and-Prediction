#!/usr/bin/env python
import os
import sys
from pathlib import Path
import socket

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def setup_environment():
    """Setup the Python environment"""
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    os.environ.setdefault('FLASK_ENV', 'development')

def main():
    try:
        setup_environment()
        from app.main import app
        
        host = "0.0.0.0"  # Listen on all interfaces
        port = 8050
        
        print(f"\nStarting Cyber Threat Intelligence Platform...")
        print(f"The application will be available at:")
        print(f"- Local: http://localhost:{port}")
        print(f"- Network: http://{get_local_ip()}:{port}")
        
        app.run_server(debug=True, host=host, port=port)
        
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()