@echo off
echo Installing Cyber Threat Intelligence Platform...

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or later.
    pause
    exit /b 1
)

:: Create and activate virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

:: Upgrade pip and install core dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install setuptools wheel

:: Create directory structure using PowerShell
echo Creating project structure...
powershell -ExecutionPolicy Bypass -File setup_dirs.ps1

:: Install requirements
echo Installing project requirements...
pip install -r requirements.txt

:: Install the package in development mode
echo Installing package in development mode...
pip install -e .

:: Create run script
echo @echo off > run.bat
echo call venv\Scripts\activate >> run.bat
echo python launch.py >> run.bat

echo.
echo Installation complete!
echo.
echo To start the application:
echo 1. Run: run.bat
echo.
pause