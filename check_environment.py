import sys
import pkg_resources
import subprocess

def check_environment():
    print("Checking Python environment...")
    print(f"Python version: {sys.version}")
    
    required_packages = [
        'flask',
        'flask-login',
        'dash',
        'dash-bootstrap-components',
        'plotly',
        'numpy',
        'pandas',
        'scikit-learn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            pkg_resources.require(package)
            print(f"✓ {package} is installed")
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package)
            print(f"✗ {package} is missing")
    
    if missing_packages:
        print("\nMissing packages. Installing...")
        for package in missing_packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print("\nAll required packages are installed!")

if __name__ == "__main__":
    try:
        check_environment()
    except Exception as e:
        print(f"Error checking environment: {str(e)}")
    input("\nPress Enter to exit...") 