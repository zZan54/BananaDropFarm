@echo off

python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in the PATH.
    echo Please install Python and try again.
    pause
    exit /b 1
)

pip --version > nul 2>&1
if errorlevel 1 (
    echo pip is not installed or not in the PATH.
    echo Please install pip and try again.
    pause
    exit /b 1
)

pip install -r requirements.txt
echo All requirements installed.