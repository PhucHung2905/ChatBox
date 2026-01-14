@echo off
REM Real Estate ChatBox v2.0 - Windows Startup Script
REM Features: Authentication, SQL Server, Admin Panel

setlocal enabledelayedexpansion

:menu
cls
echo.
echo =========================================================
echo   REAL ESTATE CHATBOX v2.0 - Startup Menu
echo   (With Authentication, SQL Server, Admin Panel)
echo =========================================================
echo.
echo SETUP:
echo 1. Setup Database (SQL Server)
echo 2. Install Dependencies
echo 3. Create/Activate Virtual Environment
echo.
echo RUN:
echo 4. Start Backend (Flask API on port 5000)
echo 5. Start Frontend (Open http://localhost:5000)
echo 6. Start Both Backend and Frontend
echo.
echo UTILITIES:
echo 7. Check Installation
echo 8. View Configuration (.env)
echo 9. Database Migration Script
echo 10. Exit
echo.

set /p choice="Enter choice (1-10): "

if "%choice%"=="1" goto setup_db
if "%choice%"=="2" goto install_deps
if "%choice%"=="3" goto setup_venv
if "%choice%"=="4" goto start_backend
if "%choice%"=="5" goto start_frontend
if "%choice%"=="6" goto start_both
if "%choice%"=="7" goto check_install
if "%choice%"=="8" goto view_config
if "%choice%"=="9" goto run_migration
if "%choice%"=="10" goto exit
goto invalid

REM ==================== Database Setup ====================
:setup_db
cls
echo.
echo =========================================================
echo   SQL Server Database Setup
echo =========================================================
echo.
echo This application uses SQL Server for data storage.
echo.
echo REQUIREMENTS:
echo - SQL Server 2016+ or SQL Server Express
echo - ODBC Driver 17 for SQL Server
echo.
echo SETUP STEPS:
echo 1. Install SQL Server from: https://www.microsoft.com/en-us/sql-server
echo 2. Install ODBC Driver 17: https://aka.ms/downloadodbc
echo 3. Create a .env file in the 'backend' folder with:
echo.
echo    DB_SERVER=localhost
echo    DB_NAME=ChatBoxDB
echo    DB_USER=sa
echo    DB_PASSWORD=your_password
echo    DB_DRIVER={ODBC Driver 17 for SQL Server}
echo    JWT_SECRET_KEY=your-secret-key-here
echo    ADMIN_EMAIL=admin@chatbox.local
echo    ADMIN_PASSWORD=admin123
echo.
echo 4. Run the migration script: python migrate.py
echo 5. Or manually run the SQL script in SQL Server Management Studio
echo.
echo Press any key to continue...
pause > nul
goto menu

REM ==================== Install Dependencies ====================
:install_deps
cls
echo.
echo Installing Dependencies...
echo.
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)
call venv\Scripts\activate.bat
echo.
echo Installing Python packages...
pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Dependencies installed successfully!
echo Press any key to continue...
pause > nul
goto menu

REM ==================== Virtual Environment ====================
:setup_venv
cls
echo.
echo Setting up Virtual Environment...
echo.
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install --upgrade pip
    echo Virtual environment created and activated!
) else (
    echo Virtual environment already exists.
    call venv\Scripts\activate.bat
    echo Virtual environment activated!
)
echo.
echo Press any key to continue...
pause > nul
goto menu

REM ==================== Start Backend ====================
:start_backend
cls
echo.
echo Starting Backend Server...
echo.
echo Access API at: http://localhost:5000
echo Health check: http://localhost:5000/health
echo.
cd backend
if not exist venv (
    echo Virtual environment not found. Creating...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo.
python app.py
pause
goto menu

REM ==================== Start Frontend ====================
:start_frontend
cls
echo.
echo Starting Frontend...
echo.
start http://localhost:5000
timeout /t 2 > nul
cd frontend
python -m http.server 8080 --directory .
pause
goto menu

REM ==================== Start Both ====================
:start_both
cls
echo.
echo Starting Backend and Frontend...
echo.
echo Backend will run on: http://localhost:5000
echo Frontend will run on: http://localhost:5000
echo.
cd backend
if not exist venv (
    echo Virtual environment not found. Creating...
    python -m venv venv
)
call venv\Scripts\activate.bat

REM Start backend in a new window
start "ChatBox Backend" cmd /k python app.py

REM Wait for backend to start
timeout /t 3 > nul

REM Open frontend in browser
start http://localhost:5000

echo.
echo Both services started!
echo Press Ctrl+C in the backend window to stop the server.
echo.
pause
goto menu

REM ==================== Check Installation ====================
:check_install
cls
echo.
echo Checking Installation...
echo.

REM Check Python
python --version > nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python is installed
    python --version
) else (
    echo [FAIL] Python not found
)
echo.

REM Check pip
pip --version > nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] pip is installed
) else (
    echo [FAIL] pip not found
)
echo.

REM Check if backend folder exists
if exist "backend" (
    echo [OK] Backend folder exists
) else (
    echo [FAIL] Backend folder not found
)
echo.

