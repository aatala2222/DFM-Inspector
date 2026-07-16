@echo off
REM DFM Inspector Launcher
REM Starts the Flask server and opens the browser

cd /d "%~dp0"

echo ============================================================
echo   DFM Inspector - Starting...
echo ============================================================
echo.
echo Starting server at http://localhost:5000
echo.
echo Close this window to stop the server.
echo ============================================================
echo.

REM Wait 3 seconds then open browser (server needs time to start)
start "" /B cmd /c "timeout /t 3 /nobreak > nul && start http://localhost:5000"

REM Start the Flask server (this keeps the window open)
python app.py

REM If Python exits, pause so user can see any error messages
echo.
echo Server stopped.
pause
