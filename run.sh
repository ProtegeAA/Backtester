#!/bin/bash

# Stock Backtester - One-Click Runner (Unix/Mac/Linux)
# This script automatically sets up the environment and runs the backtester

set -e  # Exit on error

echo "======================================"
echo "  Stock Backtester - One-Click Setup  "
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_CMD="python3"

# Check Python version (must be 3.7+)
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 7 ]); then
    echo "Error: Python 3.7 or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment found"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade requirements
echo "Checking dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "✓ All dependencies installed"

echo ""
echo "======================================"
echo "  Setup Complete! Starting Backtester"
echo "======================================"
echo ""

# Run the interactive launcher
python3 launcher.py

# Deactivate virtual environment
deactivate