REM Check if frontend folder exists
if exist "frontend" (
    echo [OK] Frontend folder exists
) else (
    echo [FAIL] Frontend folder not found
)
echo.

REM Check if requirements.txt exists
if exist "backend\requirements.txt" (
    echo [OK] requirements.txt found
) else (
    echo [FAIL] requirements.txt not found
)
echo.

REM Check Python packages
cd backend
if exist venv (
    call venv\Scripts\activate.bat
    echo.
    echo Checking Python packages:
    pip list | findstr "flask flask-sqlalchemy flask-jwt"
) else (
    echo [INFO] Virtual environment not yet created
)

cd ..
echo.
echo Press any key to continue...
pause > nul
goto menu

REM ==================== View Configuration ====================
:view_config
cls
echo.
echo Configuration (.env file)
echo.
if exist backend\.env (
    echo [Current .env content]:
    echo.
    type backend\.env
) else (
    echo [.env file not found]
    echo.
    echo Create a .env file in the 'backend' folder with these settings:
    echo.
    echo    FLASK_ENV=development
    echo    DEBUG=True
    echo    PORT=5000
    echo    SECRET_KEY=your-secret-key-here
    echo.
    echo    DATABASE SETTINGS:
    echo    DB_SERVER=localhost
    echo    DB_NAME=ChatBoxDB
    echo    DB_USER=sa
    echo    DB_PASSWORD=your_password
    echo    DB_DRIVER={ODBC Driver 17 for SQL Server}
    echo.
    echo    JWT SETTINGS:
    echo    JWT_SECRET_KEY=your-secret-key-here
    echo    JWT_ACCESS_TOKEN_EXPIRES=86400
    echo.
    echo    ADMIN SETTINGS:
    echo    ADMIN_EMAIL=admin@chatbox.local
    echo    ADMIN_PASSWORD=admin123
    echo.
    echo    API SETTINGS:
    echo    GEMINI_API_KEY=your-gemini-api-key
    echo    GEMINI_MODEL=gemini-2.5-flash
)
echo.
echo Press any key to continue...
pause > nul
goto menu

REM ==================== Run Migration ====================
:run_migration
cls
echo.
echo Running Database Migration...
echo.
cd backend
if not exist venv (
    echo Virtual environment not found. Creating...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo.
python migrate.py
echo.
echo Press any key to continue...
pause > nul
goto menu

REM ==================== Invalid Choice ====================
:invalid
cls
echo Invalid choice. Please try again.
timeout /t 2 > nul
goto menu

REM ==================== Exit ====================
:exit
echo.
echo Thank you for using Real Estate ChatBox v2.0!
echo.
echo For more information:
echo - GitHub: https://github.com/your-repo/chatbox
echo - Documentation: See README.md
echo.
echo Goodbye!
timeout /t 2 > nul
exit /b 0

:start_frontend
cls
echo.
echo Starting Frontend Server on http://localhost:8000...
echo.
cd frontend
python -m http.server 8000
pause
goto menu

:start_both
cls
echo.
echo Starting both servers...
echo Please note: This will open 2 terminal windows
echo.
pause

start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python app.py"
timeout /t 3
start "Frontend Server" cmd /k "cd frontend && python -m http.server 8000"

echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8000
echo.
pause
goto menu

:open_browser
cls
echo.
echo Opening Frontend in default browser...
echo.
start "" frontend\index.html
timeout /t 2
goto menu

:check_install
cls
echo.
echo Checking Installation...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python not found. Please install Python 3.8+
) else (
    echo [OK] Python installed
)

if exist backend (
    echo [OK] Backend folder exists
) else (
    echo [FAIL] Backend folder not found
)

if exist frontend (
    echo [OK] Frontend folder exists
) else (
    echo [FAIL] Frontend folder not found
)

if exist datasets (
    echo [OK] Datasets folder exists
) else (
    echo [FAIL] Datasets folder not found
)

if exist backend\.env (
    echo [OK] .env file configured
) else (
    echo [WARN] .env file not found - Run option 6 first
)

echo.
pause
goto menu

:setup_venv
cls
echo.
echo Setting up Virtual Environment...
echo.
cd backend

if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo Virtual environment created
)

call venv\Scripts\activate.bat
echo Virtual environment activated

if not exist .env (
    echo.
    echo Creating .env file...
    if exist .env.example (
        copy .env.example .env
        echo .env created. Please edit it with your OpenAI API key:
        echo - Open backend\.env with notepad
        echo - Replace "your_api_key_here" with your actual OpenAI API key
        notepad .env
    )
)

echo.
pause
goto menu

:install_deps
cls
echo.
echo Installing Dependencies...
echo.
cd backend

if not exist venv (
    echo Creating virtual environment first...
    python -m venv venv
)

call venv\Scripts\activate.bat
echo Installing packages from requirements.txt...
pip install -r requirements.txt

echo.
echo Installation complete!
pause
goto menu

:invalid
cls
echo Invalid choice. Please try again.
timeout /t 2
goto menu

:exit
echo.
echo Thank you for using Real Estate ChatBox!
echo.
exit /b
