import os
import sys
import subprocess
import venv
from pathlib import Path
import webbrowser
import socket
import time

class AppSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.python_path = self.venv_path / "Scripts" / "python.exe"
        self.pip_path = self.venv_path / "Scripts" / "pip.exe"

    def setup_virtual_environment(self):
        """Create and configure virtual environment"""
        if not self.venv_path.exists():
            print("Creating virtual environment...")
            try:
                # Try to use Python 3.10 or 3.11 specifically
                python_paths = [
                    r"C:\Python310\python.exe",
                    r"C:\Python311\python.exe",
                    "python3.10",
                    "python3.11",
                    "python"
                ]
                
                python_cmd = None
                for path in python_paths:
                    try:
                        result = subprocess.run([path, "--version"], capture_output=True, text=True)
                        if result.returncode == 0:
                            python_cmd = path
                            break
                    except:
                        continue
                
                if not python_cmd:
                    raise Exception("Compatible Python version not found. Please install Python 3.10 or 3.11")
                
                venv.create(self.venv_path, with_pip=True)
                
                # Upgrade pip and install essential packages
                subprocess.run([str(self.python_path), "-m", "pip", "install", "--upgrade", "pip"])
                subprocess.run([str(self.python_path), "-m", "pip", "install", "--upgrade", "setuptools", "wheel"])
            except Exception as e:
                print(f"Error creating virtual environment: {e}")
                sys.exit(1)

    def install_requirements(self):
        """Install required packages"""
        try:
            print("Installing core dependencies...")
            # Install numpy and pandas first (they're often dependencies for other packages)
            subprocess.run([str(self.pip_path), "install", "numpy>=1.24.3", "pandas>=2.1.4"])
            
            print("Installing other requirements...")
            subprocess.run([str(self.pip_path), "install", "-r", "requirements.txt"])
            
            print("Installing package in development mode...")
            subprocess.run([str(self.pip_path), "install", "-e", "."])
        except Exception as e:
            print(f"Error installing requirements: {str(e)}")
            sys.exit(1)

    def create_directories(self):
        """Create necessary directories"""
        directories = [
            "app",
            "app/config",
            "app/auth",
            "app/utils",
            "app/monitoring",
            "app/ml",
            "app/integrations",
            "app/static",
            "app/static/css",
            "app/static/js",
            "app/templates",
            "reports",
            "logs"
        ]
        
        print("Creating project structure...")
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py files
            if directory.startswith("app"):
                init_file = Path(directory) / "__init__.py"
                if not init_file.exists():
                    init_file.write_text("")

        # Create main app __init__.py
        app_init = """from pathlib import Path
APP_ROOT = Path(__file__).parent
PROJECT_ROOT = APP_ROOT.parent
"""
        (Path("app") / "__init__.py").write_text(app_init)

    def run_application(self):
        """Run the application"""
        try:
            # Add the project root to Python path
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root)
            
            # Get IP address
            ip_address = self.get_local_ip()
            port = 8050
            url = f"http://{ip_address}:{port}"

            print(f"\nStarting Cyber Threat Intelligence Platform...")
            print(f"The application will be available at: {url}")
            
            # Open browser after a delay
            def open_browser():
                time.sleep(2)
                webbrowser.open(url)

            import threading
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.start()

            # Run the application
            subprocess.run([str(self.python_path), "launch.py"], env=env)
        except Exception as e:
            print(f"Error running application: {str(e)}")
            sys.exit(1)

    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

def main():
    try:
        setup = AppSetup()
        
        # Clean up existing virtual environment if it exists
        if setup.venv_path.exists():
            print("Removing existing virtual environment...")
            import shutil
            shutil.rmtree(setup.venv_path)
        
        # Setup virtual environment
        setup.setup_virtual_environment()
        
        # Create directories
        setup.create_directories()
        
        # Install requirements
        setup.install_requirements()
        
        # Run the application
        setup.run_application()

    except Exception as e:
        print(f"Error: {str(e)}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main() 