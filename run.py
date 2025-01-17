import subprocess
import sys
import venv
from pathlib import Path
import webbrowser
import time
import os

def setup_project():
    """Set up the project environment"""
    project_root = Path(__file__).parent
    
    # Add project root to Python path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    venv_path = project_root / "venv"
    
    # Create virtual environment if it doesn't exist
    if not venv_path.exists():
        print("Creating virtual environment...")
        venv.create(venv_path, with_pip=True)
    
    # Get paths
    if sys.platform == "win32":
        python_path = venv_path / "Scripts" / "python.exe"
        pip_path = venv_path / "Scripts" / "pip.exe"
    else:
        python_path = venv_path / "bin" / "python"
        pip_path = venv_path / "bin" / "pip"
    
    # Install dependencies
    print("Installing dependencies...")
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"])
    subprocess.run([str(pip_path), "install", "-e", "."])
    
    return python_path, project_root

def main():
    try:
        # Setup the project
        python_path, project_root = setup_project()
        
        # Start the application
        print("\nStarting Cyber Threat Intelligence Platform...")
        url = "http://localhost:8050"
        print(f"The application will be available at: {url}")
        
        # Set environment variables
        env = os.environ.copy()
        env["PYTHONPATH"] = str(project_root)
        
        # Run the application
        subprocess.run([str(python_path), "launch.py"], env=env)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main() 