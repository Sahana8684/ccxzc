#!/usr/bin/env python
"""
Script to run the College Management System application.
"""
import os
import sys

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Apply bcrypt patch before importing any other modules
from school_management_system.utils.bcrypt_patch import apply_patch
apply_patch()

import uvicorn

if __name__ == "__main__":
    print("Starting College Management System...")
    print("The application will be available at http://localhost:8000")
    print("API documentation will be available at http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    # Use a direct reference to the main.py file in the current directory
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, 
                app_dir=os.path.dirname(os.path.abspath(__file__)),
                root_path="/")
