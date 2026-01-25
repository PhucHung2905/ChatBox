@echo off
REM ChatBox Backend Startup Script (Windows)
REM This script starts the Flask backend server

echo.
echo =========================================================
echo   ChatBox Backend - Starting Server
echo =========================================================
echo.

REM Navigate to backend folder
cd /d "%~dp0backend"

echo 📁 Working directory: %cd%
echo 🐍 Python: %PYTHON%
echo.

REM Check if virtual environment exists
if exist "..\\.venv\\Scripts\\activate.bat" (
    echo ✓ Virtual environment found
    call "..\\.venv\\Scripts\\activate.bat"
) else (
    echo ⚠️  Virtual environment not found
    echo Creating virtual environment...
    python -m venv ..\\.venv
    call "..\\.venv\\Scripts\\activate.bat"
)

echo.
echo 🚀 Starting Flask Backend...
echo 📍 Server will run on: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
