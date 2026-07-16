@echo off
REM DFM Inspector - Reliable Server Startup Script
REM This batch file ensures the server starts correctly every time

echo ========================================
echo DFM INSPECTOR - Starting Server
echo ========================================
echo.

REM Change to the script's directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version
echo.

echo [2/3] Starting Flask server...
echo Server will be available at: http://127.0.0.1:5000
echo.
echo IMPORTANT: Keep this window open while using the application
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

REM Start the server
python start_server.py

REM If server exits, pause so user can see any errors
echo.
echo ========================================
echo Server has stopped
echo ========================================
pause
