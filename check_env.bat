@echo off
echo Checking Python environment...

python -c "import sys; print('Python version:', sys.version)" 
echo.

python -c "import sys; exit(0 if sys.version_info[:2] < (3, 12) else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    echo Your Python version supports all features including:
    echo - TensorFlow
    echo - PyTorch
    echo - All other ML libraries
    echo.
    echo Recommended installation: install.bat
) else (
    echo Your Python version supports all features except:
    echo - TensorFlow
    echo - PyTorch
    echo.
    echo Alternative ML libraries will be used:
    echo - LightGBM
    echo - XGBoost
    echo.
    echo Installation options:
    echo 1. install.bat - All features except TensorFlow/PyTorch
    echo 2. Install Python 3.11 first for full deep learning support
)
echo.
echo All other features will work with any Python version:
echo - Dash Dashboard
echo - Data Generation
echo - Report Generation
echo - Data Collection
echo - Basic ML features
pause 