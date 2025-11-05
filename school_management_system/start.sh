#!/bin/bash
# Script to start the School Management System

# Change to the script's directory
cd "$(dirname "$0")"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if the virtual environment exists
if [ -d "venv" ]; then
    echo "Using existing virtual environment..."
    # Activate the virtual environment
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Error: Failed to activate virtual environment"
        exit 1
    fi
else
    echo "Creating virtual environment..."
    python -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
    
    # Activate the virtual environment
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Error: Failed to activate virtual environment"
        exit 1
    fi
    
    # Run the setup script
    echo "Running setup script..."
    python setup.py
    if [ $? -ne 0 ]; then
        echo "Error: Setup failed"
        exit 1
    fi
fi

# Run the application
echo "Starting the application..."
python run.py
