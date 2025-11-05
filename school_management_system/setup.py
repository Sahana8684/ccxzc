#!/usr/bin/env python
"""
Setup script for the School Management System.
This script checks if all required packages are installed and installs them if they're not.
"""
import subprocess
import sys
import os


def check_and_install_packages():
    """
    Check if all required packages are installed and install them if they're not.
    """
    print("Checking required packages...")
    
    # Get the path to the requirements.txt file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(current_dir, "requirements.txt")
    
    # Check if the requirements.txt file exists
    if not os.path.exists(requirements_file):
        print(f"Error: Requirements file not found at {requirements_file}")
        return False
    
    # Install the required packages
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("All required packages installed successfully.")
        
        # Check if pydantic-settings is installed
        try:
            import pydantic_settings
            print("pydantic-settings is already installed.")
        except ImportError:
            print("Installing pydantic-settings...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pydantic-settings"])
            print("pydantic-settings installed successfully.")
        
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to install required packages.")
        return False


if __name__ == "__main__":
    print("Setting up the School Management System...")
    
    # Check and install required packages
    if check_and_install_packages():
        print("\nSetup completed successfully.")
        print("You can now run the application using:")
        print("  python run.py")
    else:
        print("\nSetup failed. Please check the error messages above.")
