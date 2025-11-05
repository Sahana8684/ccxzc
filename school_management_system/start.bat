@echo off
REM Script to start the School Management System on Windows

REM Change to the script's directory
cd /d "%~dp0"

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Check if the virtual environment exists
if exist venv\ (
    echo Using existing virtual environment...
    REM Activate the virtual environment
    call venv\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to activate virtual environment
        exit /b 1
    )
) else (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to create virtual environment
        exit /b 1
    )
    
    REM Activate the virtual environment
    call venv\Scripts\activate.bat
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to activate virtual environment
        exit /b 1
    )
    
    REM Run the setup script
    echo Running setup script...
    python setup.py
    if %ERRORLEVEL% neq 0 (
        echo Error: Setup failed
        exit /b 1
    )
)

REM Run the application
echo Starting the application...
python run.py
