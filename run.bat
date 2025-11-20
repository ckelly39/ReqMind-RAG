@echo off
REM ReqMind - Easy Run Script for Windows

echo ========================================
echo Starting ReqMind
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run: install_windows.bat first
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment is activated
python -c "import sys; sys.exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" 2>nul
if %errorlevel% neq 0 (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if .env exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo.
    echo Please create .env file with your HUGGINGFACE_API_KEY
    echo You can copy .env.example and edit it:
    echo   copy .env.example .env
    echo   notepad .env
    echo.
    pause
    exit /b 1
)

REM Check if data directory exists
if not exist "data\" (
    echo WARNING: data directory not found!
    echo.
    echo Creating data directory...
    mkdir data
    echo Please add your PDF files to the 'data' folder
    echo.
    pause
    exit /b 1
)

echo Starting ReqMind...
echo.

cd src
python main.py

cd ..
pause
