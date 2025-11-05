@echo off
REM Script to stop the locally running school management system server
REM This script finds and stops any Python processes running the application

echo Stopping School Management System server...

REM Find and kill Python processes running uvicorn or main.py
FOR /F "tokens=1,2" %%A IN ('tasklist /FI "IMAGENAME eq python.exe" /FO TABLE /NH') DO (
    REM Check if this is our uvicorn process
    tasklist /FI "PID eq %%B" /FI "WINDOWTITLE eq *uvicorn*" /FO TABLE /NH > nul 2>&1
    IF NOT ERRORLEVEL 1 (
        echo Found uvicorn process with PID: %%B
        taskkill /PID %%B /F
        echo Process terminated.
    ) ELSE (
        REM Check if this is a Python process running main.py
        wmic process where "ProcessId=%%B" get CommandLine | findstr "main.py" > nul 2>&1
        IF NOT ERRORLEVEL 1 (
            echo Found Python process running main.py with PID: %%B
            taskkill /PID %%B /F
            echo Process terminated.
        )
    )
)

REM Alternative approach: Find and kill process using port 8000
echo Checking for processes using port 8000...
FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') DO (
    echo Found process using port 8000 with PID: %%P
    taskkill /PID %%P /F
    echo Process terminated.
)

echo All server processes should now be stopped.
pause
