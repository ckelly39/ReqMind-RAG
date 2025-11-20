@echo off
REM ReqMind Installation Script for Windows
REM This script will clean up old packages and install compatible versions

echo ========================================
echo ReqMind Installation Script
echo ========================================
echo.

REM Check if virtual environment is activated
python -c "import sys; sys.exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)"
if %errorlevel% neq 0 (
    echo ERROR: Virtual environment is not activated!
    echo.
    echo Please activate your virtual environment first:
    echo   venv\Scripts\activate
    echo.
    pause
    exit /b 1
)

echo Step 1: Uninstalling old LangChain packages...
pip uninstall -y langchain langchain-community langchain-core langchain-text-splitters 2>nul

echo.
echo Step 2: Installing compatible packages...
pip install --upgrade pip
pip install langchain>=0.3.0 langchain-community>=0.3.0 langchain-core>=0.3.0

echo.
echo Step 3: Installing remaining dependencies...
pip install chromadb>=0.4.22
pip install sentence-transformers>=2.3.1
pip install pypdf>=3.17.4
pip install huggingface-hub>=0.20.3
pip install requests>=2.31.0
pip install python-dotenv>=1.0.0
pip install typing-extensions>=4.12.0

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Edit .env and add your HUGGINGFACE_API_KEY
echo 3. Create 'data' folder and add your PDF files
echo 4. Run: cd src ^&^& python main.py
echo.
pause
