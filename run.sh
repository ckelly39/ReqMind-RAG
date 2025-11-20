#!/bin/bash
# ReqMind - Easy Run Script for Unix/Mac

echo "========================================"
echo "Starting ReqMind"
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo
    echo "Please run: ./install_unix.sh first"
    echo
    exit 1
fi

# Check if virtual environment is activated
python -c "import sys; sys.exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo
    echo "Please create .env file with your HUGGINGFACE_API_KEY"
    echo "You can copy .env.example and edit it:"
    echo "  cp .env.example .env"
    echo "  nano .env"
    echo
    exit 1
fi

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "WARNING: data directory not found!"
    echo
    echo "Creating data directory..."
    mkdir data
    echo "Please add your PDF files to the 'data' folder"
    echo
    exit 1
fi

echo "Starting ReqMind..."
echo

cd src
python main.py
cd ..
