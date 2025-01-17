@echo off
echo Installing Cyber Threat Intelligence Platform dependencies...

:: Check Python version and warn if incompatible
python -m pip install packaging
python -c "from packaging import version; import sys; ver = version.parse(sys.version.split()[0]); exit(0 if ver < version.parse('3.12') else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    echo Current Python version is compatible for all features
    set FULL_ML=1
) else (
    echo WARNING: Python version 3.11 or lower is required for TensorFlow/PyTorch
    echo Current version:
    python --version
    echo.
    echo 1. Continue with alternative ML features
    echo 2. Exit and install Python 3.11
    echo.
    choice /C 12 /M "Select an option"
    if errorlevel 2 exit /b 1
    set FULL_ML=0
)

:: Create and activate virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

:: Install setuptools and wheel first
echo Installing setuptools and wheel...
python -m pip install --upgrade pip
pip install setuptools wheel

:: Install core dependencies using pre-built wheels
echo Installing core dependencies...
pip install numpy==1.24.3 --only-binary :all:
pip install pandas==2.1.4 --only-binary :all:
pip install dash==2.14.2 dash-bootstrap-components==1.5.0 flask==3.0.2
pip install plotly==5.18.0 python-dateutil==2.8.2
pip install faker==22.6.0 reportlab==4.1.0

:: Install ML and Data Science packages
echo Installing ML and Data Science packages...
pip install scikit-learn==1.4.0
pip install statsmodels==0.14.1
pip install transformers==4.37.2

:: Install Deep Learning packages based on Python version
if "%FULL_ML%"=="1" (
    echo Installing TensorFlow and PyTorch...
    pip install tensorflow==2.15.0
    pip install torch==2.2.0 --index-url https://download.pytorch.org/whl/cpu
) else (
    echo Installing alternative ML libraries...
    pip install lightgbm==4.3.0
    pip install xgboost==2.0.3
)

:: Install Data Collection and Processing packages
echo Installing Data Collection and Processing packages...
pip install redis==5.0.1
pip install celery==5.3.6
pip install beautifulsoup4==4.12.3
pip install scrapy==2.11.0
pip install tweepy==4.14.0

:: Install Additional dependencies
echo Installing Additional dependencies...
pip install requests>=2.31.0
pip install aiohttp>=3.9.1
pip install urllib3>=2.1.0

:: Create startup scripts
echo Creating startup scripts...

:: Create full startup script
echo @echo off > run.bat
echo echo Starting Cyber Threat Intelligence Platform... >> run.bat
echo call venv\Scripts\activate >> run.bat
echo set PYTHONPATH=%%PYTHONPATH%%;%%CD%% >> run.bat
if "%FULL_ML%"=="0" (
    echo set USE_ALTERNATIVE_ML=1 >> run.bat
)
echo python app/main.py >> run.bat
echo pause >> run.bat

echo.
echo Installation complete!
echo.
if "%FULL_ML%"=="1" (
    echo All features are available!
) else (
    echo Using alternative ML libraries (no TensorFlow/PyTorch)
    echo For deep learning features, install Python 3.11
)
echo.
echo To run the application:
echo - Double-click run.bat
echo.
pause 