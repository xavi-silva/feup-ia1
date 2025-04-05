@echo off
setlocal

echo ================================
echo "Bird Sorter Setup & Launcher"
echo ================================

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed!
    echo Download and install it from: https://www.python.org/downloads
    pause
    exit /b
)

REM Show Python version
echo Python found: 
python --version

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM Run the game
echo Launching game...
cd src
python main.py

endlocal
