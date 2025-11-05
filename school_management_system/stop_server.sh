#!/bin/bash

# Script to stop the locally running school management system server
# This script finds and stops any uvicorn processes running the application

echo "Stopping School Management System server..."

# Find uvicorn processes
PIDS=$(ps aux | grep "[u]vicorn.*school_management_system" | awk '{print $2}')

if [ -z "$PIDS" ]; then
    # Try finding any uvicorn process
    PIDS=$(ps aux | grep "[u]vicorn" | awk '{print $2}')
fi

if [ -z "$PIDS" ]; then
    # Try finding any Python process with main.py
    PIDS=$(ps aux | grep "[p]ython.*main.py" | awk '{print $2}')
fi

if [ -z "$PIDS" ]; then
    echo "No running server found."
    exit 0
fi

# Kill each process
for PID in $PIDS; do
    echo "Stopping process with PID: $PID"
    kill $PID
    
    # Check if process was killed
    sleep 1
    if ps -p $PID > /dev/null; then
        echo "Process $PID did not stop gracefully. Forcing termination..."
        kill -9 $PID
    fi
done

echo "Server stopped successfully."

# Alternative approach: Find and kill process using a specific port
PORT=8000
echo "Checking for processes using port $PORT..."

if command -v lsof &> /dev/null; then
    PORT_PIDS=$(lsof -ti:$PORT)
    if [ ! -z "$PORT_PIDS" ]; then
        echo "Found processes using port $PORT: $PORT_PIDS"
        echo "Stopping these processes..."
        kill $PORT_PIDS
        sleep 1
        # Check if processes are still running
        REMAINING=$(lsof -ti:$PORT)
        if [ ! -z "$REMAINING" ]; then
            echo "Forcing termination of remaining processes..."
            kill -9 $REMAINING
        fi
        echo "All processes using port $PORT have been stopped."
    fi
else
    echo "lsof command not found. Cannot check for processes using port $PORT."
fi

echo "All server processes should now be stopped."
